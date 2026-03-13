from typing import Union, Optional

from sqlalchemy.exc import IntegrityError
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r201, r204, r404


from server.database.models.schemas import (
    EmployeeCreate, EmployeeResponse, EmployeeListResponse, Error
)
from . import employee_manager

EMPLOYEE_EXISTS = "Employee already exists."


class EmployeesView(PydanticView):

    async def post(self, employee: EmployeeCreate) -> r201[EmployeeResponse]:
        """
        Создает сотрудника.
        Tags: Employees
        """
        # json employee уже валидирован
        try:
            created_employee = await employee_manager.create_employee(employee)
        except IntegrityError:
            raise web.HTTPBadRequest(
                    reason=EMPLOYEE_EXISTS,
                )
        return web.Response(
            text=EmployeeResponse.model_validate(created_employee).model_dump_json(),
            status=201,
            content_type='application/json'
        )

    async def get(
            self,
            limit: Optional[int] = None,
            page: Optional[int] = None,
    ) -> r200[EmployeeListResponse]:
        """
        Выводит список сотрудников.
        Tags: Employees
        """
        emp_list = await employee_manager.get_employees(limit, page)
        return web.Response(
            text=EmployeeListResponse(**emp_list).model_dump_json(),
            content_type='application/json'
        )


class EmployeesViewDetail(PydanticView):

    async def get(self, employee_id: int, /) -> Union[
        r200[EmployeeResponse], r404[Error]
    ]:
        """
        Получает сотрудника по ID.
        Tags: Employees
        """
        employee = await employee_manager.get_employee(employee_id)
        if not employee:
            raise web.HTTPNotFound(reason="Employee not found")
        return web.Response(
            text=EmployeeResponse.model_validate(
                employee
            ).model_dump_json(),
            content_type='application/json'
        )

    async def put(
        self, employee_id: int, /, employee: EmployeeCreate
    ) -> Union[r200[EmployeeResponse], r404[Error]]:
        """
        Обновляет сотрудника по ID.
        Tags: Employees
        """
        updated_employee = await employee_manager.update_employee(
            employee_id,
            employee
        )
        if not updated_employee:
            raise web.HTTPNotFound(reason="Employee not found")
        EmployeeResponse.model_validate(updated_employee)
        return web.Response(
            text=updated_employee.model_dump_json(),
            content_type='application/json'
        )

    async def delete(self, employee_id: int, /) -> Union[r204, r404[Error]]:
        """
        Удаляет сотрудника по ID.
        Tags: Employees
        """
        delete_employee = await employee_manager.delete_employee(
            employee_id
        )
        if not delete_employee:
            raise web.HTTPNotFound(reason="Employee not found")
        return web.json_response(
            {"message": f"Сотрудник c ID {employee_id} удален!"},
            status=204
        )
