from typing import *

import aiohttp

from ..api_config import APIConfig, HTTPException
from ..models import *


async def get_apiv1employeesemployee_id(
    api_config_override: Optional[APIConfig] = None, *, employee_id: int
) -> EmployeeResponse:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/v1/employees/{employee_id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}

    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(
            "get",
            base_path + path,
            params=query_params,
        ) as initial_response:
            if initial_response.status != 200:
                raise HTTPException(
                    initial_response.status,
                    f"get_apiv1employeesemployee_id failed with status code: {initial_response.status}",
                )
            # Only parse JSON when a body is expected (avoid errors on 204 No Content)
            body = None if 200 == 204 else await initial_response.json()

        return EmployeeResponse(**body) if body is not None else EmployeeResponse()


async def put_apiv1employeesemployee_id(
    api_config_override: Optional[APIConfig] = None, *, employee_id: int, data: EmployeeCreate
) -> EmployeeResponse:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/v1/employees/{employee_id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}

    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request("put", base_path + path, params=query_params, json=data.dict()) as initial_response:
            if initial_response.status != 200:
                raise HTTPException(
                    initial_response.status,
                    f"put_apiv1employeesemployee_id failed with status code: {initial_response.status}",
                )
            # Only parse JSON when a body is expected (avoid errors on 204 No Content)
            body = None if 200 == 204 else await initial_response.json()

        return EmployeeResponse(**body) if body is not None else EmployeeResponse()


async def delete_apiv1employeesemployee_id(
    api_config_override: Optional[APIConfig] = None, *, employee_id: int
) -> None:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/v1/employees/{employee_id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}

    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(
            "delete",
            base_path + path,
            params=query_params,
        ) as initial_response:
            if initial_response.status != 204:
                raise HTTPException(
                    initial_response.status,
                    f"delete_apiv1employeesemployee_id failed with status code: {initial_response.status}",
                )
            # Only parse JSON when a body is expected (avoid errors on 204 No Content)
            body = None if 204 == 204 else await initial_response.json()

        return None


async def get_apiv1employees(
    api_config_override: Optional[APIConfig] = None, *, limit: Optional[int] = None, page: Optional[int] = None
) -> EmployeeListResponse:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/v1/employees"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {"limit": limit, "page": page}

    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(
            "get",
            base_path + path,
            params=query_params,
        ) as initial_response:
            if initial_response.status != 200:
                raise HTTPException(
                    initial_response.status, f"get_apiv1employees failed with status code: {initial_response.status}"
                )
            # Only parse JSON when a body is expected (avoid errors on 204 No Content)
            body = None if 200 == 204 else await initial_response.json()

        return EmployeeListResponse(**body) if body is not None else EmployeeListResponse()


async def post_apiv1employees(
    api_config_override: Optional[APIConfig] = None, *, data: EmployeeCreate
) -> EmployeeResponse:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/api/v1/employees"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}

    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request("post", base_path + path, params=query_params, json=data.dict()) as initial_response:
            if initial_response.status != 201:
                raise HTTPException(
                    initial_response.status, f"post_apiv1employees failed with status code: {initial_response.status}"
                )
            # Only parse JSON when a body is expected (avoid errors on 204 No Content)
            body = None if 201 == 204 else await initial_response.json()

        return EmployeeResponse(**body) if body is not None else EmployeeResponse()
