"""
constants/DLayout.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from utils.ConstGroup import ConstGroup


class DLayout(ConstGroup):
    """Layout"""

    BUTTON_PAUSE: str = "button_pause"
    BUTTON_QUIT: str = "button_quit"
    BUTTON_ROW: str = "button_row"
    BUTTON_START: str = "button_start"
    BUTTON_RESET: str = "button_reset"
    BUTTON_UPDATE: str = "button_update"
    CUR_EPSILON: str = "cur_epsilon"
    CUR_MEM_TYPE: str = "cur_mem_type"
    GAME_BOARD: str = "game_board"
    GAME_BOX: str = "game_box"
    EPSILON_DECAY: str = "epsilon_decay"
    EPSILON_INITIAL: str = "initial_epsilon"
    EPSILON_MIN: str = "epsilon_min"
    INPUT_10: str = "input_10"
    LABEL: str = "label"
    LABEL_SETTINGS: str = "label_settings"
    MOVE_DELAY: str = "move_delay"
    NUM_MEMORIES: str = "num_memories"
    RUNTIME_BOX: str = "runtime_box"
    SCORE: str = "score"
    SETTINGS_BOX: str = "settings_box"
    TITLE: str = "title"
    VARIABLE: str = "variable"
