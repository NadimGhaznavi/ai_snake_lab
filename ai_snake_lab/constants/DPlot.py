"""
constants/DPlot.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

from ai_snake_lab.utils.ConstGroup import ConstGroup


class Plot(ConstGroup):
    """Ploting constants"""

    # Method used to thin data that's being plotted, otherwise the plot gets "blurry"
    AVERAGE: str = "average"
    SLIDING: str = "sliding"

    MAX_DATA_POINTS: int = 100  # Maximum number of data points in a plot
