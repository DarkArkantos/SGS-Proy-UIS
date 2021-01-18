from models.activity import Activity, Optional
from models.activity_scheme import Activity_Scheme
from typing import List
from dataclasses import dataclass, field
import marshmallow_dataclass
import marshmallow.validate

@dataclass
class Instance:
    """description of class"""
    activities: List[Activity] = field(default_factory=list)
    resources: List[int] = field(default_factory=list)
