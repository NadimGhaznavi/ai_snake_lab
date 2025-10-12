"""
constants/DModelRNN.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DModelRNN(ConstGroup):
    """RNN Model Defaults"""

    LEARNING_RATE: float = 0.0007
    HIDDEN_SIZE: int = 200
    RNN_LAYERS: int = 4
    RNN_DROPOUT: float = 0.2
