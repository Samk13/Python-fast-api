# -*- coding: utf-8 -*-
from pydantic import BaseSettings

# It will validate the settings and will raise an error if the settings are not valid or missing


class Settings(BaseSettings):
    # should set theses value in the .env file or you will get an error
    database_hostname: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    # specifiy where the env file is located

    class Config:
        env_file = ".env"


settings = Settings()
settings.database_password
