import abstract

class MockDatabaseConnection(abstract.AbstractDatabaseConnection):
    def connect(self):
        pass

    def disconnect(self):
        pass


class MockDatabaseReader(abstract.AbstractDatabaseSQLReader):
    def __getattribute__(self, name: str) -> abstract.AbstractDatabaseTable:
        pass