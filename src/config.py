from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_IP: str
    DB_PORT: int
    DB_USER: str
    DB_PWD: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_IP}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
