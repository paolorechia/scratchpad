"""Mock implementations of the database interfaces.

Useful to test that the interfaces make sense (at least in principle).
"""
import abstract
from typing import Iterable, Optional, Any
from dataclasses import dataclass


@dataclass
class MockDatabaseAttribute:
    name: str
    type_: Optional[type]
    required: bool
    value: Optional[Any]


class MockDatabaseExpression(abstract.AbstractDatabaseExpression):
    pass


class MockDatabaseTable(abstract.AbstractDatabaseTable):
    def __init__(self, table_name: str, attrs: Iterable[MockDatabaseAttribute]):
        self.name = table_name
        self.__mock_items = {attr.name: [] for attr in attrs}
        self.__mock_types = {attr.name: attr.type_ for attr in attrs}
        self.__mock_required = {attr.required: attr.required for attr in attrs}

    def __getitem__(self, expr: MockDatabaseExpression):
        if isinstance(expr, str):
            return self.__mock_items[expr]

        if isinstance(expr, MockDatabaseAttribute):
            return self.__mock_items[expr.name]

        if isinstance(expr, Iterable):
            response = []
            for attr in expr:
                if isinstance(attr, str):
                    response.append(self.__mock_items[attr])
                if isinstance(attr, MockDatabaseAttribute):
                    response.append(self.__mock_items[attr.name])
                else:
                    raise TypeError(f"Cannot retrieve item of type '{type(attr)}'")

        raise TypeError(f"Cannot retrieve item of type '{type(expr)}'")

    def __setattr__(self, attrs: Iterable[MockDatabaseAttribute] ) -> None:
        """"Need to figure out a good way to set attributes"""
        passed_keys = set()
        for attr in attrs:
            if attr.name not in self.__mock_items:
                raise TypeError(f"Table '{self.name}' does not contain column '{attr.name}'")
            if attr.name in passed_keys:
                raise TypeError(f"Duplicate key found for '{attr.name}'")
            if not attr.value and self.__mock_required[attr.name]:
                raise TypeError(f"Column '{attr.name}' cannot be 'None'")
            if type(attr.value) != self.__mock_types[attr.name]:
                raise TypeError(
                    f"Column '{attr.name}' must be of type '{self.__mock_types[attr.name]}' -" 
                    f" Found '{attr.type_}'"
                )
            passed_keys.add(attr.name)
        missing_keys = self.__mock_required.keys() - passed_keys
        if len(missing_keys) > 0:
            raise TypeError(
                f"Missing required keys: {','.join(list(sorted(list(missing_keys))))}"
            )
        empty_keys = self.__mock_items.keys() - passed_keys

        # Time to insert into our 'database' :)
        for attr in attrs:
            self.__mock_items[attr.name].append(attr.value)
        
        for key in empty_keys:
            self.__mock_items[key] = None


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

    def create_table(self, table: MockDatabaseTable):
        self.__mock_database[table.name] = table


class MockDatabaseReader(abstract.AbstractDatabaseQuerier):
    def __init__(self, db_conn: MockDatabaseConnection):
        self.db_conn = db_conn

    def __getattribute__(self, name: str) -> MockDatabaseTable:
        tables = self.db_conn.get_tables()
        if name in tables:
            return tables[name]
        raise AttributeError(f"Database table '{name}' not found")
