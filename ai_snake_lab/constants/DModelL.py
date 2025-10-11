"""
constants/DModelL.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from utils.ConstGroup import ConstGroup


class DModelL(ConstGroup):
    """Linear Model Defaults"""

    LEARNING_RATE: float = 0.000009
    # The number of nodes in the hidden layer
    HIDDEN_SIZE: int = 170
    # The dropout value, 0.2 represents 20%
    P_VALUE: float = 0.2
