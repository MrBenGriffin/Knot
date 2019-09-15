import typing
from knot.space.crs import Wallpaper, WallpaperDecorator, Symmetry
from .rectilinear import Rectilinear
from .axes import Com
from .dim import Dim
from .tweak import Tweak as RTweak


@WallpaperDecorator(
    {'master': 1, 'sunset': 2, 'vanity': 2, 'mirror': 2, 'rotate': 4},
    {'master': None, 'sunset': Symmetry.H, 'vanity': Symmetry.V, 'mirror': None, 'rotate': None},
)
class Paper(Wallpaper):
    master = 1
    sunset = 2
    vanity = 3
    mirror = 4
    rotate = 5

    @staticmethod
    def select(val: str):
        sel = {'N': Paper.master, 'H': Paper.sunset, 'V': Paper.vanity, 'F': Paper.mirror, 'R': Paper.rotate}
        return sel[val]

    @classmethod
    def identity(cls):
        return Paper.master

    def __str__(self):
        text = {Paper.master: "Master", Paper.sunset: "Sunset",
                Paper.vanity: "Vanity", Paper.mirror: "Mirror", Paper.rotate: "Rotate"}
        return text[self]


class Tweak(RTweak):

    def face(self, com: Com) -> [Com, None]:
        if com is None:
            return None
        if self.worker_no == 0:
            return com
        if self.worker_no == 1:
            if self.paper == Paper.rotate:
                return com.cw
            if self.paper == Paper.mirror or self.paper.symmetry == com.axis.perp:
                return com.opposite
            return com
        if self.paper == Paper.rotate and self.worker_no == 2:
            return com.opposite
        if self.paper == Paper.rotate and self.worker_no == 3:
            return com.ccw
        return None

    def dim_mirror(self, basis: Dim) -> Dim:
        w1 = {
            Paper.sunset: Dim(basis.x, self._dim.y - basis.y),
            Paper.vanity: Dim(self._dim.x - basis.x, basis.y),
            Paper.mirror: Dim(self._dim.x - basis.x, self._dim.y - basis.y),
            Paper.rotate: Dim(self._dim.x - basis.x, self._dim.y - basis.y),
        }
        return w1[self.paper]

    def dim(self, basis: Dim) -> Dim:
        if self.worker_no == 0:
            return basis
        if self.paper == Paper.rotate:
            if self.worker_no == 1:
                # X = x cos(Theta) + y sin(theta), Y= y cos(theta) - x sin(theta)
                # sin(90) = 1; cos(90) = 0; sin(-90) = -1; cos(-90) = 0
                # so X = +y, Y= -x
                # However, the centre of the rotation is at the centre of _dim.
                # because otherwise (0,0) --> (0,0)
                # eg on a 2x2 grid,
                return Dim(basis.y, self._dim.x - basis.x)
            if self.worker_no == 3:
                return Dim(self._dim.y - basis.y, basis.x)
                # return Dim(self._dim.y - basis.y, self._dim.x - basis.x)
        return self.dim_mirror(basis)


class Square(Rectilinear):

    def tweak(self) -> typing.Type[Tweak]:
        return Tweak

    def paper(self) -> typing.Type[Wallpaper]:
        return Paper

