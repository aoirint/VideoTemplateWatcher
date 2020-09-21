from typing import NamedTuple

from .MatchResult import MatchResult

class FrameClassResult(NamedTuple):
    label: str
    match: MatchResult
