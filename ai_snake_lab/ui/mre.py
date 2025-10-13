from textual.app import App, ComposeResult
from textual_plot import PlotWidget, HiResMode
from textual.widgets import TabbedContent


class TabbedApp(App[None]):
    def compose(self) -> ComposeResult:
        with TabbedContent("Plot A", "Plot B"):
            yield PlotWidget(id="plot_a")
            yield PlotWidget(id="plot_b")
        yield PlotWidget()

    def on_mount(self) -> None:
        plot_a = self.query_one("#plot_a", PlotWidget)
        plot_a.plot(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], hires_mode=HiResMode.BRAILLE)
        plot_b = self.query_one("#plot_b", PlotWidget)
        plot_b.plot(x=[0, 1, 2, 3, 4], y=[2, 1, 9, 9, 3], hires_mode=HiResMode.BRAILLE)

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab


class SimplePlot(App):
    def compose(self) -> ComposeResult:
        yield PlotWidget(id="plot")

    def on_mount(self) -> None:
        plot = self.query_one("#plot", PlotWidget)
        plot.plot(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], hires_mode=HiResMode.BRAILLE)


TabbedApp().run()
# SimplePlot().run()
