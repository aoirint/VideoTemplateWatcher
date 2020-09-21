from pathlib import Path
import cv2
import numpy as np

from typing import Tuple, List, Dict
import dataclasses as dcl

from .BBox import BBox
from .Dimension import Dimension
from .MatchResult import MatchResult

@dcl.dataclass
class Template:
    file: Path
    bbox: BBox = None
    expected_scale: Dimension = None
    threshold: float = 0.95
    template: np.ndarray = dcl.field(init=False)

    def __post_init__(self):
        self.template = cv2.imread(str(self.file), 0)
        assert self.template is not None

    def matches(self, image) -> MatchResult:
        template = self.template
        bbox = self.bbox
        threshold = self.threshold

        tbbox = BBox(x=0, y=0, w=template.shape[1], h=template.shape[0])
        if bbox:
            tbbox = BBox(x=bbox.x, y=bbox.y, w=tbbox.w, h=tbbox.h)

        if self.expected_scale:
            ih, iw = image.shape[:2]
            ew, eh = self.expected_scale.as_tuple()

            if ih != eh or iw != ew:
                tbbox = tbbox.scale(iw / ew, ih / eh).as_int()
                template = cv2.resize(template, (tbbox.w, tbbox.h))
                if bbox:
                    bbox = bbox.scale(iw / ew, ih / eh).as_int()

        if bbox:
            image = image[bbox.top:bbox.bottom, bbox.left:bbox.right, :]

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < self.threshold:
            return None

        return MatchResult(
            bbox=BBox(x=max_loc[0], y=max_loc[1], w=tbbox.w, h=tbbox.h).offset(x=tbbox.x, y=tbbox.y),
            value=max_val,
        )

    @staticmethod
    def from_dict(self, d) -> 'Template':
        bbox = d.get('bbox')
        bbox = BBox(**bbox) if bbox else None

        return Template(
            bbox=bbox,
        )
