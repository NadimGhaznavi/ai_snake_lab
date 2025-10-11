"""
constants/DLabels.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.ai.models.ModelL import ModelL
from ai_snake_lab.ai.models.ModelRNN import ModelRNN

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DLabel(ConstGroup):
    """Labels"""

    AVERAGE: str = "Average"
    CURRENT: str = "Current"
    CURRENT_EPSILON: str = "Current Epsilon"
    DEFAULTS: str = "Defaults"
    EPSILON: str = "Epsilon"
    EPSILON_DECAY: str = "Epsilon Decay"
    EPSILON_INITIAL: str = "Initial Epsilon"
    EPSILON_MIN: str = "Minimum Epsilon"
    GAME: str = "Game"
    GAMES: str = "Games"
    GAME_SCORE: str = "Game Score"
    GAME_NUM: str = "Game Number"
    HIGHSCORE: str = "Highscore"
    MEM_TYPE: str = "Memory Type"
    MIN_EPSILON: str = "Minimum Epsilon"
    MODEL_LINEAR: str = "Linear"
    MODEL_RNN: str = "RNN"
    MODEL_TYPE: str = "Model Type"
    MOVE_DELAY: str = "Move Delay"
    PAUSE: str = "Pause"
    QUIT: str = "Quit"
    RESTART: str = "Restart"
    RUNTIME: str = "Runtime"
    RUNTIME_VALUES: str = "Runtime Values"
    SCORE: str = "Score"
    SETTINGS: str = "Configuration Settings"
    START: str = "Start"
    STORED_GAMES: str = "Stored Games"
    RESTART: str = "Restart"
    UPDATE: str = "Update"

    MODEL_TYPE_TABLE: dict = {
        str(ModelL): MODEL_LINEAR,
        ModelRNN: MODEL_RNN,
    }
