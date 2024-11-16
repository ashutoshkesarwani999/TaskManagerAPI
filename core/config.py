import os
from dotenv import load_dotenv
from enum import Enum
from pydantic import  PostgresDsn

load_dotenv()

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"

def create_postgres_url():
    scheme = "postgresql+asyncpg"
    username = os.getenv("user", "postgres")
    password = os.getenv("password", "password123")
    host = os.getenv("host", "0.0.0.0")
    port = os.getenv("port", "5432")
    database = os.getenv("db", "dbtest")

    return f"{scheme}://{username}:{password}@{host}:{port}/{database}"

class Config():
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    POSTGRES_URL:PostgresDsn=   create_postgres_url()


config: Config = Config()