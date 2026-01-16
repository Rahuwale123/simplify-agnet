from langchain.agents import AgentOutputParser
from langchain_core.agents import AgentAction, AgentFinish
from langchain.output_parsers.json import parse_json_markdown
from typing import Union

class RobustJSONAgentOutputParser(AgentOutputParser):
    """
    Parses the output of the agent. 
    If strict JSON parsing fails, it treats the entire text as a Final Answer 
    instead of raising an exception.
    """
    
    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            # 1. Attempt to parse as JSON (handles markdown code blocks too)
            response = parse_json_markdown(text)
            
            # 3. Check for "action" and "action_input"
            if isinstance(response, dict): 
                if "action" in response:
                    action = response["action"]
                    
                    # CASE A: Standard Format (has action_input)
                    if "action_input" in response:
                        action_input = response["action_input"]
                        if action == "Final Answer":
                            return AgentFinish({"output": action_input}, text)
                        return AgentAction(action, action_input, text)
                        
                    # CASE B: Flat Format (missing action_input, keys are at root)
                    # e.g. {"action": "save_field", "field": "title", "value": "CEO"}
                    # construct action_input from the rest of the dict
                    else:
                        action_input = response.copy()
                        del action_input["action"]
                        return AgentAction(action, action_input, text)
            
            # 4. Valid JSON but NO "action" key? Treat as final answer.
            return AgentFinish({"output": str(response)}, text)

        except Exception:
            # 5. Fallback: Try ast.literal_eval for Python-style dicts (single quotes)
            try:
                import ast
                # Clean text (remove markdown backticks if present but missed by json parser)
                clean_text = text.strip().replace("```json", "").replace("```", "").strip()
                response = ast.literal_eval(clean_text)
                
                if isinstance(response, dict) and "action" in response:
                    action = response["action"]
                    
                    # CASE A: Standard
                    if "action_input" in response:
                        action_input = response["action_input"]
                        if action == "Final Answer":
                            return AgentFinish({"output": action_input}, text)
                        return AgentAction(action, action_input, text)
                    
                    # CASE B: Flat
                    else:
                        action_input = response.copy()
                        del action_input["action"]
                        return AgentAction(action, action_input, text)
            except:
                pass

            # 4. Parsing failed (likely natural language). Treat as Final Answer.
            # This eliminates the "Invalid Format" retry loop.
            return AgentFinish({"output": text}, text)

    @property
    def _type(self) -> str:
        return "robust_json_chat"
