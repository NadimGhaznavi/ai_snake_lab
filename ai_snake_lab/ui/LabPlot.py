"""
db4e/Modules/LabPlot.py

    Database 4 Everything
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/db4e
    License: GPL 3.0
"""

import math
from collections import deque
from textual_plot import PlotWidget, HiResMode, LegendLocation
from textual.app import ComposeResult

from ai_snake_lab.constants.DPlot import Plot
from ai_snake_lab.constants.DLabels import DLabel
from ai_snake_lab.constants.DColors import DColor


MAX_DATA_POINTS = Plot.MAX_DATA_POINTS


class LabPlot(PlotWidget):
    """
    A widget for plotting data based on TextualPlot's PlotWidget.
    """

    def __init__(self, title, id, thin_method=None):
        super().__init__(title, id, allow_pan_and_zoom=False)
        self._plot_id = id
        self._title = title
        self._thin_method = thin_method
        self._all_days = deque(maxlen=MAX_DATA_POINTS)
        self._all_values = deque(maxlen=MAX_DATA_POINTS)

    def clear_data(self) -> None:
        self._all_days = deque(maxlen=MAX_DATA_POINTS)
        self._all_values = deque(maxlen=MAX_DATA_POINTS)

    def compose(self) -> ComposeResult:
        yield PlotWidget()

    def load_data(self, days, values, units):
        self._all_days = days
        self._all_values = values
        if units:
            self.set_ylabel(self._title + " (" + units + ")")
        else:
            self.set_ylabel(self._title)

    def add_data(self, day, value):
        self._all_days.append(day)
        self._all_values.append(value)

    def lab_plot(self, days=None, values=None) -> None:
        if len(self._all_days) == 0:
            return

        if days is not None and values is not None:
            plot_days = days
            plot_values = values
        else:
            plot_days = self._all_days
            plot_values = self._all_values
        self.clear()

        if len(plot_days) == 0:
            return

        reduced_days, reduced_values = list(self._all_days), list(self._all_values)

        self.plot(
            x=reduced_days,
            y=reduced_values,
            hires_mode=HiResMode.BRAILLE,
            line_style=DColor.GREEN,
            label=DLabel.CURRENT,
        )

        # Add an average plot over 20 to wash out the spikes and identify when the
        # AI is maxing out.
        window = max(1, len(reduced_values) // 20)
        # e.g., 5% smoothing window
        if len(reduced_values) > window:
            smoothed = [
                sum(reduced_values[i : i + window])
                / len(reduced_values[i : i + window])
                for i in range(len(reduced_values) - window + 1)
            ]
            smoothed_days = reduced_days[window - 1 :]
            self.plot(
                x=smoothed_days,
                y=smoothed,
                hires_mode=HiResMode.BRAILLE,
                line_style=DColor.RED,  # distinct color for trend
                label=DLabel.AVERAGE,
            )
        self.show_legend(location=LegendLocation.TOPLEFT)
