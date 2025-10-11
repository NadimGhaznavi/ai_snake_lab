"""
constants/DDb4EPlot.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class Plot(ConstGroup):
    """Db4EPlot Constants"""

    # Simulation loop states
    AVERAGE: str = "average"
    SLIDING: str = "sliding"
    MAX_DATA_POINTS: int = 200
