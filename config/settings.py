import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

for env_file in (".env"):
    if os.path.exists(env_file):
        load_dotenv(env_file, override=False)
        break


class Settings(BaseSettings):
    app_name: str = "Homeopathic Backend"
    app_version: str = "0.1.0"
    database_url: str | None = None
    direct_url: str | None = None
    docs_username: str | None = None
    docs_password: str | None = None
    debug: bool = False

    model_config = SettingsConfigDict(env_file=(".env"), extra="ignore")

    @property
    def sqlalchemy_database_url(self) -> str:
        raw_url = self.direct_url or self.database_url or "postgresql+psycopg://postgres:postgres@localhost:5432/homeopathic"
        if raw_url.startswith("postgresql://"):
            return raw_url.replace("postgresql://", "postgresql+psycopg://", 1)
        return raw_url


settings = Settings()
