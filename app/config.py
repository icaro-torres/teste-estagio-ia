from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Teste IA API"
    OLLAMA_HOST: str = "http://localhost:11434"
    # MUDANÇA AQUI
    OLLAMA_MODEL: str = "llama3.2" 

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()