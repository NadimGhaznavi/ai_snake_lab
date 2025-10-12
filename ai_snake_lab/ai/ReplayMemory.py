"""
ai/ReplayMemory.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0

This file contains the ReplayMemory class.
"""

import os
import random
import sqlite3, pickle
import tempfile

from ai_snake_lab.constants.DReplayMemory import MEM_TYPE
from ai_snake_lab.constants.DDef import DDef


class ReplayMemory:

    def __init__(self, seed: int):
        random.seed(seed)
        self.batch_size = 250
        # Valid options: shuffle, random_game or none
        self._mem_type = MEM_TYPE.RANDOM_GAME
        self.min_games = 1

        # All of the states for a game are stored, in order.
        self.cur_memory = []

        # Get a temporary directory for the DB file
        self._tmpfile = tempfile.NamedTemporaryFile(suffix=DDef.DOT_DB, delete=False)
        self.db_file = self._tmpfile.name

        # Connect to SQLite
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)

        # Get a cursor
        self.cursor = self.conn.cursor()

        # We don't need the file handle anymore
        self._tmpfile.close()

        # Intialize the schema
        self.init_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass  # avoid errors on interpreter shutdown

    def append(self, transition, final_score=None):
        """Add a transition to the current game."""
        old_state, move, reward, new_state, done, final_score = transition

        self.cur_memory.append((old_state, move, reward, new_state, done))

        if done:
            if final_score is None:
                raise ValueError("final_score must be provided when the game ends")

            total_frames = len(self.cur_memory)

            # Record the game
            self.cursor.execute(
                "INSERT INTO games (score, total_frames) VALUES (?, ?)",
                (final_score, total_frames),
            )
            game_id = self.cursor.lastrowid

            # Record the frames
            for i, (state, action, reward, next_state, done) in enumerate(
                self.cur_memory
            ):
                self.cursor.execute(
                    """
                    INSERT INTO frames (game_id, frame_index, state, action, reward, next_state, done)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        game_id,
                        i,
                        pickle.dumps(state),
                        pickle.dumps(action),
                        reward,
                        pickle.dumps(next_state),
                        done,
                    ),
                )

            self.conn.commit()
            self.cur_memory = []

    def close(self):
        """Close the database connection."""
        if getattr(self, "conn", None):
            self.conn.close()
            self.conn = None
        if getattr(self, "db_file", None) and os.path.exists(self.db_file):
            os.remove(self.db_file)
            self.db_file = None

    def get_average_game_length(self):
        self.cursor.execute("SELECT AVG(total_frames) FROM games")
        avg = self.cursor.fetchone()[0]
        return int(avg) if avg else 0

    def get_random_frames(self, n=None):
        if n is None:
            n = self.get_average_game_length() or 32  # fallback if no data

        self.cursor.execute(
            "SELECT state, action, reward, next_state, done "
            "FROM frames ORDER BY RANDOM() LIMIT ?",
            (n,),
        )
        rows = self.cursor.fetchall()

        frames = [
            (
                pickle.loads(state_blob),
                pickle.loads(action),
                float(reward),
                pickle.loads(next_state_blob),
                bool(done),
            )
            for state_blob, action, reward, next_state_blob, done in rows
        ]
        return frames

    def get_random_game(self):
        self.cursor.execute("SELECT id FROM games")
        all_ids = [row[0] for row in self.cursor.fetchall()]
        if not all_ids or len(all_ids) < self.min_games:
            return False

        rand_id = random.choice(all_ids)
        self.cursor.execute(
            "SELECT state, action, reward, next_state, done "
            "FROM frames WHERE game_id = ? ORDER BY frame_index ASC",
            (rand_id,),
        )
        rows = self.cursor.fetchall()
        if not rows:
            return False

        game = [
            (
                pickle.loads(state_blob),
                pickle.loads(action),
                float(reward),
                pickle.loads(next_state_blob),
                bool(done),
            )
            for state_blob, action, reward, next_state_blob, done in rows
        ]
        return game

    def get_num_games(self):
        """Return number of games stored in the database."""
        self.cursor.execute("SELECT COUNT(*) FROM games")
        return self.cursor.fetchone()[0]

    def get_training_data(self, n_games=None, n_frames=None):
        """
        Returns a list of transitions for training based on the current memory type.

        - n_games: used for RANDOM_GAME (how many full games to sample)
        - n_frames: used for SHUFFLE (how many frames to sample)
        - Returns empty list if memory type is NONE or if database/memory is empty
        """
        mem_type = self.mem_type()

        print(f"SELECTED memory type: {mem_type}")
        if mem_type == MEM_TYPE.NONE:
            return []

        elif mem_type == MEM_TYPE.RANDOM_GAME:
            n_games = n_games or 1
            training_data = []
            for _ in range(n_games):
                game = self.get_random_game()
                if game:
                    training_data.extend(game)
            return training_data

        elif mem_type == MEM_TYPE.SHUFFLE:
            n_frames = n_frames or self.get_average_game_length()
            frames = self.get_random_frames(n=n_frames)
            return frames

        else:
            raise ValueError(f"Unknown memory type: {mem_type}")

    def init_db(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                total_frames INTEGER NOT NULL
            );
            """
        )
        self.conn.commit()

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS frames (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER NOT NULL,
                frame_index INTEGER NOT NULL,
                state BLOB NOT NULL,
                action BLOB NOT NULL,      
                reward INTEGER NOT NULL,
                next_state BLOB NOT NULL,
                done INTEGER NOT NULL,        -- 0 or 1
                FOREIGN KEY (game_id) REFERENCES games(id)
            );
            """
        )
        self.conn.commit()

        self.cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_game_frame ON frames (game_id, frame_index);
            """
        )
        self.conn.commit()

        self.cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_frames_game_id ON frames (game_id);
            """
        )
        self.conn.commit()

    def mem_type(self, mem_type=None):
        if mem_type is not None:
            self._mem_type = mem_type
        return self._mem_type

    def set_memory(self, memory):
        self.memory = memory
