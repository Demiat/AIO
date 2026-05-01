from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from .settings import settings


class DBDependency:
    def __init__(self) -> None:
        # Определяем тип БД по URL
        is_sqlite = settings.db_settings.db_url.startswith("sqlite")

        engine_kwargs: dict[str, Any] = dict()
        if is_sqlite:
            engine_kwargs["pool_pre_ping"] = False
            engine_kwargs["poolclass"] = NullPool
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        
        self._engine = create_async_engine(
            url=settings.db_settings.db_url,
            echo=settings.db_settings.db_echo,
            **engine_kwargs
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autocommit=False
        )

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
