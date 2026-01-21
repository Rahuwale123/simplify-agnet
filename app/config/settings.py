import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Gemini LangChain Agent"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Gemini Settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://v4-qa.simplifysandbox.net/config/v1/api/program")

    # Server Settings
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Database Settings
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASS: str = os.getenv("DB_PASS", "password")
    DB_NAME: str = os.getenv("DB_NAME", "simi_db")

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
