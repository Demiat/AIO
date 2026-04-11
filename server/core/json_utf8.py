import json
from typing import Any

from aiohttp import web


# Фабрика для ответов JSON с UTF-8
def json_response_utf8(data: Any, **kwargs: Any) -> web.Response:
    """Обертка над web.json_response с читаемым UTF-8."""
    return web.json_response(
        data,
        dumps=lambda d: json.dumps(d, ensure_ascii=False),
        **kwargs
    )
