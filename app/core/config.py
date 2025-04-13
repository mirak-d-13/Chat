from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_url: str = os.getenv("DATABASE_URL")
    db_echo: bool = True

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")


settings = Settings()
