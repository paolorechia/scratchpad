"""Mock implementations of the database interfaces.

Useful to test that the interfaces make sense (at least in principle).
"""
import abstract
from typing import Iterable




class MockDatabaseExpression(abstract.AbstractDatabaseExpression):
    pass


class MockDatabaseTable(abstract.AbstractDatabaseTable):
    def __init__(self):
        self.__mock_items = {}

    def __getitem__(self, expr: MockDatabaseExpression):
        if isinstance(expr, str):
            return self.__mock_items[expr]

        if isinstance(expr, Iterable):
            return [self.__mock_items[i] for i in expr]
        


class MockDatabaseConnection(abstract.AbstractDatabaseConnection):
    """Nothing to connect to :)"""

    def __init__(self):
        self.__mock_database = {}

    def connect(self):
        pass

    def disconnect(self):
        pass

    def get_tables(self) -> Iterable[MockDatabaseTable]:
        return self.__mock_database.keys()


class MockDatabaseReader(abstract.AbstractDatabaseQuerier):
    def __init__(self, db_conn: MockDatabaseConnection):
        self.db_conn = db_conn

    def __getattribute__(self, name: str) -> MockDatabaseTable:
        tables = self.db_conn.get_tables()
        if name in tables:
            return tables[name]
        raise AttributeError(f"Database table '{name}' not found")