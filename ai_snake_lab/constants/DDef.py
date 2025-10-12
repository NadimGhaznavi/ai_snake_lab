"""
constants/DDef.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DDef(ConstGroup):
    """Defaults"""

    DOT_DB: str = ".db"  # .db files
    MOVE_DELAY: float = 0.0  # Delay between game moves (in the training loop)
