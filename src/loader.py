from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_PORT_LOCAL: int
    DB_USER: str
    DB_NAME: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    model_config = ConfigDict(extra='ignore', env_file='.env')

    @property
    def pg_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()