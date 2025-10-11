"""
AISim.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import threading
import time
import sys, os
from datetime import datetime, timedelta

from textual.app import App, ComposeResult
from textual.widgets import Label, Input, Button, Static
from textual.containers import Vertical, Horizontal
from textual.reactive import var
from textual.theme import Theme

from ai_snake_lab.constants.DDef import DDef
from ai_snake_lab.constants.DEpsilon import DEpsilon
from ai_snake_lab.constants.DFields import DField
from ai_snake_lab.constants.DFile import DFile
from ai_snake_lab.constants.DLayout import DLayout
from ai_snake_lab.constants.DLabels import DLabel
from ai_snake_lab.constants.DReplayMemory import MEM_TYPE
from ai_snake_lab.constants.DDir import DDir
from ai_snake_lab.constants.DDb4EPlot import Plot


from ai_snake_lab.ai.AIAgent import AIAgent
from ai_snake_lab.ai.EpsilonAlgo import EpsilonAlgo
from ai_snake_lab.game.GameBoard import GameBoard
from ai_snake_lab.game.SnakeGame import SnakeGame
from ai_snake_lab.ui.Db4EPlot import Db4EPlot

RANDOM_SEED = 1970

snake_lab_theme = Theme(
    name="db4e",
    primary="#88C0D0",
    secondary="#1f6a83ff",
    accent="#B48EAD",
    foreground="#31b8e6",
    background="black",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="black",
    panel="#000000",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)


class AISim(App):
    """A Textual app that has an AI Agent playing the Snake Game."""

    TITLE = DDef.APP_TITLE
    CSS_PATH = os.path.join(DDir.UTILS, DFile.CSS_FILE)

    ## Runtime values
    # Current epsilon value (degrades in real-time)
    cur_epsilon_widget = Label("N/A", id=DLayout.CUR_EPSILON)
    # Current memory type
    cur_mem_type_widget = Label("N/A", id=DLayout.CUR_MEM_TYPE)
    # Current model type
    cur_model_type_widget = Label("N/A", id=DLayout.CUR_MODEL_TYPE)
    # Time delay between moves
    cur_move_delay = DDef.MOVE_DELAY
    # Number of stored games in the ReplayMemory
    cur_num_games_widget = Label("N/A", id=DLayout.NUM_GAMES)
    # Elapsed time
    cur_runtime_widget = Label("N/A", id=DLayout.RUNTIME)

    # Intial Settings for Epsilon
    initial_epsilon_input = Input(
        restrict=f"0.[0-9]*",
        compact=True,
        id=DLayout.EPSILON_INITIAL,
        classes=DLayout.INPUT_10,
    )
    epsilon_min_input = Input(
        restrict=f"0.[0-9]*",
        compact=True,
        id=DLayout.EPSILON_MIN,
        classes=DLayout.INPUT_10,
    )
    epsilon_decay_input = Input(
        restrict=f"0.[0-9]*",
        compact=True,
        id=DLayout.EPSILON_DECAY,
        classes=DLayout.INPUT_10,
    )
    move_delay_input = Input(
        restrict=f"[0-9]*.[0-9]*",
        compact=True,
        id=DLayout.MOVE_DELAY,
        classes=DLayout.INPUT_10,
    )

    # Buttons
    pause_button = Button(label=DLabel.PAUSE, id=DLayout.BUTTON_PAUSE, compact=True)
    restart_button = Button(
        label=DLabel.RESTART, id=DLayout.BUTTON_RESTART, compact=True
    )
    start_button = Button(label=DLabel.START, id=DLayout.BUTTON_START, compact=True)
    quit_button = Button(label=DLabel.QUIT, id=DLayout.BUTTON_QUIT, compact=True)
    defaults_button = Button(
        label=DLabel.DEFAULTS, id=DLayout.BUTTON_DEFAULTS, compact=True
    )
    update_button = Button(label=DLabel.UPDATE, id=DLayout.BUTTON_UPDATE, compact=True)

    # A dictionary to hold runtime statistics
    stats = {
        DField.GAME_SCORE: {
            DField.GAME_NUM: [],
            DField.GAME_SCORE: [],
        }
    }

    game_score_plot = Db4EPlot(
        title=DLabel.GAME_SCORE, id=DLayout.GAME_SCORE_PLOT, thin_method=Plot.SLIDING
    )

    def __init__(self) -> None:
        super().__init__()
        self.game_board = GameBoard(20, id=DLayout.GAME_BOARD)
        self.snake_game = SnakeGame(game_board=self.game_board, id=DLayout.GAME_BOARD)
        self.epsilon_algo = EpsilonAlgo(seed=RANDOM_SEED)
        self.agent = AIAgent(self.epsilon_algo, seed=RANDOM_SEED)
        self.cur_state = DField.STOPPED
        self.game_score_plot._x_label = DLabel.GAME_NUM
        self.game_score_plot._y_label = DLabel.GAME_SCORE

        # Setup the simulator in a background thread
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.running = DField.STOPPED
        self.simulator_thread = threading.Thread(target=self.start_sim, daemon=True)

    async def action_quit(self) -> None:
        """Quit the application."""
        self.stop_event.set()
        if self.simulator_thread.is_alive():
            self.simulator_thread.join(timeout=2)
        await super().action_quit()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        # Title bar
        yield Label(DDef.APP_TITLE, id=DLayout.TITLE)

        # Configuration Settings
        yield Vertical(
            Horizontal(
                Label(
                    f"{DLabel.EPSILON_INITIAL}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                self.initial_epsilon_input,
            ),
            Horizontal(
                Label(
                    f"{DLabel.EPSILON_DECAY}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                self.epsilon_decay_input,
            ),
            Horizontal(
                Label(f"{DLabel.EPSILON_MIN}", classes=DLayout.LABEL_SETTINGS),
                self.epsilon_min_input,
            ),
            Horizontal(
                Label(
                    f"{DLabel.MOVE_DELAY}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                self.move_delay_input,
            ),
            id=DLayout.SETTINGS_BOX,
        )

        # The Snake Game
        yield Vertical(
            self.game_board,
            id=DLayout.GAME_BOX,
        )

        # Runtime values
        yield Vertical(
            Horizontal(
                Label(f"{DLabel.EPSILON}", classes=DLayout.LABEL),
                self.cur_epsilon_widget,
            ),
            Horizontal(
                Label(f"{DLabel.MEM_TYPE}", classes=DLayout.LABEL),
                self.cur_mem_type_widget,
            ),
            Horizontal(
                Label(f"{DLabel.STORED_GAMES}", classes=DLayout.LABEL),
                self.cur_num_games_widget,
            ),
            Horizontal(
                Label(f"{DLabel.MODEL_TYPE}", classes=DLayout.LABEL),
                self.cur_model_type_widget,
            ),
            Horizontal(
                Label(f"{DLabel.RUNTIME}", classes=DLayout.LABEL),
                self.cur_runtime_widget,
            ),
            id=DLayout.RUNTIME_BOX,
        )

        # Buttons
        yield Vertical(
            Horizontal(
                self.start_button,
                self.pause_button,
                self.quit_button,
                classes=DLayout.BUTTON_ROW,
            ),
            Horizontal(
                self.defaults_button,
                self.update_button,
                self.restart_button,
                classes=DLayout.BUTTON_ROW,
            ),
        )

        # Empty fillers
        yield Static(id=DLayout.FILLER_1)
        yield Static(id=DLayout.FILLER_2)
        yield Static(id=DLayout.FILLER_3)

        # The game score plot
        yield self.game_score_plot

    def on_mount(self):
        self.initial_epsilon_input.value = str(DEpsilon.EPSILON_INITIAL)
        self.epsilon_decay_input.value = str(DEpsilon.EPSILON_DECAY)
        self.epsilon_min_input.value = str(DEpsilon.EPSILON_MIN)
        self.move_delay_input.value = str(DDef.MOVE_DELAY)
        settings_box = self.query_one(f"#{DLayout.SETTINGS_BOX}", Vertical)
        settings_box.border_title = DLabel.SETTINGS
        runtime_box = self.query_one(f"#{DLayout.RUNTIME_BOX}", Vertical)
        runtime_box.border_title = DLabel.RUNTIME_VALUES
        self.cur_mem_type_widget.update(
            MEM_TYPE.MEM_TYPE_TABLE[self.agent.memory.mem_type()]
        )
        self.cur_num_games_widget.update(str(self.agent.memory.get_num_games()))
        # Initial state is that the app is stopped
        self.add_class(DField.STOPPED)
        # Register the theme
        self.register_theme(snake_lab_theme)

        # Set the app's theme
        self.theme = "db4e"

    def on_quit(self):
        if self.running == DField.RUNNING:
            self.stop_event.set()
            if self.simulator_thread.is_alive():
                self.simulator_thread.join()
        sys.exit(0)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        # Pause button was pressed
        if button_id == DLayout.BUTTON_PAUSE:
            self.pause_event.set()
            self.running = DField.PAUSED
            self.remove_class(DField.RUNNING)
            self.add_class(DField.PAUSED)
            self.cur_move_delay = float(self.move_delay_input.value)
            self.cur_model_type_widget.update(self.agent.model_type())

        # Restart button was pressed
        elif button_id == DLayout.BUTTON_RESTART:
            self.running = DField.STOPPED
            self.add_class(DField.STOPPED)
            self.remove_class(DField.PAUSED)

            # Signal thread to stop
            self.stop_event.set()
            # Unpause so we can exit cleanly
            self.pause_event.clear()
            # Join the old thread
            if self.simulator_thread.is_alive():
                self.simulator_thread.join(timeout=2)

            # Reset the game and the UI
            self.snake_game.reset()
            score = 0
            highscore = 0
            self.epoch = 1
            game_box = self.query_one(f"#{DLayout.GAME_BOX}", Vertical)
            game_box.border_title = ""
            game_box.border_subtitle = ""

            # Recreate events and get a new thread
            self.stop_event = threading.Event()
            self.pause_event = threading.Event()
            self.simulator_thread = threading.Thread(target=self.start_sim, daemon=True)

        # Start button was pressed
        elif button_id == DLayout.BUTTON_START:
            if self.running == DField.STOPPED:
                self.start_thread()
            elif self.running == DField.PAUSED:
                self.pause_event.clear()
            self.pause_event.clear()
            self.running = DField.RUNNING
            self.add_class(DField.RUNNING)
            self.remove_class(DField.STOPPED)
            self.remove_class(DField.PAUSED)
            self.cur_move_delay = float(self.move_delay_input.value)
            self.cur_model_type_widget.update(self.agent.model_type())

        # Reset button was pressed
        elif button_id == DLayout.BUTTON_DEFAULTS:
            self.initial_epsilon_input.value = str(DEpsilon.EPSILON_INITIAL)
            self.epsilon_decay_input.value = str(DEpsilon.EPSILON_DECAY)
            self.epsilon_min_input.value = str(DEpsilon.EPSILON_MIN)
            self.move_delay_input.value = str(DDef.MOVE_DELAY)

        # Quit button was pressed
        elif button_id == DLayout.BUTTON_QUIT:
            self.on_quit()

        # Update button was pressed
        elif button_id == DLayout.BUTTON_UPDATE:
            self.cur_move_delay = float(self.move_delay_input.value)

    def start_sim(self):
        self.snake_game.reset()
        game_board = self.game_board
        agent = self.agent
        snake_game = self.snake_game
        score = 0
        highscore = 0
        self.epoch = 1
        game_box = self.query_one(f"#{DLayout.GAME_BOX}", Vertical)
        game_box.border_title = f"{DLabel.GAME} #{self.epoch}"
        start_time = datetime.now()

        while not self.stop_event.is_set():
            if self.pause_event.is_set():
                self.pause_event.wait()
                time.sleep(0.2)
                continue
            # The actual training loop...
            old_state = game_board.get_state()
            move = agent.get_move(old_state)
            reward, game_over, score = snake_game.play_step(move)
            if score > highscore:
                highscore = score
            game_box.border_subtitle = (
                f"{DLabel.HIGHSCORE}: {highscore}, {DLabel.SCORE}: {score}"
            )
            if not game_over:
                ## Keep playing
                time.sleep(self.cur_move_delay)
                new_state = game_board.get_state()
                agent.train_short_memory(old_state, move, reward, new_state, game_over)
                agent.remember(old_state, move, reward, new_state, game_over)
            else:
                ## Game over
                self.epoch += 1
                game_box = self.query_one(f"#{DLayout.GAME_BOX}", Vertical)
                game_box.border_title = f"{DLabel.GAME} #{self.epoch}"
                # Remember the last move
                agent.remember(old_state, move, reward, new_state, game_over)
                # Train long memory
                agent.train_long_memory()
                # Reset the game
                snake_game.reset()
                # Let the agent know we've finished a game
                agent.played_game(score)
                # Get the current epsilon value
                cur_epsilon = self.epsilon_algo.epsilon()
                if cur_epsilon < 0.0001:
                    self.cur_epsilon_widget.update("0.0000")
                else:
                    self.cur_epsilon_widget.update(str(round(cur_epsilon, 4)))
                # Update the number of stored memories
                self.cur_num_games_widget.update(str(self.agent.memory.get_num_games()))
                # Update the stats object
                self.stats[DField.GAME_SCORE][DField.GAME_NUM].append(self.epoch)
                self.stats[DField.GAME_SCORE][DField.GAME_SCORE].append(score)
                # Update the plot object
                self.game_score_plot.add_data(self.epoch, score)
                self.game_score_plot.db4e_plot()
                # Update the runtime widget
                elapsed_secs = (datetime.now() - start_time).total_seconds()
                runtime = minutes_to_uptime(elapsed_secs)
                self.cur_runtime_widget.update(runtime)

    def start_thread(self):
        self.simulator_thread.start()


def minutes_to_uptime(seconds: int):
    # Return a string like:
    # 0h 0m 45s
    # 1d 7h 32m
    days, minutes = divmod(int(seconds), 86400)
    hours, minutes = divmod(minutes, 3600)
    minutes, seconds = divmod(minutes, 60)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def main():
    app = AISim()
    app.run()


if __name__ == "__main__":
    main()
