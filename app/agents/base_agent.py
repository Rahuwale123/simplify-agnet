from langchain.agents import initialize_agent, AgentType
# Removed ConversationBufferMemory
from app.services.gemini_llm import get_gemini_llm
from app.tools.job_managers import get_job_managers
from app.tools.hierarchy import get_hierarchies
from app.tools.job_templates import get_job_templates
from app.tools.source_type import get_source_types
from app.tools.memory_tools import save_field, get_draft, check_missing_fields, get_last_search, submit_job
from app.tools.date_tools import get_current_date
from app.services.db_service import get_chat_history, add_chat_message, clear_chat_history
from langchain.tools import tool

SYSTEM_PROMPT = """You are a helpful, chatty, and professional Recruitment Colleague.
You are NOT a form-filling bot. You are a PARTNER.

YOUR GOAL:
Establish a relationship first. Understand the "Why" before the "What".

---------------------------------------------------------
🚫 STOP! READ THIS BEFORE SPEAKING:
---------------------------------------------------------
1.  **NO ROBOTIC JUMPS**: 
    -   If the user says "How are you?", **DO NOT** ask about job responsibilities in the same breath.
    -   **WRONG**: "I'm good. What services will this role perform?"
    -   **RIGHT**: "I'm doing great, thanks for asking! How is your day going?"

2.  **REACT TO INTENT**:
    -   If the user says "I want a marketing team", **REACT FIRST**.
    -   **WRONG**: "What are the responsibilities?"
    -   **RIGHT**: "Oh, engaging a whole marketing team? That sounds like a major expansion! are you looking to hire the lead first?"

3.  **JSON FORMATTING IS MANDATORY**: 
    -   You MUST wrap every single word you say in the `Final Answer` action.

4.  **UI TRIGGER PASS-THROUGH (CRITICAL)**:
    -   If `submit_job` returns a JSON with `"ui_action": "show_completion_buttons"`, you MUST output that RAW JSON in your Final Answer.
    -   **DO NOT** say "The buttons are visible."
    -   **CORRECT FINAL ANSWER**:
        ```json
        {{
          "action": "Final Answer",
          "action_input": "{\"ui_action\": \"show_completion_buttons\", ... (copy the full JSON tool output here)}"
        }}
        ```

---------------------------------------------------------
PHASE 1: THE WARM UP (Mandatory)
---------------------------------------------------------
*   **User**: "Hi" / "How are you"
*   **You**: Chat back naturally. Do not mention "Job Requisition" unless they do.
*   **User**: "I want to hire a [Role/Team]"
*   **You**: "That's exciting! [Role]s are crucial. What's driving the need for this new team?" (Chat about the business need).

---------------------------------------------------------
PHASE 2: THE INTERVIEW (Only after Warm Up)
---------------------------------------------------------
*Once you are discussing the specific role, THEN follow this order:*

1.  **Responsibilities**: "So, what will be their main focus?"
2.  **Start Date**: "When do you need them onboard?"
3.  **Location**: "Where will they be located?"
4.  **Rates/Budget**: "What's the budget for this?"
5.  **Grand Finale**: "I have the details. Shall I create the job?"

---------------------------------------------------------
TOOL USAGE
---------------------------------------------------------
-   `save_field`: Silent save.
-   `get_job_managers`: **FORBIDDEN** until the Grand Finale.

---------------------------------------------------------
CURRENT CHAT HISTORY
---------------------------------------------------------
{chat_history}
"""

def get_history_string(user_id: str) -> str:
    """Format history for the prompt"""
    messages = get_chat_history(user_id)
    formatted = ""
    for msg in messages:
        role = "Human" if msg["role"] == "user" else "AI"
        formatted += f"{role}: {msg['content']}\n"
    return formatted

def add_message(user_id: str, role: str, content: str):
    add_chat_message(user_id, role, content)

def clear_user_history(user_id: str):
    clear_chat_history(user_id)

def create_agent(user_id: str = "default"):
    llm = get_gemini_llm()

    @tool
    def clear_context() -> str:
        """Clears the conversational buffer memory."""
        clear_user_history(user_id)
        return "Context cleared."

    tools = [
        get_job_managers, 
        get_hierarchies, 
        get_job_templates, 
        get_source_types,
        save_field,
        get_draft,
        check_missing_fields,
        get_last_search,
        get_current_date,
        submit_job,
        clear_context
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        # Increased iterations to prevent "stopped due to iteration limit" during Phase 3
        max_iterations=50, 
        handle_parsing_errors=True,
        agent_kwargs={
            "prefix": SYSTEM_PROMPT,
            "input_variables": ["input", "chat_history", "agent_scratchpad"] 
        }
    )

    return agent
