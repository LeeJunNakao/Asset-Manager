class DatabaseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UniqueViolationException(DatabaseException):
    def __init__(self, entity: str):
        self.entity = entity
        self.details = "Item already exist"
        super().__init__(self.details)


class InexistentItem(DatabaseException):
    def __init__(self, entity: str):
        self.entity = entity
        self.details = "Item does not exist"
        super().__init__(self.details)
