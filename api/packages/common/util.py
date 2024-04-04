from typing import Any
from dotenv import dotenv_values
import os


class Config:
    config = None

    @classmethod
    def env_get(cls, key: str, default: Any = None) -> Any:
        if cls.config is None:
            api_dir = os.path.join(os.path.dirname(__file__), '../..')
            env_path = os.path.join(os.path.abspath(api_dir), '.env')
            cls.config = dotenv_values(env_path)
        return cls.config.get(key, default)
