import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"), override=False)

class Config:
    ENV_STATE: str
    DB_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SECRET_KEY: str = os.getenv("SECRET_KEY") 

class TestConfig(Config):
    ENV_STATE = "test"
    DB_URL = os.getenv("TEST_DB_URL")

class DevConfig(Config):
    ENV_STATE = "dev"
    DB_URL = os.getenv("DB_URL")

def get_config(env_state: str) -> Config:
    configs = {
        "test": TestConfig,
        "dev": DevConfig
    }
    if env_state not in configs:
        raise ValueError(f"Invalid environment state: {env_state}")
    return configs[env_state]()

config = get_config(os.getenv("ENV_STATE"))