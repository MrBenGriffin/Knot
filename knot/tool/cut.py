# encoding: utf-8
from enum import Enum
from ..space.rectilinear import Square, Rectangle
from .tool import CutDecorator


@CutDecorator(
    {'O': 'O', 'I': 'I', 'X': 'X', 'H': 'B'},
    {'O': 0, 'I': 2, 'X': 1, 'H': 3, 'B': 4},
    {
        Rectangle().com(): {'N': 3, 'E': 2, 'S': 1, 'W': 0},
        Square().com(): {'N': 3, 'E': 2, 'S': 1, 'W': 0}
    }

)
class Cut(Enum):
    O = 1
    I = 2
    X = 3
    H = 4
    B = 5

    def __str__(self):
        text = {1: "O", 2: "I", 3: "X", 4: "H", 5: "B"}
        return text[self._value_]
