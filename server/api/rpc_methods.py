import aiohttp_rpc

from . import employee_manager


@aiohttp_rpc.rpc_method()
async def calculate_salary(employee_id: int, hours: int):
    employee = await employee_manager.get_employee(employee_id)
    if not employee:
        raise aiohttp_rpc.errors.InvalidParams("Employee not found")
    return {"result": employee.rate_per_hour * hours}