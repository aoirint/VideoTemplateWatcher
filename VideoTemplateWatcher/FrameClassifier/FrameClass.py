from typing import Tuple, List, Dict
from dataclasses import dataclass, field

from .Template import Template
from .MatchResult import MatchResult

@dataclass
class FrameClass:
    label: str
    templates: Tuple[Template]

    def matches(self, image) -> MatchResult:
        for template in self.templates:
            res = template.matches(image=image)
            if res:
                return res

        return None

    @staticmethod
    def from_dict(self, d) -> 'FrameClass':
        tmpls = d.get('templates', [])
        templates = []
        for tmpl in tmpls:
            template = Template.from_dict(tmpl)
            templates.append(template)

        return FrameClass(
            label=d.get('label'),
            templates=templates,
        )
