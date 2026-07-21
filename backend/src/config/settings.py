from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ==========================
    # Email Configuration
    # ==========================
    SMTP_HOST: str

    SMTP_PORT: int

    SMTP_USERNAME: str

    SMTP_PASSWORD: str

    SMTP_FROM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
