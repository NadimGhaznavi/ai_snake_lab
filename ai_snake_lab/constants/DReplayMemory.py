"""
constants/DReplayMemory.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class MEM_TYPE(ConstGroup):
    """Replay memory constants"""

    NONE: str = "none"
    NONE_LABEL: str = "None"
    RANDOM_GAME: str = "random_game"
    RANDOM_GAME_LABEL: str = "Random Game"
    SHUFFLE: str = "shuffle"
    SHUFFLE_LABEL: str = "Random Frames"

    MEM_TYPE_TABLE: dict = {
        NONE: NONE_LABEL,
        RANDOM_GAME: RANDOM_GAME_LABEL,
        SHUFFLE: SHUFFLE_LABEL,
    }

    MEMORY_TYPES: list = [
        (NONE_LABEL, NONE),
        (RANDOM_GAME_LABEL, RANDOM_GAME),
        (SHUFFLE_LABEL, SHUFFLE),
    ]


class MEM(ConstGroup):
    """Replay memory constants"""

    MIN_GAMES: int = 20
    NO_DATA: int = -1
