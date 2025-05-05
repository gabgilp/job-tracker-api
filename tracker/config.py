import os
from dotenv import load_dotenv

class Config:
    ENV_STATE: str
    DB_URL: str
    FORCE_ROLL_BACK: bool

class TestConfig(Config):
    ENV_STATE = "test"
    DB_URL = os.getenv("TEST_DB_URL")
    FORCE_ROLL_BACK = True

class DevConfig(Config):
    ENV_STATE = "dev"
    DB_URL = os.getenv("DB_URL")
    FORCE_ROLL_BACK = False

def get_config(env_state: str) -> Config:
    configs = {
        "test": TestConfig,
        "dev": DevConfig
    }
    if env_state not in configs:
        raise ValueError(f"Invalid environment state: {env_state}")
    return configs[env_state]()

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"), override=False)
config = get_config(os.getenv("ENV_STATE", "dev"))