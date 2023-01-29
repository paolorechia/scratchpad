"""
The example module supplies abstract classes that can be used
to build concrete implementations of database connections and
database readers.
"""

from typing import Optional, Iterable
import abc

class AbstractDatabaseExpression:
    @abc.abstractclassmethod
    def __getitem__(self, expr: Optional["AbstractDatabaseExpression"]):
        raise NotImplementedError()


class AbstractDatabaseTable:
    @abc.abstractclassmethod
    def __getitem__(self, expr: AbstractDatabaseExpression):
        raise NotImplementedError()


class AbstractDatabaseConnection:
    def __init__(self) -> None:
        self.connected = False
        self._tables = set()

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def disconnect(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_tables(self) -> Iterable[AbstractDatabaseTable]:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def create_table(self, table: AbstractDatabaseTable):
        raise NotImplementedError()

    def __enter__(self):
        if not self.connected:
            self.connected = True
            self.connect()

    def __exit__(self, *args, **kwargs):
        if self.connected:
            self.connected = False
            self.disconnect()



class AbstractDatabaseQuerier:
    def __init__(self, db_conn: AbstractDatabaseConnection):
        self.db_conn = db_conn

    @abc.abstractclassmethod
    def __getattribute__(self, name: str) -> AbstractDatabaseTable:
        """Fetches a table from the Database."""
        raise NotImplementedError()

    @abc.abstractclassmethod
    def __setattr__(self, name: str, table: AbstractDatabaseTable) -> None:
        """Creates a table into the Database."""
        raise NotImplementedError()

    def __enter__(self):
        with self.db_conn:
            yield

    def __exit__(self, *args, **kwargs):
        pass