from typing import Union, Optional

from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200, r201, r204, r404


from server.database.models.schemas import (
    EmployeeCreate, EmployeeResponse, EmployeeListResponse, Error
)
from .managers import EmployeeManager

employee_manager = EmployeeManager()


class EmployeesView(PydanticView):

    async def post(self, employee: EmployeeCreate) -> r201[EmployeeResponse]:
        """
        Создает сотрудника.
        Tags: Employees
        """
        # employee уже валидирован
        created_employee = await employee_manager.create_employee(employee)
        return web.Response(
            text=created_employee.model_dump_json(),
            content_type='application/json',
            status=201
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
            text=emp_list.model_dump_json(),
            content_type='application/json'
        )


class EmployeesViewDetail(PydanticView):

    async def get(self, employee_id: int, /) -> Union[
        r200[EmployeeResponse], r404[Error]
    ]:
        """
        Обновить сотрудника по ID.
        Tags: Employees
        """
        employee = await employee_manager.get_employee(employee_id)
        return web.Response(
            text=employee.model_dump_json(),
            content_type='application/json'
        )

    async def put(
        self, employee_id: int, /, employee: EmployeeCreate
    ) -> Union[r200[EmployeeResponse], r404[Error]]:
        """
        Обновить сотрудника по ID.
        Tags: Employees
        """
        updated_employee = await employee_manager.update_employee(
            employee_id,
            employee
        )
        return web.Response(
            text=updated_employee.model_dump_json(),
            content_type='application/json'
        )

    async def delete(self, employee_id: int, /) -> Union[r204, r404[Error]]:
        """
        Удалить сотрудника по ID.
        Tags: Employees
        """
        return web.json_response(
            {"message": f"Сотрудник {employee_id} удален!"},
            status=204
        )
