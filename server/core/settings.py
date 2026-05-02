from typing import Literal
# from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """Настройки для подключения базы данных."""

    env: Literal["dev", "test", "prod"] = "dev"

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_echo: bool

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_url = self._build_db_url()
    
    def _build_db_url(self) -> str:
        """
        Возвращает строку подключения к базе
        в зависимости от рабочего окружения.
        """
        if self.env == "test":
            return "sqlite+aiosqlite:///:memory:"
        elif self.env == "dev":
            return "sqlite+aiosqlite:///dev.db"
        else:  # prod
            return (
                f"postgresql+asyncpg://{self.db_user}:"
                f"{self.db_password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )

    # @cached_property
    # def db_url(self):
    #     """
    #     Возвращает строку подключения к базе
    #     в зависимости от рабочего окружения.
    #     """
    #     if self.env == "test":
    #         return "sqlite+aiosqlite:///:memory:"
    #     elif self.env == "dev":
    #         return "sqlite+aiosqlite:///dev.db"
    #     else:  # prod
    #         return (
    #             f"postgresql+asyncpg://{self.db_user}:"
    #             f"{self.db_password}@"
    #             f"{self.db_host}:{self.db_port}/{self.db_name}"
    #         )


class Settings(BaseSettings):
    """Совокупный класс настроек."""
    HOST: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore")

    db_settings: DBSettings = DBSettings()  # type: ignore[call-arg]


settings = Settings()  # type: ignore[call-arg]
