from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Use SQLite by default

    class Config:
        env_file = ".env"

    @property
    def database_url(self):
        return self.DATABASE_URL

settings = Settings() 