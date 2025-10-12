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

from ai_snake_lab.constants.DReplayMemory import MEM_TYPE
from ai_snake_lab.constants.DLabels import DLabel


class AIAgent:

    def __init__(self, epsilon_algo: EpsilonAlgo, seed: int):
        self.epsilon_algo = epsilon_algo
        self.memory = ReplayMemory(seed=seed)
        # self._model = ModelL(seed=seed)
        self._model = ModelRNN(seed=seed)
        self.trainer = AITrainer(model=self._model)

        if type(self._model) == ModelRNN:
            self.memory.mem_type(MEM_TYPE.RANDOM_GAME)

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

    def model_type(self):
        if type(self._model) == ModelL:
            return DLabel.MODEL_LINEAR
        elif type(self._model) == ModelRNN:
            return DLabel.MODEL_RNN

    def model(self):
        return self._model

    def played_game(self, score):
        self.epsilon_algo.played_game()

    def remember(self, state, action, reward, next_state, done, score=None):
        # Store the state, action, reward, next_state, and done in memory
        self.memory.append((state, action, reward, next_state, done, score))

    def set_optimizer(self, optimizer):
        self.trainer.set_optimizer(optimizer)

    def train_long_memory(self):
        # Ask ReplayMemory for data
        training_data = self.memory.get_training_data(n_games=1)
        if not training_data:
            return  # either no memory or user chose None

        for state, action, reward, next_state, done, *_ in training_data:
            self.trainer.train_step(state, action, reward, next_state, [done])

    def train_short_memory(self, state, action, reward, next_state, done):
        # Always train on the current frame
        self.trainer.train_step(state, action, reward, next_state, [done])
