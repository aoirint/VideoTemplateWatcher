
from typing import Tuple, List, Dict, NamedTuple
from dataclasses import dataclass, field

from .BBox import BBox

class MatchResult(NamedTuple):
    bbox: BBox
    value: float
