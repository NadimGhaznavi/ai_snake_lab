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
import copy

from ai_snake_lab.ai.models.ModelL import ModelL
from ai_snake_lab.ai.models.ModelRNN import ModelRNN
from ai_snake_lab.constants.DModelL import DModelL
from ai_snake_lab.constants.DModelLRNN import DModelRNN
from ai_snake_lab.constants.DSim import DSim


class AITrainer:

    def __init__(self, seed):
        torch.manual_seed(seed)

        self.model = None
        self.target_model = None
        self.optimizer = None

        # self.criterion = nn.MSELoss()
        self.criterion = nn.SmoothL1Loss()
        self.gamma = DSim.DISCOUNT_RATE  # Huber loss
        self.tau = 0.01  # For soft target updates
        self.update_counter = 0
        self.target_update_freq = 100  # Every N training steps

    def get_optimizer(self):
        return self.optimizer

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def set_model(self, model):
        self.model = model

        # The learning rate needs to be adjusted for the model type
        if isinstance(model, ModelL):
            learning_rate = DModelL.LEARNING_RATE
        elif isinstance(model, ModelRNN):
            learning_rate = DModelRNN.LEARNING_RATE
        else:
            raise ValueError(f"Unknown model type: {type(model)}")

        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

        # Initialize target network as a frozen copy
        self.target_model = copy.deepcopy(self.model)
        for param in self.target_model.parameters():
            param.requires_grad = False

    def get_optimizer(self):
        return self.optimizer

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def soft_update_target(self):
        """Soft update: θ_target ← τ*θ_main + (1-τ)*θ_target"""
        for target_param, main_param in zip(
            self.target_model.parameters(), self.model.parameters()
        ):
            target_param.data.copy_(
                self.tau * main_param.data + (1.0 - self.tau) * target_param.data
            )

    def train_step(self, state, action, reward, next_state, game_over):
        # Convert to tensors
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # Add a batch dimension if needed
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over,)

        # Predicgted Q-values (main network)
        pred = self.model(state)

        # Compute target Q-values (use target network)
        target = pred.clone().detach()

        for idx in range(len(game_over)):
            Q_new = reward[idx]
            if not game_over[idx][0]:
                Q_next = torch.max(self.target_model(next_state[idx]))
                Q_new = reward[idx] + self.gamma * Q_next
            target[idx][action[idx].argmax().item()] = Q_new  # Update Q value

        # Compute loss and backprop
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)

        self.optimizer.step()  # Adjust the weights

        # Update target model periodically (soft update each N steps)
        self.update_counter += 1
        if self.update_counter % self.target_update_freq == 0:
            self.soft_update_target()
