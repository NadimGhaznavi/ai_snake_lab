# Introduction

**AI Snake Lab** is an interactive reinforcement learning sandbox for experimenting with AI agents in a classic Snake Game environment — featuring a live Textual TUI interface, flexible replay memory database, and modular model definitions.

---

# 🚀 Features

- 🐍 **Classic Snake environment** with customizable grid and rules
- 🧠 **AI agent interface** supporting multiple architectures (Linear, RNN, CNN)
- 🎮 **Textual-based simulator** for live visualization and metrics
- 💾 **SQLite-backed replay memory** for storing frames, episodes, and runs
- 🧩 **Experiment metadata tracking** — models, hyperparameters, state-map versions
- 📊 **Built-in plotting** for hashrate, scores, and learning progress

---

# 🧰 Tech Stack

| Component | Description |
|------------|--------------|
| **Python 3.11+** | Core language |
| **Textual** | Terminal UI framework |
| **SQLite3** | Lightweight replay memory + experiment store |
| **PyTorch** *(optional)* | Deep learning backend for models |
| **Plotext / Matplotlib** | Visualization tools |

---

# Installation

This project is on [PyPI](https://pypi.org/project/ai-snake-lab/). You can install the *AI Snake Lab* software using `pip`.

## Create a Sandbox 

```shell
python3 -m venv snake_venv
. snake_venv/bin/activate
```

## Install the AI Snake Lab

After you have activated your *venv* environment:

```shell
pip install ai-snake-lab
```

---

# Running the AI Snake Lab

From within your *venv* environment:

```shell
ai-snake-lab
```

---

# Links and Acknowledgements

This code is based on a YouTube tutorial, [Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake](https://www.youtube.com/watch?v=L8ypSXwyBds&t=1042s&ab_channel=freeCodeCamp.org) by Patrick Loeber. You can access his original code [here](https://github.com/patrickloeber/snake-ai-pytorch) on GitHub. Thank you Patrick!!! You are amazing!!!!

Thanks also go out to Will McGugan and the [Textual](https://textual.textualize.io/) team. Textual is an amazing framework. Talk about *rapid Application Development*. Porting this took less than a day.

---