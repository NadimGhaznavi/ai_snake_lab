"""
game/AISim.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import numpy as np

from textual.scroll_view import ScrollView
from textual.geometry import Offset, Region, Size
from textual.strip import Strip
from textual.reactive import var

from rich.segment import Segment
from rich.style import Style

from ai_snake_lab.game.GameElements import Direction

emptyA = "#111111"
emptyB = "#000000"
food = "#940101"
snake = "#025b02"
snake_head = "#16e116"


class ClientGameBoard(ScrollView):
    COMPONENT_CLASSES = {
        "clientgameboard--emptyA-square",
        "clientgameboard--emptyB-square",
        "clientgameboard--food-square",
        "clientgameboard--snake-square",
        "clientgameboard--snake-head-square",
    }

    DEFAULT_CSS = """
    ClientGameBoard > .clientgameboard--emptyA-square {
        background: #111111;
    }
    ClientGameBoard > .clientgameboard--emptyB-square {
        background: #000000;
    }
    ClientGameBoard > .clientgameboard--food-square {
        background: #940101;
    }
    ClientGameBoard > .clientgameboard--snake-square {
        background: #025b02;
    }
    ClientGameBoard > .clientgameboard--snake-head-square {
        background: #0ca30c;
    }
    """

    food = var(Offset(3, 3))
    snake_head = var(Offset(0, 0))
    snake_body = var([])
    direction = Direction.RIGHT
    last_dirs = [0, 0, 1, 0]

    def __init__(self, board_size: int, id=None) -> None:
        super().__init__(id=id)
        self._board_size = board_size
        self.virtual_size = Size(board_size * 2, board_size)
        snake_head = Offset(board_size // 2, board_size // 2)
        snake = [
            snake_head,
            Offset(snake_head.x - 1, snake_head.y),
            Offset(snake_head.x - 2, snake_head.y),
        ]
        self.update_snake(snake=snake, direction=Direction.RIGHT)

    def board_size(self) -> int:
        return self._board_size

    def render_line(self, y: int) -> Strip:
        scroll_x, scroll_y = self.scroll_offset
        y += scroll_y
        row_index = y

        emptyA = self.get_component_rich_style("clientgameboard--emptyA-square")
        emptyB = self.get_component_rich_style("clientgameboard--emptyB-square")
        food = self.get_component_rich_style("clientgameboard--food-square")
        snake = self.get_component_rich_style("clientgameboard--snake-square")
        snake_head = self.get_component_rich_style("clientgameboard--snake-head-square")

        if row_index >= self._board_size:
            return Strip.blank(self.size.width)

        is_odd = row_index % 2

        def get_square_style(column: int, row: int) -> Style:
            if self.food == Offset(column, row):
                square_style = food
            elif self.snake_head == Offset(column, row):
                square_style = snake_head
            elif Offset(column, row) in self.snake_body:
                square_style = snake
            else:
                square_style = emptyA if (column + is_odd) % 2 else emptyB
            return square_style

        segments = [
            Segment(" " * 2, get_square_style(column, row_index))
            for column in range(self._board_size)
        ]
        strip = Strip(segments, self._board_size * 2)
        # Crop the strip so that is covers the visible area
        strip = strip.crop(scroll_x, scroll_x + self.size.width)
        return strip

    def update_food(self, food: Offset) -> None:
        self.food = food
        self.refresh()
        # self.render_line()

    def update_snake(self, snake: list[Offset], direction: Direction) -> None:
        self.direction = direction
        self.snake_head = snake[0]
        self.snake_body = snake[1:]
        self.refresh()
        # self.render_line()
