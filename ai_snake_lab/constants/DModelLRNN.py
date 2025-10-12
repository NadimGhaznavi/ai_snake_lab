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
    """RNN Model constants"""

    LEARNING_RATE: float = 0.0007  # Default: Learning rate
    HIDDEN_SIZE: int = 200  # Default: The number of nodes in the hidden layer
    RNN_LAYERS: int = 4  # Default: Number of RNN layers
    P_VALUE: float = 0.18  # Default: Dropout layer value - 20%
    MODEL: str = "rnn"
    NON_LINEARITY: str = "tanh"
