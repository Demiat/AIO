import json

from aiohttp import web
from aiohttp_pydantic import oas

from server.api.routes import add_routes
from server.core import settings
from server.middleware import request_logging_middleware
from server.logger import setup_logging


def create_app() -> web.Application:

    # Настраиваем логирование
    setup_logging()

    # Работаем с JSON в UTF-8
    json._default_encoder.ensure_ascii = False

    app = web.Application(middlewares=[
        request_logging_middleware,
    ])

    # Настраиваем OpenAPI документацию
    oas.setup(app)

    # Регистрируем роуты
    add_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host=settings.HOST, port=settings.PORT)
