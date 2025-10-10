"""
Modules/ModelRNN.py

    AI Snake Game Simulator
    Author: Nadim-Daniel Ghaznavi
    Copyright: (c) 2024-2025 Nadim-Daniel Ghaznavi
    GitHub: https://github.com/NadimGhaznavi/ai
    License: GPL 3.0
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ModelRNN(nn.Module):
    def __init__(self, seed: int):
        super(ModelRNN, self).__init__()
        torch.manual_seed(seed)
        input_size = 27
        hidden_size = 200
        output_size = 3
        rnn_layers = 4
        rnn_dropout = 0.2
        self.m_in = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
        )
        self.m_rnn = nn.RNN(
            input_size=hidden_size,
            hidden_size=hidden_size,
            nonlinearity="tanh",
            num_layers=rnn_layers,
            dropout=rnn_dropout,
        )
        self.m_out = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.m_in(x)
        inputs = x.view(1, -1, 200)
        x, h_n = self.m_rnn(inputs)
        x = self.m_out(x)
        return x[len(x) - 1]
