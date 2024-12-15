from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "DEV", "PROD"]
    DB_NAME: str
    DB_IP: str
    DB_PORT: int
    DB_USER: str
    DB_PWD: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file='.env')

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_IP}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
