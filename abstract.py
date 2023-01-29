"""
The example module supplies abstract classes that can be used
to build concrete implementations of database connections and
database readers.
"""

from typing import Optional
import abc

class AbstractDatabaseConnection:
    def __init__(self) -> None:
        self.connected = False

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def disconnect(self):
        raise NotImplementedError()

    def __enter__(self):
        if not self.connected:
            self.connected = True
            self.db_conn.connect()

    def __exit__(self, *args, **kwargs):
        if self.connected:
            self.connected = False
            self.db_conn.disconnect()


class AbstractDatabaseExpression:
    @abc.abstractclassmethod
    def __getitem__(self, expr: Optional["AbstractDatabaseExpression"]):
        raise NotImplementedError()


class AbstractDatabaseTable:
    @abc.abstractclassmethod
    def __getitem__(self, expr: AbstractDatabaseExpression):
        raise NotImplementedError()


class AbstractDatabaseSQLReader:
    def __init__(self, db_conn: AbstractDatabaseConnection):
        self.db_conn = db_conn

    @abc.abstractclassmethod
    def __getattribute__(self, name: str) -> AbstractDatabaseTable:
        raise NotImplementedError()

    def __enter__(self):
        with self.db_conn:
            yield

    def __exit__(self, *args, **kwargs):
        pass