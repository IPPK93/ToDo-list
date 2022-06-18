class Task:
    def __init__(self, description: str, is_active: bool = True):
        self.description = description
        self.is_active = is_active

    def finish(self) -> None:
        self.is_active = False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        return (
            self.is_active == other.is_active and self.description == other.description
        )
