class ServiceExceptions(Exception):
    def __init__(self, entity: str, message: str, status_code: int = 400):
        self.entity = entity
        self.details = message
        self.status_code = status_code
        super().__init__(message)


class FailedToCreate(ServiceExceptions):
    def __init__(self, entity):
        super().__init__(entity,  f"Failed to create {entity}")


class FailedToFind(ServiceExceptions):
    def __init__(self, entity):
        super().__init__(entity, f"Failed to find {entity}")


class FailedToUpdate(ServiceExceptions):
    def __init__(self, entity):
        super().__init__(entity, f"Failed to update {entity}")


class FailedToDelete(ServiceExceptions):
    def __init__(self, entity):
        super().__init__(entity, f"Failed to delete {entity}")
