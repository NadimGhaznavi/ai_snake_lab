"""
db4e/ui/TabbedPlots.py

    Database 4 Everything
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/db4e
    License: GPL 3.0
"""

from textual.containers import Container
from textual.widgets import TabbedContent, TabPane, Static
from textual.app import ComposeResult, Widget

from ai_snake_lab.ui.LabPlot import LabPlot

from ai_snake_lab.constants.DLabels import DLabel
from ai_snake_lab.constants.DPlot import Plot
from ai_snake_lab.constants.DLayout import DLayout

from textual_plot import PlotWidget, HiResMode, LegendLocation


class TabbedPlots(Widget):

    def compose(self) -> ComposeResult:
        with TabbedContent(
            DLabel.GAME_SCORE, DLabel.HIGHSCORE, id=DLayout.TABBED_PLOTS
        ):
            yield PlotWidget(id=DLayout.GAME_SCORE_PLOT)
            yield Static("HIGHSCORE PLOT")

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    def on_mount(self):
        game_score_plot = self.query_one(f"#{DLayout.GAME_SCORE_PLOT}", PlotWidget)
        game_score_plot.set_xlabel(DLabel.GAME_NUM)
        game_score_plot.set_ylabel(DLabel.GAME_SCORE)
        game_score_plot.plot(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])

    def game_score_lab_plot(self):
        self.query_one(f"#{DLayout.GAME_SCORE_PLOT}", LabPlot).lab_plot()

    def add_game_score_data(self, epoch, score):
        self.query_one(f"#{DLayout.GAME_SCORE_PLOT}", LabPlot).add_data(epoch, score)
