"""
db4e/Modules/Db4EPlot.py

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

from ai_snake_lab.constants.DDb4EPlot import Plot
from ai_snake_lab.constants.DLabels import DLabel


MAX_DATA_POINTS = Plot.MAX_DATA_POINTS


class Db4EPlot(PlotWidget):
    """
    A widget for plotting data based on TextualPlot's PlotWidget.
    """

    def __init__(self, title, id, thin_method=None):
        super().__init__(title, id, allow_pan_and_zoom=False)
        self._plot_id = id
        self._title = title
        self._thin_method = thin_method
        if thin_method == Plot.SLIDING:
            self._all_days = deque(maxlen=MAX_DATA_POINTS)
            self._all_values = deque(maxlen=MAX_DATA_POINTS)
        else:
            self._all_days = None
            self._all_values = None

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

    def set_xlabel(self, label):
        return super().set_xlabel(label)

    def db4e_plot(self, days=None, values=None) -> None:
        if days is not None and values is not None:
            plot_days = days
            plot_values = values
        else:
            plot_days = self._all_days
            plot_values = self._all_values
        self.clear()
        if len(plot_days) == 0:
            return
        if self._thin_method == Plot.AVERAGE:
            reduced_days, reduced_values = self.reduce_data(plot_days, plot_values)
        else:
            reduced_days, reduced_values = list(self._all_days), list(self._all_values)

        self.plot(
            x=reduced_days,
            y=reduced_values,
            hires_mode=HiResMode.BRAILLE,
            line_style="green",
            label=DLabel.CURRENT,
        )

        # Add an average plot over 20 to wash out the spikes and identify when the
        # AI is maxing out.
        window = max(1, len(reduced_values) // 20)  # e.g., 5% smoothing window
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
                line_style="red",  # distinct color for trend
                label=DLabel.AVERAGE,
            )
        self.show_legend(location=LegendLocation.TOPLEFT)

    def reduce_data2(self, times, values):
        # Reduce the total number of data points, otherwise the plot gets "blurry"
        step = max(1, len(times) // MAX_DATA_POINTS)

        # Reduce times with step
        reduced_times = times[::step]

        # Bin values by step (average)
        reduced_values = [
            sum(values[i : i + step]) / len(values[i : i + step])
            for i in range(0, len(values), step)
        ]
        results = reduced_times[: len(reduced_values)], reduced_values
        return results

    def reduce_data(self, times, values):
        """Reduce times and values into <= MAX_DATA_POINTS bins.
        Each bin's value is the average of the values in the bin.
        Each bin's time is chosen as the last time in the bin (so last bin -> times[-1]).
        """
        if not times or not values:
            return [], []

        assert len(times) == len(values), "times and values must be same length"

        step = max(1, math.ceil(len(times) / MAX_DATA_POINTS))

        reduced_times = []
        reduced_values = []
        for i in range(0, len(times), step):
            chunk_times = times[i : i + step]
            chunk_vals = values[i : i + step]

            # average values (works for floats or Decimal)
            avg_val = sum(chunk_vals) / len(chunk_vals)

            # representative time: choose last item in the chunk so final rep is times[-1]
            rep_time = chunk_times[-1]

            reduced_times.append(rep_time)
            reduced_values.append(avg_val)

        # Guarantee the final time equals the exact last time (safety)
        if reduced_times:
            reduced_times[-1] = times[-1]

        return reduced_times, reduced_values

    def update_time_range(self, selected_time):
        if selected_time == -1:
            return

        selected_time = int(selected_time)
        max_length = len(self._all_days)
        if selected_time > max_length:
            new_values = self._all_values
            new_times = self._all_days
        else:
            new_values = self._all_values[-selected_time:]
            new_times = self._all_days[-selected_time:]
        self.db4e_plot(new_times, new_values)
