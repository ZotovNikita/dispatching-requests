from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    backend_base_url: str

    class Config:
        env_file = Path('.env')
        env_file_encoding = 'utf-8'
