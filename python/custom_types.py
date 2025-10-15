# pylint: disable=missing-docstring

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        # Enforce that other is also a Coord and compare x and y values
        # This is basically operator overloading
        x_eq = self.x == other.x
        y_eq = self.y == other.y
        return isinstance(other, Coord) and x_eq and y_eq
    def __hash__(self):
        # Allow Coord objects to be used as dictionary keys and stored in sets
        return hash((self.x, self.y))

class FrontierObj:
    def __init__(self, f: float, seq: int, g: float, pos: Coord):
        self.f = f
        self.seq = seq
        self.g = g
        self.pos = Coord(pos.x,pos.y)
    def __lt__(self, other):
        # Enforce min-heap comparison and tie-breaker
        return (self.f, self.seq, self.g) < (other.f, other.seq, other.g)

class FrontierObjMod:
    def __init__(self, f: float, seq: int, g: float, pos: Coord):
        self.f = f
        self.seq = seq
        self.g = g
        self.pos = Coord(pos.x,pos.y)
    def __lt__(self, other):
        # Enforce min-heap comparison and tie-breaker
        return (self.f, -self.g, self.seq) < (other.f, -other.g, other.seq)

class Result:
    def __init__(self):
        self.path: list = []
        self.rim: set = set()
        self.cloud: set = set()
