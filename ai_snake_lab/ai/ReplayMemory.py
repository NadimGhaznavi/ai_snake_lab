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
from collections import deque
import random
import sqlite3, pickle
import tempfile
import shutil

from ai_snake_lab.constants.DReplayMemory import MEM_TYPE
from ai_snake_lab.constants.DDef import DDef


class ReplayMemory:

    def __init__(self, seed: int):
        random.seed(seed)
        self.batch_size = 250
        # Valid options: shuffle, random_game, targeted_score, random_targeted_score
        self._mem_type = MEM_TYPE.RANDOM_GAME
        self.min_games = 1
        self.max_states = 15000
        self.max_shuffle_games = 40
        self.max_games = 500

        if self._mem_type == MEM_TYPE.SHUFFLE:
            # States are stored in a deque and a random sample will be returned
            self.memories = deque(maxlen=self.max_states)

        elif self._mem_type == MEM_TYPE.RANDOM_GAME:
            # All of the states for a game are stored, in order, in a deque.
            # A complete game will be returned
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

    def append(self, transition):
        """Add a transition to the current game."""
        if self._mem_type != MEM_TYPE.RANDOM_GAME:
            raise NotImplementedError(
                "Only RANDOM_GAME memory type is implemented for SQLite backend"
            )

        self.cur_memory.append(transition)
        _, _, _, _, done = transition

        if done:
            # Serialize the full game to JSON
            serialized = pickle.dumps(self.cur_memory)
            self.cursor.execute(
                "INSERT INTO games (transitions) VALUES (?)", (serialized,)
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

    def get_random_game(self):
        """Return a random full game from the database."""
        self.cursor.execute("SELECT id FROM games")
        all_ids = [row[0] for row in self.cursor.fetchall()]
        if len(all_ids) >= self.min_games:
            rand_id = random.choice(all_ids)
            self.cursor.execute("SELECT transitions FROM games WHERE id=?", (rand_id,))
            row = self.cursor.fetchone()
            if row:
                return pickle.loads(row[0])
        return False

    def get_random_states(self):
        mem_size = len(self.memories)
        if mem_size < self.batch_size:
            return self.memories
        return random.sample(self.memories, self.batch_size)

    def get_memory(self):
        if self._mem_type == MEM_TYPE.SHUFFLE:
            return self.get_random_states()

        elif self._mem_type == MEM_TYPE.RANDOM_GAME:
            return self.get_random_game()

    def get_num_games(self):
        """Return number of games stored in the database."""
        self.cursor.execute("SELECT COUNT(*) FROM games")
        return self.cursor.fetchone()[0]

    def init_db(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transitions TEXT NOT NULL
        )
        """
        )
        self.conn.commit()

    def mem_type(self, mem_type=None):
        if mem_type is not None:
            self._mem_type = mem_type
        return self._mem_type

    def set_memory(self, memory):
        self.memory = memory
