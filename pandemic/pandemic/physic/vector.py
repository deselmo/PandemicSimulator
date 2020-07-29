from __future__ import annotations
import math


class Vector:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    """ vector addition - vector1+vector2"""
    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x+other.x, self.y+other.y)

    """ vector subtraction - vector1-vector2 """
    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x-other.x, self.y-other.y)

    """ vector multiplication - vector*k """
    def __mul__(self, other: float) -> Vector:
        return Vector(self.x*other, self.y*other)

    """ vector division - vector/k"""
    def __truediv__(self, other: float) -> Vector:
        return Vector(self.x/other, self.y/other)

    """ vector negation - -vector"""
    def __neg__(self) -> Vector:
        return self * -1

    """ vector length"""
    def length(self) -> float:
        return self.x*self.x + self.y*self.y

    """ vector module - abs(vector) """
    def __abs__(self) -> float:
        return math.sqrt(self.length())

    """ vector normalization - +vector """
    def __pos__(self) -> Vector:
        return self / abs(self)

    """ vector comparison - vector1 == vector2 """
    def __eq__(self, other: Vector):
        return self.x == other.x and self.y == other.y

    """ vector comparison - vector1 != vector2 """
    def __ne__(self, other: Vector):
        return self.x != other.x or self.y != other.y

    """ vector string representation - repr(vector) """
    def __repr__(self) -> str:
        return '({},{})'.format(self.x, self.y)

    """ vector string conversion - str(vector) """
    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def rad(rad: float) -> Vector:
        return Vector(math.cos(rad), math.sin(rad))
