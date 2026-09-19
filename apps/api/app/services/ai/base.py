from dataclasses import dataclass
from typing  import Protocol

@dataclass
class CitizenUnderstanding:
    language: str | None
    category: str | None
    intent: str | None
    issue: str | None
    location_text: str | None

class AIProvider(Protocol):
    def understand(
        self,
        text: str,
    ) -> CitizenUnderstanding:
        raise NotImplementedError()