"""
Modules/Agent.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import torch
from Modules.ModelL import ModelL
from Modules.EpsilonAlgo import EpsilonAlgo
from Modules.ReplayMemory import ReplayMemory
from Modules.AITrainer import AITrainer
from Modules.ModelL import ModelL
from Modules.ModelRNN import ModelRNN

from Constants.DReplayMemory import MEM_TYPE


class AIAgent:

    def __init__(self, epsilon_algo: EpsilonAlgo, seed: int):
        self.epsilon_algo = epsilon_algo
        self.memory = ReplayMemory(seed=seed)
        self.model = ModelL(seed=seed)
        # self.model = ModelRNN(seed=seed)
        self.trainer = AITrainer(self.model)

        if type(self.model) == ModelRNN:
            self.memory.mem_type(MEM_TYPE.RANDOM_GAME)

    def get_model(self):
        return self.model

    def get_move(self, state):
        random_move = self.epsilon_algo.get_move()  # Explore with epsilon
        if random_move != False:
            return random_move  # Random move was returned

        # Exploit with an AI agent based action
        final_move = [0, 0, 0]
        if type(state) != torch.Tensor:
            state = torch.tensor(state, dtype=torch.float)  # Convert to a tensor
        prediction = self.model(state)  # Get the prediction
        move = torch.argmax(prediction).item()  # Select the move with the highest value
        final_move[move] = 1  # Set the move
        return final_move  # Return

    def get_optimizer(self):
        return self.trainer.get_optimizer()

    def played_game(self, score):
        self.epsilon_algo.played_game()

    def remember(self, state, action, reward, next_state, done):
        # Store the state, action, reward, next_state, and done in memory
        self.memory.append((state, action, reward, next_state, done))

    def set_model(self, model):
        self.model = model

    def set_optimizer(self, optimizer):
        self.trainer.set_optimizer(optimizer)

    def train_long_memory(self):
        # Get the states, actions, rewards, next_states, and dones from the mini_sample
        memory = self.memory.get_memory()
        memory_type = self.memory.mem_type()

        if type(self.model) == ModelRNN:
            for state, action, reward, next_state, done in memory[0]:
                self.trainer.train_step(state, action, reward, next_state, [done])

        elif memory_type == MEM_TYPE.SHUFFLE:
            for state, action, reward, next_state, done in memory:
                self.trainer.train_step(state, action, reward, next_state, [done])

        else:
            for state, action, reward, next_state, done in memory[0]:
                self.trainer.train_step(state, action, reward, next_state, [done])

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, [done])
