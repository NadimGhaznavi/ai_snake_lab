"""
ai/AITrainer.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import torch.optim as optim
import torch.nn as nn
import torch
import numpy as np
import time
import sys

from ai_snake_lab.ai.models.ModelL import ModelL
from ai_snake_lab.ai.models.ModelRNN import ModelRNN

from ai_snake_lab.constants.DModelL import DModelL
from ai_snake_lab.constants.DModelLRNN import DModelRNN
from ai_snake_lab.constants.DSim import DSim


class AITrainer:

    def __init__(self, seed):
        torch.manual_seed(seed)

        self.model = None
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.gamma = DSim.DISCOUNT_RATE

    def get_optimizer(self):
        return self.optimizer

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def set_model(self, model):
        self.model = model
        # The learning rate needs to be adjusted for the model type
        if type(model) == ModelL:
            learning_rate = DModelL.LEARNING_RATE
        elif type(model) == ModelRNN:
            learning_rate = DModelRNN.LEARNING_RATE
        else:
            raise ValueError(f"Unknown model type: {type(model)}")
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

    def train_step_cnn(self, state, action, reward, next_state, game_over):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        pred = self.model(state)
        target = pred.clone()
        if game_over:
            Q_new = reward  # No future rewards, the game is over.
        else:
            Q_new = reward + self.gamma * torch.max(self.model(next_state).detach())
        target[0][action.argmax().item()] = Q_new  # Update Q value
        self.optimizer.zero_grad()  # Reset gradients
        loss = self.criterion(target, pred)  # Calculate the loss
        loss.backward()
        self.optimizer.step()  # Adjust the weights

    def train_step(self, state, action, reward, next_state, game_over):
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        if len(state.shape) == 1:
            # Add a batch dimension
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over,)

        pred = self.model(state)
        target = pred.clone().detach()

        for idx in range(len(game_over)):
            Q_new = reward[idx]
            if not game_over[idx][0]:
                Q_new = reward[idx] + self.gamma * torch.max(
                    self.model(next_state[idx])
                )
            target[idx][action[idx].argmax().item()] = Q_new  # Update Q value

        self.optimizer.zero_grad()  # Reset gradients

        loss = self.criterion(target, pred)  # Calculate the loss
        loss.backward()
        self.optimizer.step()  # Adjust the weights
