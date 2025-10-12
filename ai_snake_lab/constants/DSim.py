"""
constants/DGameBoard.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup

from ai_snake_lab.constants.DLabels import DLabel
from ai_snake_lab.constants.DModelL import DModelL
from ai_snake_lab.constants.DModelLRNN import DModelRNN


class DSim(ConstGroup):
    """Simulation Constants"""

    # Random, random seed to make simulation runs repeatable
    RANDOM_SEED: int = 1970

    # Size of the statemap, this is from the GameBoard class
    STATE_SIZE: int = 27

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

    # A list of tuples, for the TUI's model selection drop down menu (Select widget).
    MODEL_TYPES: list = [
        (DLabel.LINEAR_MODEL.value, DModelL.MODEL.value),
        (DLabel.RNN_MODEL.value, DModelRNN.MODEL.value),
    ]

    # A dictionary of model_field to model_name values, for the TUI's runtime model
    # widget (Label widget).
    MODEL_TYPE: dict = {
        DModelL.MODEL.value: DLabel.LINEAR_MODEL.value,
        DModelRNN.MODEL.value: DLabel.RNN_MODEL.value,
    }
