"""
ai/Agent.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import torch
from ai_snake_lab.ai.EpsilonAlgo import EpsilonAlgo
from ai_snake_lab.ai.ReplayMemory import ReplayMemory
from ai_snake_lab.ai.AITrainer import AITrainer
from ai_snake_lab.ai.models.ModelL import ModelL
from ai_snake_lab.ai.models.ModelRNN import ModelRNN

from ai_snake_lab.constants.DLabels import DLabel
from ai_snake_lab.constants.DReplayMemory import MEM
from ai_snake_lab.constants.DModelL import DModelL
from ai_snake_lab.constants.DModelLRNN import DModelRNN


class AIAgent:

    def __init__(self, epsilon_algo: EpsilonAlgo, seed: int):
        self.epsilon_algo = epsilon_algo
        self.memory = ReplayMemory(seed=seed)
        self.trainer = None
        self._training_data = []
        self._game_id = None
        self._model_type = None
        self._seed = seed

    def game_id(self, game_id=None):
        if game_id is not None:
            self._game_id = game_id
        return self._game_id

    def get_move(self, state):
        random_move = self.epsilon_algo.get_move()  # Explore with epsilon
        if random_move != False:
            return random_move  # Random move was returned

        # Exploit with an AI agent based action
        final_move = [0, 0, 0]
        if type(state) != torch.Tensor:
            state = torch.tensor(state, dtype=torch.float)  # Convert to a tensor
        prediction = self._model(state)  # Get the prediction
        move = torch.argmax(prediction).item()  # Select the move with the highest value
        final_move[move] = 1  # Set the move
        return final_move  # Return

    def get_optimizer(self):
        return self.trainer.get_optimizer()

    def load_training_data(self):
        # Ask ReplayMemory for a single game (vectorized)
        batch, game_id = self.memory.get_training_data()
        if batch is None:
            self.game_id(MEM.NO_DATA)
            return

        states, actions, rewards, next_states, dones = batch

        # Update current game id for TUI
        self.game_id(game_id)

        # Store the training data in the agent (without frame index)
        self._training_data = list(zip(states, actions, rewards, next_states, dones))

    def model_type(self, model_type=None):
        if model_type is not None:
            if model_type == DModelL.MODEL:
                self._model = ModelL(seed=self._seed)
            elif model_type == DModelRNN.MODEL:
                self._model = ModelRNN(seed=self._seed)
            self.trainer = AITrainer(seed=self._seed)
            self.trainer.set_model(self._model)
        return self._model_type

    def model_type_name(self):
        if type(self._model) == ModelL:
            return DLabel.LINEAR_MODEL
        elif type(self._model) == ModelRNN:
            return DLabel.RNN_MODEL

    def model(self):
        return self._model

    def set_optimizer(self, optimizer):
        self.trainer.set_optimizer(optimizer)

    def train_long_memory(self, batch_size=64):
        # No training data is available
        if self.game_id() == MEM.NO_DATA:
            return

        training_batch = self.training_data()
        if not training_batch:
            return

        states, actions, rewards, next_states, dones = zip(*training_batch)
        n_samples = len(states)
        total_loss = 0.0

        # Slice into mini-batches
        for start in range(0, n_samples, batch_size):
            end = min(start + batch_size, n_samples)
            batch_states = states[start:end]
            batch_actions = actions[start:end]
            batch_rewards = rewards[start:end]
            batch_next_states = next_states[start:end]
            batch_dones = dones[start:end]

            # Vectorized training step
            loss = self.trainer.train_step(
                batch_states,
                batch_actions,
                batch_rewards,
                batch_next_states,
                batch_dones,
            )
            total_loss += loss

        avg_loss = total_loss / (n_samples / batch_size)
        return avg_loss

    def train_short_memory(self, state, action, reward, next_state, done):
        # Always train on the current frame
        self.trainer.train_step(state, action, reward, next_state, [done])

    def training_data(self):
        return self._training_data
