import datetime
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class TypeToken(BaseModel):
    refresh: str = "refresh"
    access: str = "access"


class Auth(BaseModel):
    public_key: Path = BASE_DIR / "src" / "certs" / "jwt-public.pem"
    private_key: Path = BASE_DIR / "src" / "certs" / "jwt-private.pem"
    algorithm: str = "RS256"
    access_exp: datetime.timedelta = datetime.timedelta(hours=52)
    refresh_exp: datetime.timedelta = datetime.timedelta(days=30)
    type_token: TypeToken = TypeToken()
    cookie_refresh: str = "refresh-token"
    cookie_access: str = "access-token"


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    auth: Auth = Auth()

    @property
    def POSTGRES_URL(self):
        return (f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
