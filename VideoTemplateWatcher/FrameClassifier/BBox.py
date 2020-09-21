from typing import Tuple, List, Dict
import dataclasses as dcl

@dcl.dataclass
class BBox:
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0

    left: float = dcl.field(init=False)
    top: float = dcl.field(init=False)
    right: float = dcl.field(init=False)
    bottom: float = dcl.field(init=False)
    size: Tuple[float] = dcl.field(init=False)

    def __post_init__(self):
        self.left = self.x
        self.top = self.y
        self.right = self.x + self.w
        self.bottom = self.y + self.h
        self.size = (self.w, self.h)

    def offset(self, x: float, y: float) -> 'BBox':
        return BBox(
            x=self.x + x,
            y=self.y + y,
            w=self.w,
            h=self.h,
        )

    def scale(self, x_rate: float, y_rate: float) -> 'BBox':
        return BBox(
            x=self.x * x_rate,
            y=self.y * y_rate,
            w=self.w * x_rate,
            h=self.h * y_rate,
        )

    def as_int(self) -> 'BBox':
        return BBox(
            x=int(self.x),
            y=int(self.y),
            w=int(self.w),
            h=int(self.h),
        )
