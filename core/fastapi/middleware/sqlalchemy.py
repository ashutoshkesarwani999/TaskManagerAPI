from uuid import uuid4
from starlette.types import ASGIApp, Receive, Scope, Send
from core.database.session import reset_session_context, session, set_session_context


class SQLAlchemyMiddleware:
    """
    ASGI middleware for managing SQLAlchemy database sessions.It creates a unique session
    context for each request and cleans up resources after the request is completed.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Process an incoming request with database session management.
        Creates a new session context for each request, executes the request,
        and ensures proper cleanup of database resources regardless of request
        success or failure.

        Args:
            scope (Scope): The ASGI connection scope
            receive (Receive): The ASGI receive function
            send (Send): The ASGI send function

        Raises:
            Exception: Re-raises any exceptions that occur during request processing
        """
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as exception:
            raise exception
        finally:
            await session.remove()
            reset_session_context(context=context)
