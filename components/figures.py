from typing import Tuple
import pygame as pg

class Figure:
    BLUE = (0, 168, 255)
    RED = (255, 118, 117)

    def __init__(
        self, 
        pos: Tuple[int] | Tuple[Tuple[Tuple[int]]], 
        thickness: int = 15, 
        color: Tuple[int] = (255, 255, 255)
    ) -> None:
        self.pos = pos
        self.thickness = thickness
        self.color = color

    def draw(self, screen: pg.Surface) -> None:
        pass


class Cross(Figure):
    def __init__(self, pos: Tuple[Tuple[Tuple[int]]], thickness: int = 20) -> None:
        super().__init__(pos, thickness, Figure.BLUE)

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.line(screen, self.color, self.pos[0][0], self.pos[0][1], self.thickness)
        pg.draw.line(screen, self.color, self.pos[1][0], self.pos[1][1], self.thickness)


class Circle(Figure):
    def __init__(self, pos: Tuple[int], radius: int = 10, thickness: int = 15) -> None:
        self.radius = radius
        super().__init__(pos, thickness, Figure.RED)

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.circle(screen, self.color, self.pos, self.radius, self.thickness)
    