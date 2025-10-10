"""
constants/DEpsilon.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from utils.ConstGroup import ConstGroup


class DEpsilon(ConstGroup):
    """Epsilon Defaults"""

    EPSILON_INITIAL: float = 0.99
    EPSILON_MIN: float = 0.0
    EPSILON_DECAY: float = 0.95
