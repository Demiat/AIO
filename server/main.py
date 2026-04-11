from aiohttp import web
from aiohttp_pydantic import oas

from server.api.routes import add_routes
from server.core import settings
from server.logger import setup_logging
from server.middleware import request_logging_middleware


def create_app() -> web.Application:
    """Создает и настраивает приложение."""

    # Настраиваем логирование
    setup_logging()

    app = web.Application(middlewares=[
        request_logging_middleware,
    ])

    # Настраиваем OpenAPI документацию
    oas.setup(app)

    # Регистрируем роуты
    add_routes(app)

    return app


# Создаем глобальный экземпляр приложения
app = create_app()

if __name__ == "__main__":
    web.run_app(app, host=settings.HOST, port=settings.PORT)
