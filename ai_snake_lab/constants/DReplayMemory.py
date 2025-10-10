"""
constants/DReplayMemory.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from utils.ConstGroup import ConstGroup


class MEM_TYPE(ConstGroup):
    """Replay Memory Type"""

    SHUFFLE: str = "shuffle"
    SHUFFLE_LABEL: str = "Shuffled set"
    RANDOM_GAME: str = "random_game"
    RANDOM_GAME_LABEL: str = "Random game"

    MEM_TYPE_TABLE: dict = {
        SHUFFLE: SHUFFLE_LABEL,
        RANDOM_GAME: RANDOM_GAME_LABEL,
    }
