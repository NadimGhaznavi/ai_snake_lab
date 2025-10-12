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
from ai_snake_lab.constants.DModelL import DModelL
from ai_snake_lab.constants.DModelLRNN import DModelRNN


class DLabel(ConstGroup):
    """Human Readable Labels"""

    APP_TITLE: str = "AI Snake Lab"
    AVERAGE: str = "Average"
    CURRENT: str = "Current"
    CUR_EPSILON: str = "Current Epsilon"
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
    HIGHSCORES: str = "Highscores"
    LINEAR_MODEL: str = "Linear"
    MEM_TYPE: str = "Memory Type"
    MIN_EPSILON: str = "Minimum Epsilon"
    MODEL_TYPE: str = "Model Type"
    MOVE_DELAY: str = "Move Delay"
    N_SLASH_A: str = "N/A"
    PAUSE: str = "Pause"
    QUIT: str = "Quit"
    RESTART: str = "Restart"
    RNN_MODEL: str = "RNN"
    RUNTIME: str = "Runtime"
    RUNTIME_VALUES: str = "Runtime Values"
    SCORE: str = "Score"
    SETTINGS: str = "Configuration Settings"
    START: str = "Start"
    STORED_GAMES: str = "Stored Games"
    RESTART: str = "Restart"
    UPDATE: str = "Update"
