from dotenv import dotenv_values
from typing import List
from datetime import timedelta

# Load environment variables from .env file
values = dotenv_values()


class Config:
    DB_CONNECTION: str = values.get("DB_CONNECTION")
    DB_MODELS: List[str] = ["models.todo_model", "models.user_model"]
    SECRET_KEY: str = values.get("SECRET_KEY")
    ALGORITHM: str = values.get("ALGORITHM")
    JWT_ACCESS_EXP: timedelta = timedelta(days=1)
    JWT_REFRESH_EXP: timedelta = timedelta(days=30)
