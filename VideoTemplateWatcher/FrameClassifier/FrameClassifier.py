from pathlib import Path
import cv2
import numpy as np

from typing import Tuple, List, Dict
from dataclasses import dataclass, field

from .BBox import BBox
from .FrameClass import FrameClass

@dataclass
class FrameClassifier:
    classes: Tuple[FrameClass] = tuple()
    global_bbox: BBox = None

    def classify(self, image) -> FrameClass:
        bbox = self.global_bbox
        image = image[bbox.top:bbox.bottom, bbox.left:bbox.right, :]

        for clazz in self.classes:
            res = clazz.matches(image)
            if res:
                return res

        return None
