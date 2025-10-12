"""
constants/DModelL.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class DModelL(ConstGroup):
    """Linear Model constants"""

    HIDDEN_SIZE: int = 170  # Default: The number of nodes in the hidden layer
    LEARNING_RATE: float = 0.000009  # Default: Learning rate
    MODEL: str = "linear"
    P_VALUE: float = 0.2  # Default: Dropout layer value - 20%
