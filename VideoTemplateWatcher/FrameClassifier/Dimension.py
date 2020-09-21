from typing import Tuple, List, Dict
import dataclasses as dcl

@dcl.dataclass
class Dimension:
    w: float = 0
    h: float = 0

    def scale(self, x_rate: float, y_rate: float) -> 'Dimension':
        return Dimension(
            w=self.w * x_rate,
            h=self.h * y_rate,
        )

    def as_int(self) -> 'Dimension':
        return Dimension(
            w=int(self.w),
            h=int(self.h),
        )

    def as_tuple(self) -> Tuple[float]:
        return self.w, self.h
