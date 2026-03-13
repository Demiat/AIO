"""Менеджеры работы с базой данных."""
from typing import Optional, Type

from sqlalchemy import insert, update, select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.core import DBDependency
from server.database.models import Employee
from server.database.models.schemas import (
    EmployeeCreate,
)
from .pagination import pg_offset

EMPLOYEE_EXISTS = "Employee already exists."


class EmployeeManager:
    """Работает с сотрудниками в базе данных."""

    def __init__(self, db: Optional[DBDependency] = None):
        self.db = db or DBDependency()
        self.model: Type[Employee] = Employee

    async def _get_employee(self, session: AsyncSession, employee_id: int) -> Optional[Employee]:
        """Получает сотрудника из базы или None"""
        result = await session.execute(
            select(self.model).where(self.model.id == employee_id)
        )
        return result.scalar_one_or_none()


    async def create_employee(
        self,
        employee: EmployeeCreate,
    ) -> Employee:
        """Создает сотрудника."""
        async with self.db.db_session() as session:
            try:
                result = await session.execute(
                    insert(self.model)
                    .values(**employee.model_dump())
                    .returning(self.model)
                )
            except IntegrityError:
                raise
            await session.commit()
            return result.scalar_one()

    async def get_employees(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> dict:
        """Получает пагинированный список сотрудников."""
        async with self.db.db_session() as session:
            query = select(self.model)
            if limit is not None and page is not None:
                offset = pg_offset(limit, page)
                query = query.offset(offset).limit(limit)
            result = await session.execute(query)

            # Получим общее количество записей
            total = await session.scalar(
                select(
                    func.count(self.model.id)
                )
            )
            return {
                "total": total,
                "page": page,
                "limit": limit,
                "items": result.scalars().all()
            }

    async def get_employee(self, employee_id: int) -> Optional[Employee]:
        """Получает сотрудника по id."""
        async with self.db.db_session() as session:
            return await self._get_employee(session, employee_id)

    async def update_employee(
        self,
        employee_id: int,
        employee: EmployeeCreate,
    ) -> Optional[Employee]:
        """Обновляет поля сотрудника."""
        # Первый вариант обновления - работа с объектами,
        # можно пользоваться событиями sqlalchemy.
        # Минусы - дополнительный запрос в базу данных

        # db_employee = await self._get_employee(employee_id)
        # db_employee.name = employee.name
        # db_employee.email = employee.email

        # async with self.db.db_session() as session:
        #     session.add(db_employee)
        #     await session.commit()
        #     return db_employee

        # Второй вариант - просто SQL запрос, зато 1 запрос
        async with self.db.db_session() as session:
            result = await session.execute(
                update(self.model)
                .where(self.model.id == employee_id)
                .values(name=employee.name, email=employee.email)
                .returning(self.model)
            )
            updated_employee = result.scalar_one_or_none()
            await session.commit()
            return updated_employee
    
    async def delete_employee(self, employee_id: int) -> bool:
        """Удаляет сотрудника по ID."""
        async with self.db.db_session() as session:
            employee = await self._get_employee(session, employee_id)
            if not employee:
                return False
            await session.delete(employee)
            await session.commit()
            return True


