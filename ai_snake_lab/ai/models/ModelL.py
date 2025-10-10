"""
Modules/ModelL.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ModelL(nn.Module):
    def __init__(self, seed: int):
        super(ModelL, self).__init__()
        torch.manual_seed(seed)
        input_size = 27  # Size of the "state" as tracked by the GameBoard
        hidden_size = 170
        output_size = 3
        p_value = 0.1
        self.input_block = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
        )
        self.hidden_block = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
        )
        self.dropout_block = nn.Dropout(p=p_value)
        self.output_block = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.input_block(x)
        x = self.hidden_block(x)
        x = self.dropout_block(x)
        x = self.output_block(x)
        return x
