"""
constants/DFields.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DField(ConstGroup):
    """Fields"""

    # Simulation loop states
    PAUSED: str = "paused"
    RUNNING: str = "running"
    STOPPED: str = "stopped"

    # Stats dictionary keys
    GAME_SCORE: str = "game_score"
    GAME_NUM: str = "game_num"
