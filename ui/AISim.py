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
import sys

from textual.app import App, ComposeResult
from textual.widgets import Label, Input, Button
from textual.containers import Vertical, Horizontal
from textual.reactive import var

from Constants.DDef import DDef
from Constants.DEpsilon import DEpsilon
from Constants.DFields import DField
from Constants.DFile import DFile
from Constants.DLayout import DLayout
from Constants.DLabels import DLabel
from Constants.DReplayMemory import MEM_TYPE

from Modules.AIAgent import AIAgent
from Modules.EpsilonAlgo import EpsilonAlgo
from Widgets.GameBoard import GameBoard
from Modules.SnakeGame import SnakeGame

RANDOM_SEED = 1970


class AISim(App):
    """A Textual app that has an AI Agent playing the Snake Game."""

    TITLE = DDef.APP_TITLE
    CSS_PATH = DFile.CSS_PATH

    ## Runtime values
    # Current epsilon value (degrades in real-time)
    cur_epsilon_widget = Label("N/A", id=DLayout.CUR_EPSILON)
    # Current memory type
    cur_mem_type_widget = Label("N/A", id=DLayout.CUR_MEM_TYPE)
    # Number of stored memories
    cur_num_memories_widget = Label("N/A", id=DLayout.NUM_MEMORIES)
    # Runtime move delay value
    cur_move_delay = DDef.MOVE_DELAY

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
    start_button = Button(label=DLabel.START, id=DLayout.BUTTON_START, compact=True)
    quit_button = Button(label=DLabel.QUIT, id=DLayout.BUTTON_QUIT, compact=True)
    reset_button = Button(label=DLabel.RESET, id=DLayout.BUTTON_RESET, compact=True)
    update_button = Button(label=DLabel.UPDATE, id=DLayout.BUTTON_UPDATE, compact=True)

    def __init__(self) -> None:
        super().__init__()
        self.game_board = GameBoard(20, id=DLayout.GAME_BOARD)
        self.snake_game = SnakeGame(game_board=self.game_board, id=DLayout.GAME_BOARD)
        self.epsilon_algo = EpsilonAlgo(seed=RANDOM_SEED)
        self.agent = AIAgent(self.epsilon_algo, seed=RANDOM_SEED)
        self.running = False

        self.score = Label("Game: 0, Highscore: 0, Score: 0")

        # Setup the simulator in a background thread
        self.stop_event = threading.Event()
        self.simulator_thread = threading.Thread(target=self.start_sim, daemon=True)

    async def action_quit(self) -> None:
        """Quit the application."""
        self.stop_event.set()
        if self.simulator_thread.is_alive():
            self.simulator_thread.join(timeout=2)
        await super().action_quit()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Label(DDef.APP_TITLE, id=DLayout.TITLE)
        yield Horizontal(
            Vertical(
                Vertical(
                    Horizontal(
                        Label(
                            f"{DLabel.EPSILON_INITIAL} : ",
                            classes=DLayout.LABEL_SETTINGS,
                        ),
                        self.initial_epsilon_input,
                    ),
                    Horizontal(
                        Label(
                            f"{DLabel.EPSILON_DECAY}   : ",
                            classes=DLayout.LABEL_SETTINGS,
                        ),
                        self.epsilon_decay_input,
                    ),
                    Horizontal(
                        Label(
                            f"{DLabel.EPSILON_MIN} : ", classes=DLayout.LABEL_SETTINGS
                        ),
                        self.epsilon_min_input,
                    ),
                    Horizontal(
                        Label(
                            f"{DLabel.MOVE_DELAY}      : ",
                            classes=DLayout.LABEL_SETTINGS,
                        ),
                        self.move_delay_input,
                    ),
                    id=DLayout.SETTINGS_BOX,
                ),
                Vertical(
                    Horizontal(
                        self.start_button,
                        self.reset_button,
                        self.update_button,
                        self.quit_button,
                    ),
                    id=DLayout.BUTTON_ROW,
                ),
            ),
            Vertical(
                self.game_board,
                id=DLayout.GAME_BOX,
            ),
            Vertical(
                Horizontal(
                    Label(f"{DLabel.EPSILON} : ", classes=DLayout.LABEL),
                    self.cur_epsilon_widget,
                ),
                Horizontal(
                    Label(f"{DLabel.MEM_TYPE} : ", classes=DLayout.LABEL),
                    self.cur_mem_type_widget,
                ),
                Horizontal(
                    Label(f"{DLabel.MEMORIES} : ", classes=DLayout.LABEL),
                    self.cur_num_memories_widget,
                ),
                id=DLayout.RUNTIME_BOX,
            ),
        )

    def on_mount(self):
        self.initial_epsilon_input.value = str(DEpsilon.EPSILON_INITIAL)
        self.epsilon_decay_input.value = str(DEpsilon.EPSILON_DECAY)
        self.epsilon_min_input.value = str(DEpsilon.EPSILON_MIN)
        self.move_delay_input.value = str(DDef.MOVE_DELAY)
        settings_box = self.query_one(f"#{DLayout.SETTINGS_BOX}", Vertical)
        settings_box.border_title = DLabel.SETTINGS
        runtime_box = self.query_one(f"#{DLayout.RUNTIME_BOX}", Vertical)
        runtime_box.border_title = DLabel.RUNTIME
        self.cur_mem_type_widget.update(
            MEM_TYPE.MEM_TYPE_TABLE[self.agent.memory.mem_type()]
        )
        self.cur_num_memories_widget.update(str(self.agent.memory.get_num_memories()))
        # Initial state is that the app is stopped
        self.add_class(DField.STOPPED)

    def on_quit(self):
        if self.running == True:
            self.stop_event.set()
            if self.simulator_thread.is_alive():
                self.simulator_thread.join()
        sys.exit(0)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        # Start button was pressed
        if button_id == DLayout.BUTTON_START:
            self.start_thread()
            self.running = True
            self.add_class(DField.RUNNING)
            self.remove_class(DField.STOPPED)
            self.cur_move_delay = float(self.move_delay_input.value)
        # Reset button was pressed
        elif button_id == DLayout.BUTTON_RESET:
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

        while not self.stop_event.is_set():
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
                self.cur_num_memories_widget.update(
                    str(self.agent.memory.get_num_memories())
                )

    def start_thread(self):
        self.simulator_thread.start()


if __name__ == "__main__":
    app = AISim()
    app.run()
