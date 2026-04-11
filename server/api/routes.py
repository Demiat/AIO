from aiohttp import web

from server.api import rpc, views
from server.core.json_utf8 import json_response_utf8


def add_routes(app):
    """
    Связывает обработчики с путями эндпоинтов в URL.
    """
    app.add_routes([
        web.get("/", lambda request: json_response_utf8(
            "Hi, World! Привет, МИР!")
        ),
        web.view(
            "/api/v1/employees/{employee_id}", views.EmployeesViewDetail
        ),
        web.view("/api/v1/employees", views.EmployeesView),
        web.post(
            "/api/v1/rpc", rpc.aiohttp_rpc.rpc_server.handle_http_request
        ),
    ])
