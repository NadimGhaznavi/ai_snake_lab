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
from textual.widgets import Label, Input, Button, Static, Log, Select, Checkbox
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
from ai_snake_lab.constants.DAIAgent import DAIAgent


from ai_snake_lab.ai.AIAgent import AIAgent
from ai_snake_lab.ai.EpsilonAlgo import EpsilonAlgo

from ai_snake_lab.game.GameBoard import GameBoard
from ai_snake_lab.game.SnakeGame import SnakeGame

from ai_snake_lab.ui.TabbedPlots import TabbedPlots


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
    surface="#111111",
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

# A list of tuples, for the TUI's exploration selection drop down menu (Select widget).
EXPLORATION_TYPES: list = [
    (DLabel.EPSILON_N, DEpsilon.EPSILON_N),
    (DLabel.EPSILON, DEpsilon.EPSILON),
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
        self.agent = AIAgent(seed=DSim.RANDOM_SEED)

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
                    f"{DLabel.LEARNING_RATE}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                Input(
                    restrict=f"[0-9]*.[0-9]*",
                    compact=True,
                    id=DLayout.LEARNING_RATE,
                    classes=DLayout.INPUT_10,
                ),
            ),
            Horizontal(
                Label(
                    f"{DLabel.DYNAMIC_TRAINING}",
                    classes=DLayout.LABEL_SETTINGS,
                ),
                Checkbox(
                    id=DLayout.DYNAMIC_TRAINING,
                    classes=DLayout.INPUT_10,
                    compact=True,
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
            Horizontal(
                Label(
                    f"{DLabel.EXPLORATION}",
                    classes=DLayout.LABEL_SETTINGS_12,
                ),
                Select(
                    EXPLORATION_TYPES,
                    compact=True,
                    id=DLayout.EXPLORATION,
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
                Label(f"{DLabel.TRAINING_LOOPS}", classes=DLayout.LABEL),
                Label(DLabel.N_SLASH_A, id=DLayout.TRAINING_LOOPS),
            ),
            Horizontal(
                Label(
                    f"{DLabel.TRAINING_GAME_ID}",
                    classes=DLayout.LABEL,
                    id=DLayout.TRAINING_ID_LABEL,
                ),
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
                f"[b #3e99af]{DLabel.GAME:>7s}{DLabel.SCORE:>7s}{DLabel.TIME:>13s}[/]"
            ),
            Log(highlight=False, auto_scroll=True, id=DLayout.HIGHSCORES),
            id=DLayout.HIGHSCORES_BOX,
        )

        # Empty placeholders for the grid layout
        yield Static(id=DLayout.FILLER_2)

        # The game score plot
        yield TabbedPlots(id=DLayout.TABBED_PLOTS)

    def on_mount(self):

        # Configuration defaults
        self.set_defaults()
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

        # Add a starting point of (0,0) to the highscores plot
        plots = self.query_one(f"#{DLayout.TABBED_PLOTS}", TabbedPlots)
        plots.add_highscore_data(0, 0)

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
            plots = self.query_one(f"#{DLayout.TABBED_PLOTS}", TabbedPlots)
            plots.clear_data()

            # Reset the neural network's learned weights
            model = self.agent.model()
            model.reset_parameters()

            # Set the current stored games back to zero
            cur_stored_games = self.query_one(f"#{DLayout.STORED_GAMES}", Label)
            cur_stored_games.update("0")

            # Clear the ReplayMemory's runtime DB
            self.agent.memory.clear_runtime_data()

            # Reset the training game id
            self.query_one(f"#{DLayout.CUR_TRAINING_GAME_ID}", Label).update(
                DLabel.N_SLASH_A
            )

            ## Simulation loop thread control
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
        self.query_one(f"#{DLayout.EPSILON_INITIAL}", Input).value = str(
            DEpsilon.EPSILON_INITIAL
        )
        self.query_one(f"#{DLayout.EPSILON_DECAY}", Input).value = str(
            DEpsilon.EPSILON_DECAY
        )
        self.query_one(f"#{DLayout.EPSILON_MIN}", Input).value = str(
            DEpsilon.EPSILON_MIN
        )
        self.query_one(f"#{DLayout.MEM_TYPE}", Select).value = MEM_TYPE.RANDOM_GAME

        # The "default" learning rate is model specific
        cur_model_type = self.query_one(f"#{DLayout.MODEL_TYPE}", Select).value
        learning_rate = self.query_one(f"#{DLayout.LEARNING_RATE}", Input)
        if cur_model_type == DModelL.MODEL:
            learning_rate_value = f"{DModelL.LEARNING_RATE:.6f}"
        elif cur_model_type == DModelRNN.MODEL:
            learning_rate_value = f"{DModelRNN.LEARNING_RATE:.6f}"
        learning_rate.value = str(learning_rate_value)

        # Adaptive Memory
        self.query_one(f"#{DLayout.DYNAMIC_TRAINING}", Checkbox).value = True

        # Move delay
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
        plots = self.query_one(f"#{DLayout.TABBED_PLOTS}", TabbedPlots)
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
            move = agent.get_move(old_state, score)
            reward, game_over, score = snake_game.play_step(move)

            # New highscore! Add a line to the highscores Log widget
            if score > highscore:
                highscore = score
                elapsed_secs = (datetime.now() - start_time).total_seconds()
                runtime_str = minutes_to_uptime(elapsed_secs)
                highscores.write_line(f"{epoch:7,d}{score:7d}{runtime_str:>13s}")
                plots.add_highscore_data(epoch, score)
                # Send the EpsilonN a signal to instantiate a new EpsilonAlgo.
                # This call is accepted, but ignored by the vanilla EpsilonAlog
                agent.explore.new_highscore(score=score)

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
                game_box.border_title = f"{DLabel.GAME} {epoch:,}"

                # Remember the last move, get's passed to the ReplayMemory
                agent.memory.append(
                    (old_state, move, reward, new_state, game_over), final_score=score
                )

                # Load the training data
                agent.load_training_data()
                # Update the TUI
                mem_type = agent.memory.mem_type()
                # If the memory type is random frames, show the number of frames
                if mem_type == MEM_TYPE.SHUFFLE:
                    num_frames = agent.num_frames()
                    if num_frames == MEM.NO_DATA:
                        training_game_id.update(DLabel.N_SLASH_A)
                    else:
                        training_game_id.update(str(num_frames))
                # If the memory type is random game, show the game ID
                elif mem_type == MEM_TYPE.RANDOM_GAME:
                    game_id = agent.game_id()
                    if game_id == MEM.NO_DATA:
                        training_game_id.update(DLabel.N_SLASH_A)
                    else:
                        training_game_id.update(str(game_id))

                # Pass the epoch to the Agent to support "adapative training"
                agent.epoch(epoch)

                # Do the long training
                agent.train_long_memory()

                # Reset the game
                snake_game.reset()
                # The Epsilon algorithm object needs to know when the game is over to
                # decay epsilon
                agent.explore.played_game(score=score)
                # Get the current epsilon value
                cur_epsilon_value = agent.explore.epsilon(score=score)
                if cur_epsilon_value < 0.0001:
                    cur_epsilon.update("0.0000")
                else:
                    cur_epsilon.update(str(round(cur_epsilon_value, 4)))

                # Update the number of stored memories
                stored_games = agent.memory.get_num_games()
                cur_stored_games.update(f"{stored_games:,}")
                # Update the stats object
                self.stats[DSim.GAME_SCORE][DSim.GAME_NUM].append(epoch)
                self.stats[DSim.GAME_SCORE][DSim.GAME_SCORE].append(score)
                # Update the plot object
                plots.add_game_score_data(epoch, score)

                # Update the runtime widget
                elapsed_secs = (datetime.now() - start_time).total_seconds()
                runtime_str = minutes_to_uptime(elapsed_secs)
                cur_runtime.update(runtime_str)

                # Update the loss plot
                epoch_loss_avg = agent.trainer.get_epoch_loss()
                plots.add_loss_data(epoch=epoch, loss=epoch_loss_avg)

                # Update the training loops value
                if self.query_one(f"#{DLayout.DYNAMIC_TRAINING}", Checkbox).value:
                    loops = max(
                        1, min(epoch // 250, DAIAgent.MAX_DYNAMIC_TRAINING_LOOPS)
                    )
                else:
                    loops = 1
                self.query_one(f"#{DLayout.TRAINING_LOOPS}", Label).update(str(loops))

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

        # Now that we've set the model, we can pass in the learning rate
        learning_rate = self.query_one(f"#{DLayout.LEARNING_RATE}", Input).value
        self.agent.trainer.set_learning_rate(float(learning_rate))

        # Get the memory type from the settings, put it into the runtime
        memory_type = self.query_one(f"#{DLayout.MEM_TYPE}", Select)
        cur_mem_type = self.query_one(f"#{DLayout.CUR_MEM_TYPE}", Label)
        cur_mem_type.update(MEM_TYPE.MEM_TYPE_TABLE[memory_type.value])
        # Also pass the selected memory type to the ReplayMemory object
        self.agent.memory.mem_type(memory_type.value)
        # Adaptive memory
        self.agent.dynamic_training(
            self.query_one(f"#{DLayout.DYNAMIC_TRAINING}", Checkbox).value
        )

        # Change the current settings from Game ID to Random Frames if we're using
        # random frames
        if memory_type.value == MEM_TYPE.SHUFFLE:
            training_label = self.query_one(f"#{DLayout.TRAINING_ID_LABEL}", Label)
            training_label.update(DLabel.RANDOM_FRAMES)

        # Set the exploration type
        self.agent.set_explore(self.query_one(f"#{DLayout.EXPLORATION}", Select).value)

        # Get the epsilon settings and pass them to the explore module (Epsilon or EpsilonN)
        self.agent.explore.epsilon_min(
            float(self.query_one(f"#{DLayout.EPSILON_MIN}", Input).value)
        )
        self.agent.explore.initial_epsilon(
            float(self.query_one(f"#{DLayout.EPSILON_INITIAL}", Input).value)
        )
        self.agent.explore.epsilon_decay(
            float(self.query_one(f"#{DLayout.EPSILON_DECAY}", Input).value)
        )


# Helper function
def minutes_to_uptime(seconds: int):
    # Return a string like:
    # 0h 0m 45s
    # 1d 7h 32m
    days, minutes = divmod(int(seconds), 86400)
    hours, minutes = divmod(minutes, 3600)
    minutes, seconds = divmod(minutes, 60)

    if days > 0:
        if seconds < 10:
            seconds = f" {seconds}"
        if minutes < 10:
            minutes = f" {minutes}"
        if hours < 10:
            hours = f" {hours}"
        return f"{days}d {hours}h {minutes}m"

    elif hours > 0:
        if seconds < 10:
            seconds = f" {seconds}"
        if minutes < 10:
            minutes = f" {minutes}"
        return f"{hours}h {minutes}m"

    elif minutes > 0:
        if seconds < 10:
            seconds = f" {seconds}"
        if minutes < 10:
            return f" {minutes}m {seconds}s"
        return f"{minutes}m {seconds}s"

    else:
        return f"{seconds}s"


# This is for the pyPI ai-snake-lab entry point to work....
def main():
    app = AISim()
    app.run()


if __name__ == "__main__":
    main()
