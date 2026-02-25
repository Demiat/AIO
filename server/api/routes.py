from aiohttp import web

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
            "/api/v1/employee/{employee_id}", views.EmployeesViewDetail
        ),
        web.view("/api/v1/employee", views.EmployeesView),
    ])
