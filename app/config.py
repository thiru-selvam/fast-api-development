from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_driver: str = 'postgresql'
    database_hostname: str = 'localhost'
    database_port: int = 5432
    database_username: str = 'postgres'
    database_password: str = 'postgres'
    database_name: str = 'postgres'
    secret_key: str = 'd92003a7c5623d8df0c5d52b690102ef4201454bb3c37e9127eb42c28bf7166d'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60

    class Config:
        env_file = '.env'


settings = Settings()
