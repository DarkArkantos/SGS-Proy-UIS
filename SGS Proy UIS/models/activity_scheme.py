from typing import List
from dataclasses import dataclass, field
import marshmallow_dataclass
@dataclass
class Activity_Scheme():
    Index: int
    Duration: int
    Precedence: List[int] = field(default_factory=list)
    Resources: List[int] = field(default_factory=list)


