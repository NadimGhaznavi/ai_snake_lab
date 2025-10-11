"""
constants/DGameBoard.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DSim(ConstGroup):
    """Simulation Constants"""

    # Size of the statemap, this is from the GameBoard class
    STATE_SIZE: int = 30
    # The number of "choices" the snake has: go forward, left or right.
    OUTPUT_SIZE: int = 3
