from server.main import app
from server.database.models.schemas import EmployeeResponse


async def test_get_employee(aiohttp_client):
    client = await aiohttp_client(app)
    response = await client.get("/api/v1/employees/123")
    employee = EmployeeResponse.model_validate(await response.json())
    assert employee.name == "John"