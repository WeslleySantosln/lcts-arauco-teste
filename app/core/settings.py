from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "LCTS API"

    VERSION: str = "0.1.0"

    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql://user:password@localhost/lcts"

    UPDATE_INTERVAL: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    SIMULATION_INTERVAL_SECONDS: int = 1
    SIMULATION_SPEED_SECONDS: int = 300
    MAX_ACTIVE_DELIVERIES: int = 20


settings = Settings()