"""
constants/DModelRNN.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from utils.ConstGroup import ConstGroup


class DModelRNN(ConstGroup):
    """RNN Model Defaults"""

    LEARNING_RATE: float = 0.0007
    INPUT_SIZE: int = 400
    MAX_MEMORIES: int = 20
    MAX_MEMORY: int = 100000
