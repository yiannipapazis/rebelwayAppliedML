from dataclasses import dataclass, field, replace
from library.random_number_utils import RandomUtils

@dataclass(frozen=True, order=True, slots=True)
class Book:
    name: str
    author: str
    type: str
    pages: int

    @property
    def search_string(self):
        return f"{self.name} {self.author} {self.type}"
