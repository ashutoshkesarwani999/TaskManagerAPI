from typing import Any, Generic, Type, TypeVar
from fastapi import HTTPException, status

from core.database import Base, Propagation, Transactional
from core.exceptions.base import (
    NotFoundException,
    UnprocessableEntity,
    InternalServerError,
    DatabaseError,
)
from core.repository.base import BaseRepo

ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    """
    Base controller class for handling CRUD operations on database models.

    This class provides a generic implementation for basic database operations
    including create, read, update, and delete (CRUD). It uses transaction
    management and proper error handling.

    Attributes:
        model_class (Type[ModelType]): The SQLAlchemy model class
        repository (BaseRepo): The repository instance for database operations

    Type Parameters:
        ModelType: A TypeVar bound to Base, representing the model type
    """

    def __init__(self, model: Type[ModelType], repository: BaseRepo):
        """
        Initialize the controller with a model class and repository.

        Args:
            model (Type[ModelType]): The SQLAlchemy model class
            repository (BaseRepo): The repository instance for database operations
        """
        self.model_class = model
        self.repository = repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def create(self, attributes: dict[str, Any]) -> ModelType:
        """
        Create a new instance of the model in the database.

        This method creates a new record in the database using the provided
        attributes. The operation is wrapped in a transaction.

        Args:
            attributes (dict[str, Any]): Dictionary of model attributes and their values

        Returns:
            ModelType: The newly created model instance

        Raises:
            UnprocessableEntity: If the attributes are invalid
            DatabaseError: If there's an error during database operation
        """
        try:
            create = await self.repository.create(attributes)
            return create
        except DatabaseError as e:
            raise InternalServerError from e

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        """
        Retrieve a paginated list of model instances.

        This method returns a list of model instances with pagination support
        and optional joining of related models.

        Args:
            skip (int, optional): Number of records to skip. Defaults to 0
            limit (int, optional): Maximum number of records to return. Defaults to 100

        Returns:
            list[ModelType]: List of model instances

        Raises:
            DatabaseError: If there's an error during database operation
        """
        try:
            response = await self.repository.get_all(skip, limit)
            return response
        except DatabaseError as e:
            raise InternalServerError from e

    async def get_by_id(self, id: int) -> ModelType:
        """
        Retrieve a single model instance by its ID.

        This method attempts to find and return a model instance matching
        the provided ID.

        Args:
            id (int): The unique identifier of the model instance

        Returns:
            ModelType: The found model instance

        Raises:
            NotFoundException: If no instance is found with the given ID
            DatabaseError: If there's an error during database operation
        """
        try:
            db_obj = await self.repository.get_by_field(
                field="id",
                value=id,
            )
            if not db_obj:
                raise NotFoundException(
                    f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
                )
            return db_obj
        except DatabaseError as e:
            raise InternalServerError from e

    @Transactional(propagation=Propagation.REQUIRED)
    async def update(
        self,
        id: int,
        attributes: dict[str, Any],
    ) -> ModelType:
        """
        Update an existing model instance.

        This method updates an existing record in the database with the provided
        attributes. The operation is wrapped in a transaction.

        Args:
            id (int): The unique identifier of the model instance to update
            attributes (dict[str, Any]): Dictionary of attributes to update
            join_ (Set[str], optional): Set of relationship names to join. Defaults to None

        Returns:
            ModelType: The updated model instance

        Raises:
            NotFoundException: If no instance is found with the given ID
            UnprocessableEntity: If no updates are provided or if updates are invalid
            DatabaseError: If there's an error during database operation
        """
        try:
            db_obj = await self.get_by_id(id)
            if not db_obj:
                raise NotFoundException(
                    f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
                )

            if db_obj == attributes:
                raise UnprocessableEntity("No updates provided")

            await self.repository.update_by_id(
                id=id, params=attributes, synchronize_session="evaluate"
            )
            ab = await self.get_by_id(id)

            await self.repository.refresh(ab)
            return ab
        except DatabaseError as e:
            raise InternalServerError from e

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete(self, id: int) -> bool:
        """
        Delete a model instance by its ID.

        This method attempts to delete a record from the database. The operation
        is wrapped in a transaction.

        Args:
            id (int): The unique identifier of the model instance to delete

        Returns:
            bool: True if deletion was successful, False otherwise

        Raises:
            NotFoundException: If no instance is found with the given ID
            DatabaseError: If there's an error during database operation
        """
        try:
            db_obj = await self.get_by_id(id)
            if not db_obj:
                raise NotFoundException(
                    f"{self.model_class.__tablename__.title()} with id: {id} does not exist"
                )
            delete = await self.repository.delete_by_id(id=id)
            return delete
        except DatabaseError as e:
            raise InternalServerError from e
