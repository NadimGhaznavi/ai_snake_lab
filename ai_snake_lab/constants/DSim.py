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

    # Random, random seed to make simulation runs repeatable
    RANDOM_SEED: int = 1970

    # Size of the statemap, this is from the GameBoard class
    STATE_SIZE: int = 19

    # The number of "choices" the snake has: go forward, left or right.
    OUTPUT_SIZE: int = 3

    # The discount (gamma) default
    DISCOUNT_RATE: float = 0.9

    # Training loop states
    PAUSED: str = "paused"
    RUNNING: str = "running"
    STOPPED: str = "stopped"

    # Stats dictionary keys
    GAME_SCORE: str = "game_score"
    GAME_NUM: str = "game_num"
