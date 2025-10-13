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
from textual.widgets import Label, Input, Button, Static, Log, Select
from textual.containers import Vertical, Horizontal
from textual.theme import Theme

from ai_snake_lab.constants.DDef import DDef
from ai_snake_lab.constants.DEpsilon import DEpsilon
from ai_snake_lab.constants.DFile import DFile
from ai_snake_lab.constants.DLayout import DLayout
from ai_snake_lab.constants.DLabels import DLabel
from ai_snake_lab.constants.DReplayMemory import MEM_TYPE, MEM
from ai_snake_lab.constants.DSim import DSim
from ai_snake_lab.constants.DPlot import Plot
from ai_snake_lab.constants.DModelL import DModelL
from ai_snake_lab.constants.DModelLRNN import DModelRNN

from ai_snake_lab.ai.AIAgent import AIAgent
from ai_snake_lab.ai.EpsilonAlgo import EpsilonAlgo

from ai_snake_lab.game.GameBoard import GameBoard
from ai_snake_lab.game.SnakeGame import SnakeGame

from ai_snake_lab.ui.LabPlot import LabPlot


SNAKE_LAB_THEME = Theme(
    name=DLayout.SNAKE_LAB_THEME,
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

# A list of tuples, for the TUI's model selection drop down menu (Select widget).
MODEL_TYPES: list = [
    (DLabel.LINEAR_MODEL, DModelL.MODEL),
    (DLabel.RNN_MODEL, DModelRNN.MODEL),
]

# A dictionary of model_field to model_name values, for the TUI's runtime model
# widget (Label widget).
MODEL_TYPE: dict = {
    DModelL.MODEL: DLabel.LINEAR_MODEL,
    DModelRNN.MODEL: DLabel.RNN_MODEL,
}


class AISim(App):
    """A Textual app that has an AI Agent playing the Snake Game."""

    TITLE = DLabel.APP_TITLE
    CSS_PATH = DFile.CSS_FILE

    def __init__(self) -> None:
        """Constructor"""
        super().__init__()

        # The game board, game, agent and epsilon algorithm object
        self.game_board = GameBoard(20, id=DLayout.GAME_BOARD)
        self.snake_game = SnakeGame(game_board=self.game_board, id=DLayout.GAME_BOARD)
        self.epsilon_algo = EpsilonAlgo(seed=DSim.RANDOM_SEED)
        self.agent = AIAgent(self.epsilon_algo, seed=DSim.RANDOM_SEED)

        # A dictionary to hold runtime statistics
        self.stats = {
            DSim.GAME_SCORE: {
                DSim.GAME_NUM: [],
                DSim.GAME_SCORE: [],
            }
        }

        # Prepare to run the main training loop in a background thread
        self.cur_state = DSim.STOPPED
        self.running = DSim.STOPPED
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
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
        yield Label(DLabel.APP_TITLE, id=DLayout.TITLE)

        # Configuration Settings
        yield Vertical(
            Horizontal(
                Label(
                    f"{DLabel.EPSILON_INITIAL}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                Input(
                    restrict=f"0.[0-9]*",
                    compact=True,
                    id=DLayout.EPSILON_INITIAL,
                    classes=DLayout.INPUT_10,
                ),
            ),
            Horizontal(
                Label(
                    f"{DLabel.EPSILON_DECAY}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                Input(
                    restrict=f"0.[0-9]*",
                    compact=True,
                    id=DLayout.EPSILON_DECAY,
                    classes=DLayout.INPUT_10,
                ),
            ),
            Horizontal(
                Label(f"{DLabel.EPSILON_MIN}", classes=DLayout.LABEL_SETTINGS),
                Input(
                    restrict=f"0.[0-9]*",
                    compact=True,
                    id=DLayout.EPSILON_MIN,
                    classes=DLayout.INPUT_10,
                ),
            ),
            Horizontal(
                Label(
                    f"{DLabel.MOVE_DELAY}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                Input(
                    restrict=f"[0-9]*.[0-9]*",
                    compact=True,
                    id=DLayout.MOVE_DELAY,
                    classes=DLayout.INPUT_10,
                ),
            ),
            Horizontal(
                Label(
                    f"{DLabel.MODEL_TYPE}",
                    classes=DLayout.LABEL_SETTINGS_19,
                ),
                Select(
                    MODEL_TYPES,
                    compact=True,
                    id=DLayout.MODEL_TYPE,
                    allow_blank=False,
                ),
            ),
            Horizontal(
                Label(
                    f"{DLabel.MEM_TYPE}",
                    classes=DLayout.LABEL_SETTINGS_12,
                ),
                Select(
                    MEM_TYPE.MEMORY_TYPES,
                    compact=True,
                    id=DLayout.MEM_TYPE,
                    allow_blank=False,
                ),
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
                Label(f"{DLabel.MODEL_TYPE}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.CUR_MODEL_TYPE),
            ),
            Horizontal(
                Label(f"{DLabel.MOVE_DELAY}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.CUR_MOVE_DELAY),
            ),
            Horizontal(
                Label(f"{DLabel.MEM_TYPE}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.CUR_MEM_TYPE),
            ),
            Horizontal(
                Label(f"{DLabel.STORED_GAMES}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.STORED_GAMES),
            ),
            Horizontal(
                Label(f"{DLabel.TRAINING_GAME_ID}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.CUR_TRAINING_GAME_ID),
            ),
            Horizontal(
                Label(f"{DLabel.CUR_EPSILON}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.CUR_EPSILON),
            ),
            Horizontal(
                Label(f"{DLabel.RUNTIME}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.RUNTIME),
            ),
            id=DLayout.RUNTIME_BOX,
        )

        # Buttons
        yield Vertical(
            Horizontal(
                Button(label=DLabel.START, id=DLayout.BUTTON_START, compact=True),
                Button(label=DLabel.PAUSE, id=DLayout.BUTTON_PAUSE, compact=True),
                Button(label=DLabel.QUIT, id=DLayout.BUTTON_QUIT, compact=True),
                classes=DLayout.BUTTON_ROW,
            ),
            Horizontal(
                Button(label=DLabel.DEFAULTS, id=DLayout.BUTTON_DEFAULTS, compact=True),
                Button(label=DLabel.UPDATE, id=DLayout.BUTTON_UPDATE, compact=True),
                Button(label=DLabel.RESTART, id=DLayout.BUTTON_RESTART, compact=True),
                classes=DLayout.BUTTON_ROW,
            ),
        )

        # Highscores
        yield Vertical(
            Label(
                f"   [b #3e99af]{DLabel.GAME:6s}{DLabel.SCORE:6s}       {DLabel.TIME:10s}[/]"
            ),
            Log(highlight=False, auto_scroll=True, id=DLayout.HIGHSCORES),
            id=DLayout.HIGHSCORES_BOX,
        )

        # Empty placeholders for the grid layout
        yield Static(id=DLayout.FILLER_2)

        # The game score plot
        yield LabPlot(
            title=DLabel.GAME_SCORE,
            id=DLayout.GAME_SCORE_PLOT,
            thin_method=Plot.SLIDING,
        )

    def on_mount(self):
        # Configuration defaults
        self.set_defaults()
        game_score_plot = self.query_one(f"#{DLayout.GAME_SCORE_PLOT}", LabPlot)
        game_score_plot.set_xlabel(DLabel.GAME_NUM)
        game_score_plot.set_ylabel(DLabel.GAME_SCORE)
        settings_box = self.query_one(f"#{DLayout.SETTINGS_BOX}", Vertical)
        settings_box.border_title = DLabel.SETTINGS
        # Runtime values
        highscore_box = self.query_one(f"#{DLayout.HIGHSCORES_BOX}", Vertical)
        highscore_box.border_title = DLabel.HIGHSCORES
        runtime_box = self.query_one(f"#{DLayout.RUNTIME_BOX}", Vertical)
        runtime_box.border_title = DLabel.RUNTIME_VALUES

        # Initial state is that the app is stopped
        self.add_class(DSim.STOPPED)

        # Register and set the theme
        self.register_theme(SNAKE_LAB_THEME)
        self.theme = DLayout.SNAKE_LAB_THEME

    def on_quit(self):
        if self.running == DSim.RUNNING:
            self.stop_event.set()
            if self.simulator_thread.is_alive():
                self.simulator_thread.join()
        sys.exit(0)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        # Pause button was pressed
        if button_id == DLayout.BUTTON_PAUSE:
            self.pause_event.set()
            self.running = DSim.PAUSED
            self.remove_class(DSim.RUNNING)
            self.add_class(DSim.PAUSED)

        # Restart button was pressed
        elif button_id == DLayout.BUTTON_RESTART:
            self.running = DSim.STOPPED
            self.add_class(DSim.STOPPED)
            self.remove_class(DSim.PAUSED)

            # Reset the game and the UI
            self.snake_game.reset()

            # We display the game number, highscore and score here, so clear it.
            game_box = self.query_one(f"#{DLayout.GAME_BOX}", Vertical)
            game_box.border_title = ""
            game_box.border_subtitle = ""

            # The highscores (a Log widget ) should be cleared
            highscores = self.query_one(f"#{DLayout.HIGHSCORES}", Log)
            highscores.clear()

            # Clear the plot data
            game_score_plot = self.query_one(f"#{DLayout.GAME_SCORE_PLOT}", LabPlot)
            game_score_plot.clear_data()
            game_score_plot.clear()

            # Reset the neural network's learned weights
            model = self.agent.model()
            model.reset_parameters()

            # Signal thread to stop
            self.stop_event.set()
            # Unpause so we're not blocking
            self.pause_event.clear()
            # Join the old thread
            if self.simulator_thread.is_alive():
                self.simulator_thread.join(timeout=2)
            # Recreate threading events and get a new thread
            self.stop_event = threading.Event()
            self.pause_event = threading.Event()
            self.simulator_thread = threading.Thread(target=self.start_sim, daemon=True)

        # Start button was pressed
        elif button_id == DLayout.BUTTON_START:
            # Get the configuration settings, put them into the runtime widgets and
            # pass the values to the actual backend objects
            self.update_settings()

            if self.running == DSim.STOPPED:
                self.start_thread()
            elif self.running == DSim.PAUSED:
                self.pause_event.clear()
            self.pause_event.clear()
            self.running = DSim.RUNNING
            self.add_class(DSim.RUNNING)
            self.remove_class(DSim.STOPPED)
            self.remove_class(DSim.PAUSED)

        # Defaults button was pressed
        elif button_id == DLayout.BUTTON_DEFAULTS:
            self.set_defaults()

        # Quit button was pressed
        elif button_id == DLayout.BUTTON_QUIT:
            self.on_quit()

        # Update button was pressed
        elif button_id == DLayout.BUTTON_UPDATE:
            self.update_settings()

    def set_defaults(self):
        initial_epsilon = self.query_one(f"#{DLayout.EPSILON_INITIAL}", Input)
        initial_epsilon.value = str(DEpsilon.EPSILON_INITIAL)
        epsilon_decay = self.query_one(f"#{DLayout.EPSILON_DECAY}", Input)
        epsilon_decay.value = str(DEpsilon.EPSILON_DECAY)
        epsilon_min = self.query_one(f"#{DLayout.EPSILON_MIN}", Input)
        epsilon_min.value = str(DEpsilon.EPSILON_MIN)
        mem_type = self.query_one(f"#{DLayout.MEM_TYPE}", Select)
        mem_type.value = MEM_TYPE.RANDOM_GAME
        model_type = self.query_one(f"#{DLayout.MODEL_TYPE}", Select)
        model_type.value = DModelRNN.MODEL
        move_delay = self.query_one(f"#{DLayout.MOVE_DELAY}", Input)
        move_delay.value = str(DDef.MOVE_DELAY)

    def start_sim(self):
        game_board = self.game_board
        agent = self.agent
        snake_game = self.snake_game

        # Reset the score, highscore and epoch
        score = 0
        highscore = 0
        epoch = 1

        # Update the game box, where we display the score, highscore and epch
        game_box = self.query_one(f"#{DLayout.GAME_BOX}", Vertical)
        game_box.border_title = f"{DLabel.GAME} #{epoch}"
        game_box.border_subtitle = (
            f"{DLabel.HIGHSCORE}: {highscore}, {DLabel.SCORE}: {score}"
        )

        # Start the clock for the current runtime
        start_time = datetime.now()

        # Get a reference to the stored games, highscores and current epsilon widgets.
        # We'll update these in the main training loop.
        highscores = self.query_one(f"#{DLayout.HIGHSCORES}", Log)
        cur_epsilon = self.query_one(f"#{DLayout.CUR_EPSILON}", Label)
        cur_stored_games = self.query_one(f"#{DLayout.STORED_GAMES}", Label)
        game_score_plot = self.query_one(f"#{DLayout.GAME_SCORE_PLOT}", LabPlot)
        cur_runtime = self.query_one(f"#{DLayout.RUNTIME}", Label)
        training_game_id = self.query_one(f"#{DLayout.CUR_TRAINING_GAME_ID}", Label)
        cur_move_delay = self.query_one(f"#{DLayout.MOVE_DELAY}", Input)

        # The main training loop)
        while not self.stop_event.is_set():
            ## The actual training loop...

            # Watch for user's pushing the pause button
            if self.pause_event.is_set():
                self.pause_event.wait()
                time.sleep(0.2)
                continue

            # Reinforcement learning starts here
            old_state = game_board.get_state()
            move = agent.get_move(old_state)
            reward, game_over, score = snake_game.play_step(move)

            # New highscore! Add a line to the highscores Log widget
            if score > highscore:
                highscore = score
                elapsed_secs = (datetime.now() - start_time).total_seconds()
                runtime_str = minutes_to_uptime(elapsed_secs)
                highscores.write_line(f"{epoch:6d} {score:6d} {runtime_str:>12s}")

            # Update the highscore and score on the game box
            game_box.border_subtitle = (
                f"{DLabel.HIGHSCORE}: {highscore}, {DLabel.SCORE}: {score}"
            )

            # We're still playing the current game
            if not game_over:
                # Get the current move delay from the UI
                time.sleep(float(cur_move_delay.value))

                # Reinforcement learning here....
                new_state = game_board.get_state()
                agent.train_short_memory(old_state, move, reward, new_state, game_over)
                agent.memory.append((old_state, move, reward, new_state, game_over))

            # Game is over
            else:
                # Increment the epoch and update the game box widget
                epoch += 1
                game_box.border_title = f"{DLabel.GAME} #{epoch}"

                # Remember the last move, get's passed to the ReplayMemory
                agent.memory.append(
                    (old_state, move, reward, new_state, game_over), final_score=score
                )
                # Train long memory
                agent.load_training_data()
                game_id = agent.game_id()
                if game_id == MEM.NO_DATA:
                    training_game_id.update(DLabel.N_SLASH_A)
                else:
                    training_game_id.update(str(game_id))
                agent.train_long_memory()
                # Reset the game
                snake_game.reset()
                # The Epsilon algorithm object needs to know when the game is over to
                # decay epsilon
                agent.epsilon_algo.played_game()
                # Get the current epsilon value
                cur_epsilon_value = self.epsilon_algo.epsilon()
                if cur_epsilon_value < 0.0001:
                    cur_epsilon.update("0.0000")
                else:
                    cur_epsilon.update(str(round(cur_epsilon_value, 4)))
                # Update the number of stored memories
                cur_stored_games.update(str(self.agent.memory.get_num_games()))
                # Update the stats object
                self.stats[DSim.GAME_SCORE][DSim.GAME_NUM].append(epoch)
                self.stats[DSim.GAME_SCORE][DSim.GAME_SCORE].append(score)
                # Update the plot object
                game_score_plot.add_data(epoch, score)
                game_score_plot.lab_plot()
                # Update the runtime widget
                elapsed_secs = (datetime.now() - start_time).total_seconds()
                runtime_str = minutes_to_uptime(elapsed_secs)
                cur_runtime.update(runtime_str)

    def start_thread(self):
        self.simulator_thread.start()

    def update_settings(self):
        # Get the move delay from the settings, put it into the runtime
        move_delay = self.query_one(f"#{DLayout.MOVE_DELAY}", Input)
        cur_move_delay = self.query_one(f"#{DLayout.CUR_MOVE_DELAY}", Label)
        cur_move_delay.update(move_delay.value)

        ## Changing these setings on-the-fly is like swapping out your carburetor while
        ## you're in the middle of a race. But, this is a sandbox, so let the user play.

        # Get the model type from the settings, put it into the runtime
        model_type = self.query_one(f"#{DLayout.MODEL_TYPE}", Select)
        cur_model_type = self.query_one(f"#{DLayout.CUR_MODEL_TYPE}", Label)
        cur_model_type.update(MODEL_TYPE[model_type.value])
        # Also pass it to the Agent
        self.agent.model_type(model_type=model_type.value)

        # Get the memory type from the settings, put it into the runtime
        memory_type = self.query_one(f"#{DLayout.MEM_TYPE}", Select)
        cur_mem_type = self.query_one(f"#{DLayout.CUR_MEM_TYPE}", Label)
        cur_mem_type.update(MEM_TYPE.MEM_TYPE_TABLE[memory_type.value])
        # Also pass the selected memory type to the ReplayMemory object
        self.agent.memory.mem_type(memory_type.value)


# Helper function
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


# This is for the pyPI ai-snake-lab entry point to work....
def main():
    app = AISim()
    app.run()


if __name__ == "__main__":
    main()
