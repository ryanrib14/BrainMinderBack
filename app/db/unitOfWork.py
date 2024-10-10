from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, Any
from sqlalchemy.orm import Session


class UnitOfWorkBase(ABC):
    @abstractmethod
    def __enter__(self) -> Any:
        # Subclasses will handle their specific entering logic
        pass

    @abstractmethod
    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        # Subclasses will handle their specific exit logic, including committing or rolling back transactions
        pass

    @abstractmethod
    def commit(self) -> None:
        # Subclasses must implement how to commit transactions
        pass

    @abstractmethod
    def rollback(self) -> None:
        # Subclasses must implement how to rollback transactions
        pass

    @abstractmethod
    def close_session(self) -> None:
        # Subclasses must implement how to close their sessions
        pass


class UnitOfWork(UnitOfWorkBase):
    def __init__(
        self,
        session_factory: Callable[[], Session],
        repo_factories: Dict[str, Callable[[Session], object]],
    ) -> None:
        self._session_factory = session_factory
        self._session: Optional[Session] = None
        self._repo_factories = repo_factories

    def __enter__(self) -> Any:
        self._session = self._session_factory()
        for repo_name, factory in self._repo_factories.items():
            setattr(self, repo_name, factory(self._session))
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        super().__exit__(exc_type, exc_value, traceback)
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            self.close_session()

    def commit(self) -> None:
        if self._session:
            self._session.commit()

    def rollback(self) -> None:
        if self._session:
            self._session.rollback()

    def close_session(self) -> None:
        if self._session:
            self._session.close()
            self._session = None  # Ensure the session is dereferenced
