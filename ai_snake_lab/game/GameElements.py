"""
game/GameElements.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from enum import Enum


class Direction(Enum):
    """
    A simple Enum class that represents a direction in the
    Snake game. It has four values:
    1. RIGHT
    2. LEFT
    3. UP
    4. DOWN
    """

    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
