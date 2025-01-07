class GreatHelper:
    def __init__(self, name: str, default: str) -> None:
        self.name = name
        self.default = default

    def as_dict(self) -> dict[str, str]:
        return {
            'name': self.name,
            'default': self.default
        }
