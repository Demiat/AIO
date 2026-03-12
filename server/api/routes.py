from aiohttp import web
import aiohttp_rpc

from server.api import views


def add_routes(app):
    """
    Связывает обработчики с путями эндпоинтов в URL.
    """

    app.add_routes([
        web.get("/", lambda request: web.json_response(
            "Hi, World! Привет, МИР!")
        ),
        web.view(
            "/api/v1/employees/{employee_id}", views.EmployeesViewDetail
        ),
        web.view("/api/v1/employees", views.EmployeesView),
        web.post("/api/v1/rpc", aiohttp_rpc.rpc_server.handle_http_request),
    ])
