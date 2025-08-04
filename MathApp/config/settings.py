from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./requests.db"
    global_token: str = "token123"

    class Config:
        env_file = ".env"


settings = Settings()
