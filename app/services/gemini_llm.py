import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.config.settings import settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def get_gemini_llm():
    # Check for direct override
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    # 1. Direct OpenAI Mode (Instant, no fallback logic needed)
    if provider == "openai":
        print(f"🚀 INITIALIZING LLM: OpenAI (GPT-4o) [PROVIDER={provider}]")
        return ChatOpenAI(
            model="gpt-4o",
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )

    print(f"🌍 INITIALIZING LLM: Gemini 2.0 Flash (with OpenAI Fallback) [PROVIDER={provider}]")
    # 2. Gemini Mode (With OpenAI Fallback)
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7,
        max_retries=0, # FAIL FAST
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    openai_llm = ChatOpenAI(
        model="gpt-4o",
        api_key=settings.OPENAI_API_KEY,
        temperature=0.7
    )

    return gemini_llm.with_fallbacks([openai_llm])
