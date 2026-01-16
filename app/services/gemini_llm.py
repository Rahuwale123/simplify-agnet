import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.config.settings import settings
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Singleton Cache
_cached_llm = None

def get_gemini_llm():
    global _cached_llm
    if _cached_llm is not None:
        return _cached_llm

    # Check for direct override
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    # 1. Direct OpenAI Mode (Instant, no fallback logic needed)
    if provider == "openai":
        print(f"🚀 INITIALIZING LLM: OpenAI (GPT-4o) [PROVIDER={provider}]")
        _cached_llm = ChatOpenAI(
            model="gpt-4o",
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )
        return _cached_llm

    print(f"🌍 INITIALIZING LLM: Gemini 2.0 Flash (NO Fallback) [PROVIDER={provider}]")
    # 2. Gemini Mode
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.7,
        max_retries=1, # Allow 1 retry? Or 0 to see errors fast.
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    # DISABLE OPENAI FALLBACK to avoid 401 errors when key is missing/invalid
    # openai_llm = ChatOpenAI(
    #     model="gpt-4o",
    #     api_key=settings.OPENAI_API_KEY,
    #     temperature=0.7
    # )

    # _cached_llm = gemini_llm.with_fallbacks([openai_llm])
    _cached_llm = gemini_llm
    return _cached_llm