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

from game.GameElements import Direction

emptyA = "#111111"
emptyB = "#000000"
food = "#940101"
snake = "#025b02"
snake_head = "#16e116"


class GameBoard(ScrollView):
    COMPONENT_CLASSES = {
        "gameboard--emptyA-square",
        "gameboard--emptyB-square",
        "gameboard--food-square",
        "gameboard--snake-square",
        "gameboard--snake-head-square",
    }

    DEFAULT_CSS = """
    GameBoard > .gameboard--emptyA-square {
        background: #111111;
    }
    GameBoard > .gameboard--emptyB-square {
        background: #000000;
    }
    GameBoard > .gameboard--food-square {
        background: #940101;
    }
    GameBoard > .gameboard--snake-square {
        background: #025b02;
    }
    GameBoard > .gameboard--snake-head-square {
        background: #0ca30c;
    }
    """

    food = var(Offset(0, 0))
    snake_head = var(Offset(0, 0))
    snake_body = var([])
    direction = Direction.RIGHT
    last_dirs = [0, 0, 1, 0]

    def __init__(self, board_size: int, id=None) -> None:
        super().__init__(id=id)
        self._board_size = board_size
        self.virtual_size = Size(board_size * 2, board_size)

    def board_size(self) -> int:
        return self._board_size

    def get_state(self):

        head = self.snake_head
        direction = self.direction
        point_l = Offset(head.x - 1, head.y)
        point_r = Offset(head.x + 1, head.y)
        point_u = Offset(head.x, head.y - 1)
        point_d = Offset(head.x, head.y + 1)
        dir_l = direction == Direction.LEFT
        dir_r = direction == Direction.RIGHT
        dir_u = direction == Direction.UP
        dir_d = direction == Direction.DOWN

        state = [
            # 1. Snake collision straight ahead
            (dir_r and self.is_snake_collision(point_r))
            or (dir_l and self.is_snake_collision(point_l))
            or (dir_u and self.is_snake_collision(point_u))
            or (dir_d and self.is_snake_collision(point_d)),
            # 2. Snake collision to the right
            (dir_u and self.is_snake_collision(point_r))
            or (dir_d and self.is_snake_collision(point_l))
            or (dir_l and self.is_snake_collision(point_u))
            or (dir_r and self.is_snake_collision(point_d)),
            # 3. Snake collision to the left
            (dir_d and self.is_snake_collision(point_r))
            or (dir_u and self.is_snake_collision(point_l))
            or (dir_r and self.is_snake_collision(point_u))
            or (dir_l and self.is_snake_collision(point_d)),
            # 4. divider
            0,
            # 5. Wall collision straight ahead
            (dir_r and self.is_wall_collision(point_r))
            or (dir_l and self.is_wall_collision(point_l))
            or (dir_u and self.is_wall_collision(point_u))
            or (dir_d and self.is_wall_collision(point_d)),
            # 6. Wall collision to the right
            (dir_u and self.is_wall_collision(point_r))
            or (dir_d and self.is_wall_collision(point_l))
            or (dir_l and self.is_wall_collision(point_u))
            or (dir_r and self.is_wall_collision(point_d)),
            # 7. Wall collision to the left
            (dir_d and self.is_wall_collision(point_r))
            or (dir_u and self.is_wall_collision(point_l))
            or (dir_r and self.is_wall_collision(point_u))
            or (dir_l and self.is_wall_collision(point_d)),
            # 8. divider
            0,
            # 9, 10, 11, 12. Last move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            # 13. divider
            0,
            # 14 - 23. Food location
            self.food.x < self.snake_head.x,  # Food left
            self.food.x > self.snake_head.x,  # Food right
            self.food.y < self.snake_head.y,  # Food up
            self.food.y > self.snake_head.y,  # Food down
            self.food.x == self.snake_head.x,
            self.food.x == self.snake_head.x
            and self.food.y > self.snake_head.y,  # Food ahead
            self.food.x == self.snake_head.x
            and self.food.y < self.snake_head.y,  # Food behind
            self.food.y == self.snake_head.y,
            self.food.y == self.snake_head.y
            and self.food.x > self.snake_head.x,  # Food above
            self.food.y == self.snake_head.y
            and self.food.x < self.snake_head.x,  # Food below
        ]

        # 24, 25, 26 and 27. Previous direction of the snake
        for aDir in self.last_dirs:
            state.append(int(aDir))
        self.last_dirs = [dir_l, dir_r, dir_u, dir_d]

        return np.array(state, dtype="int8")

    def is_snake_collision(self, pt: Offset) -> bool:
        if pt in self.snake_body:
            return True
        return False

    def is_wall_collision(self, pt: Offset) -> bool:
        if pt.x >= self._board_size or pt.x < 0 or pt.y >= self._board_size or pt.y < 0:
            return True
        return False

    def render_line(self, y: int) -> Strip:
        scroll_x, scroll_y = self.scroll_offset
        y += scroll_y
        row_index = y

        emptyA = self.get_component_rich_style("gameboard--emptyA-square")
        emptyB = self.get_component_rich_style("gameboard--emptyB-square")
        food = self.get_component_rich_style("gameboard--food-square")
        snake = self.get_component_rich_style("gameboard--snake-square")
        snake_head = self.get_component_rich_style("gameboard--snake-head-square")

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

    def watch_food(self, previous_food: Offset, food: Offset) -> None:
        """Called when the food square changes."""

        def get_square_region(square_offset: Offset) -> Region:
            """Get region relative to widget from square coordinate."""
            x, y = square_offset
            region = Region(x * 2, y, 2, 1)
            # Move the region into the widgets frame of reference
            region = region.translate(-self.scroll_offset)
            return region

        # Refresh the previous food square
        self.refresh(get_square_region(previous_food))

        # Refresh the new food square
        self.refresh(get_square_region(food))

    def update_food(self, food: Offset) -> None:
        self.food = food
        self.refresh()

    def update_snake(self, snake: list[Offset], direction: Direction) -> None:
        self.direction = direction
        self.snake_head = snake[0]
        self.snake_body = snake[1:]
        self.refresh()
