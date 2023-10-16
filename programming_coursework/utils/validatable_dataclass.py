from dataclasses import dataclass, fields

__all__ = ["ValidatableDataClass"]


@dataclass(frozen=True)
class ValidatableDataClass:
    def __post_init__(self):
        for field in fields(self):
            if not isinstance(getattr(self, field.name), field.type):
                raise TypeError(f"Field {field.name} must be of type {field.type}")
