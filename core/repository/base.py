from typing import Generic, List, Optional, Type, TypeVar, Union

from asyncpg.exceptions import (
    NotNullViolationError,
    UndefinedTableError,
    UniqueViolationError,
)
from sqlalchemy import delete, select, update
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    ProgrammingError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.session import Base
from core.exceptions.base import DatabaseError, UnprocessableEntity
from core.repository.enum import SynchronizeSessionEnum
from core.utils.logging import logger

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.session = db_session
        self.model = model

    async def create(self, params: dict) -> ModelType:
        """
        Create a new instance of the model in the database.

        Args:
            params (Dict[str, Any]): Model attributes for creation

        Returns:
            ModelType: Created model instance

        Raises:
            UnprocessableEntity: For unique constraint or null violations
            DatabaseError: For database-related errors
            ValueError: If session is not initialized
        """
        try:

            instance = self.model(**params)
            if self.session is None:
                raise ValueError("Session is not initialized.")
            self.session.add(instance)

            await self.session.flush()
            return instance
        except IntegrityError as e:
            logger.error(f"IntegrityError occurred: {e}", exc_info=True)

            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UniqueViolationError.sqlstate:
                logger.warning(f"Unique constraint violation: {e}")
                raise UnprocessableEntity("Unique constraint violation") from e
            if error_code == NotNullViolationError.sqlstate:
                logger.warning(f"Required field cannot be null: {e}")
                raise UnprocessableEntity("Required field cannot be null") from e

            raise DatabaseError("Integrity error while Creating record.") from e
        except ProgrammingError as e:
            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UndefinedTableError.sqlstate:
                raise DatabaseError("Database table does not exist.") from e

            raise DatabaseError("Database programming error occurred.") from e
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError("Database error occurred.") from e

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Retrieve all instances of the model with pagination support
        Args:
            skip (int): Skip the instances
            limit (int): Number of instances to fetch in one go

        Raises:
            NoResultFound: If record with ID doesn't exist
            DatabaseError: If database update fails
        """
        try:
            query = select(self.model).offset(skip).limit(limit)
            result = await self.session.execute(query)
            return result.scalars().all()
        except ProgrammingError as e:
            logger.error(f"Database table does not exist: {e}", exc_info=True)
            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UndefinedTableError.sqlstate:
                raise DatabaseError("Database table does not exist.") from e

            raise DatabaseError("Database programming error occurred.") from e
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError("Database error occurred.") from e

    async def get_by_field(
        self, field: str, value: Union[str, int]
    ) -> Optional[ModelType]:
        """
        Fetch all instances of a Model by a specific field

        Args:
            params (str): Field to fetch data
            id (int): Record ID to match

        Raises:
            NoResultFound: If record with ID doesn't exist
            DatabaseError: If database update fails
        """
        try:
            model_field = getattr(self.model, field, None)

            if model_field is None:
                raise ValueError(f"Field '{field}' does not exist in the model.")

            query = select(self.model).where(model_field == value)

            result = await self.session.execute(query)
            return result.scalars().first()
        except ProgrammingError as e:
            logger.error(f"Database table does not exist: {e}", exc_info=True)
            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UndefinedTableError.sqlstate:
                raise DatabaseError("Database table does not exist.") from e

            raise DatabaseError("Database programming error occurred.") from e
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError("Database error occurred.") from e

    async def update_by_id(
        self,
        id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        """
        Update a model instance by ID.

        Args:
            id (int): Record ID to update
            params (Dict[str, Any]): Fields and values to update
            synchronize_session (SynchronizeSessionEnum, optional): Synchronization strategy

        Raises:
            NoResultFound: If record with ID doesn't exist
            DatabaseError: If database update fails
        """
        try:
            query = (
                update(self.model)
                .where(self.model.id == id)
                .values(**params)
                .execution_options(synchronize_session=synchronize_session)
            )
            result = await self.session.execute(query)
            await self.session.commit()
            if result.rowcount == 0:
                raise NoResultFound(f"No record found with id {id}")
            return {"message": "Record updated successfully"}
        except NoResultFound:
            logger.warning(f"No record found with id {id}")
            raise
        except IntegrityError as e:
            logger.error(f"IntegrityError occurred: {e}", exc_info=True)
            raise DatabaseError from e
        except ProgrammingError as e:
            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UndefinedTableError.sqlstate:
                logger.error("Database table does not exist.", exc_info=True)

            logger.error("Database programming error occurred.", exc_info=True)
            raise DatabaseError from e
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError from e

    async def delete(self, model: ModelType) -> None:
        """
        Delete a model instance
        Args:
            model (ModelType): Model Instance

        Raises:
            DatabaseError: If database update fails
        """
        try:
            await self.session.delete(model)
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError from e

    async def delete_by_id(
        self,
        id: int,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        """
        Delete a model instance by ID.

        Args:
            id (int): Record ID to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            NoResultFound: If record with ID doesn't exist
            DatabaseError: If database deletion fails
        """
        try:
            query = (
                delete(self.model)
                .where(self.model.id == id)
                .returning(self.model)
                .execution_options(synchronize_session=synchronize_session)
            )
            result = await self.session.execute(query)
            deleted_row = result.scalar()
            if not deleted_row:
                logger.warning(f"No record found with id {id}")
                raise NoResultFound(f"No record found with id {id}")
        except NoResultFound:
            logger.warning(f"No record found with id {id}")
            raise
        except IntegrityError as e:
            logger.error(f"Integrity Error occurred: {e}", exc_info=True)
            raise DatabaseError from e
        except ProgrammingError as e:
            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UndefinedTableError.sqlstate:
                logger.error("Database table does not exist.", exc_info=True)

            logger.error("Database programming error occurred.", exc_info=True)
            raise DatabaseError from e
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError from e

    async def refresh(self, instance: ModelType) -> None:
        """
        Refresh the given instance from the database.

        Args:
            instance (ModelType): Model instance to refresh

        Raises:
            DatabaseError: If refresh operation fails
        """
        try:
            result = await self.session.refresh(instance)
        except ProgrammingError as e:
            error_code = getattr(e.orig, "sqlstate", None)
            if error_code == UndefinedTableError.sqlstate:
                logger.error("Database table does not exist.", exc_info=True)

            logger.error("Database programming error occurred.", exc_info=True)
            raise DatabaseError from e
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}", exc_info=True)
            raise DatabaseError from e
