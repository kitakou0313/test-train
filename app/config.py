from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./taskdb.sqlite3"
    app_env: str = "development"
    secret_key: str = "dev-secret-key-change-in-production"

    model_config = {"env_file": ".env"}


settings = Settings()
