---
title: AI Snake Lab
---

![AI Snake Lab](/images/ai-snake-lab.png)

# 🐍 Introduction

**AI Snake Lab** is an interactive reinforcement learning sandbox for experimenting with AI agents in a classic Snake Game environment — featuring a live Textual TUI interface, distributed architecture, and modular model definitions.

---

# 🚀 Features

- 🐍 **Classic Snake environment** with customizable grid and rules
- 🧠 **AI agent interface** supporting multiple architectures (Linear, RNN, CNN)
- 🎮 **Textual-based simulator** for live visualization and metrics
- 💾 **SQLite-backed replay memory** for storing frames, episodes, and runs
- 🧩 **Experiment metadata tracking** — models, hyperparameters, experimental features
- 📊 **Built-in plotting** for scores, highscores and loss

---

# 🧰 Tech Stack

| Component                                              | Description
|--------------------------------------------------------|--------------
| [Python 3.11+](https://www.python.org/)                | The Python programming language
| [Textual](https://textual.textualize.io/)              | Rapid application development framework
| [SQLite3](https://sqlite.org/)                         | SQL engine database
| [PyTorch](https://pytorch.org/)                        | Deep learning framework
| [Textual-Plot](https://pypi.org/project/textual-plot/) | Textual plotting widget
| [ZeroMQ](https://zeromq.org/)                          | Messaging library

---

# 💻 Installation

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

# ▶️ Running the AI Snake Lab

You need three terminals to run the **AI Snake Lab**. One terminal for the `SimServer`, one for the `SimRouter`, and one for the `SimClient`.

Lanching the simulation server:

```shell
sim-server
```

Lanching the simulation router:

```shell
sim-router
```

Launching the simulation client:

```shell
sim-client
```

---

# 🙏 Acknowledgements

The original code for this project was based on a YouTube tutorial, [Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake](https://www.youtube.com/watch?v=L8ypSXwyBds) by Patrick Loeber. You can access his original code [here](https://github.com/patrickloeber/snake-ai-pytorch) on GitHub. Thank you Patrick!!! You are amazing!!!! This project is a port of the pygame and matplotlib solution.

Thanks also go out to Will McGugan and the [Textual](https://textual.textualize.io/) team. Textual is an amazing framework. Talk about *Rapid Application Development*. Porting this from a Pygame and MatPlotLib solution to Textual took less than a day.

---

# 🌟 Inspiration

Creating an artificial intelligence agent, letting it loose and watching how it performs is an amazing process. It's not unlike having children, except on a much, much, much smaller scale, at least today! Watching the AI driven Snake Game is mesmerizing. I'm constantly thinking of ways I could improve it. I credit Patrick Loeber for giving me a fun project to explore the AI space.

Much of my career has been as a Linux Systems administrator. My comfort zone is on the command line. I've never worked as a programmer and certainly not as a front end developer. [Textual](https://textual.textualize.io/), as a framework for building rich *Terminal User Interfaces* is exactly my speed and when I saw [Dolphie](https://github.com/charles-001/dolphie), I was blown away. Built-in, real-time plots of MySQL metrics: Amazing! 

Richard S. Sutton is also an inspiration to me. His thoughts on *Reinforcement Learning* are a slow motion revolution. His criticisms of the existing AI landscape with it's focus on engineering a specific AI to do a specific task and then considering the job done is spot on. His vision for an AI agent that does continuous, non-linear learning remains the next frontier on the path to *General Artificial Intelligence*.

---

# 📚 Technical Docs

- [Architecture](/pages/architecture.html)
- [Filesystem Layout](/pages/project_layout.html)
- [Database Schema](/pages/db_schema.html)
- [Constant - Definitions and Organization](/pages/constants.html)
- [Git Commit Standards](/pages/git_commit_standards.html)
- [Git Branching Strategy](/pages/git_branching_strategy.html)
- [Change Log](/CHANGELOG.md)

---

# 🔗 Links

- Patrick Loeber's [YouTube Tutorial](https://www.youtube.com/watch?v=L8ypSXwyBds)
- Will McGugan's [Textual](https://textual.textualize.io/) *Rapid Application Development* framework
- [Dolphie](https://github.com/charles-001/dolphie): *A single pane of glass for real-time analytics into MySQL/MariaDB & ProxySQL*
- Richard Sutton's [Homepage](http://www.incompleteideas.net/)
- Richard Sutton [quotes](/pages/richard_sutton.html) and other materials.
- [Useful Plots to Diagnose your Neural Network](https://medium.com/data-science/useful-plots-to-diagnose-your-neural-network-521907fa2f45) by George V Jose
- [A Deep Dive into Learning Curves in Machine Learning](https://wandb.ai/mostafaibrahim17/ml-articles/reports/A-Deep-Dive-Into-Learning-Curves-in-Machine-Learning--Vmlldzo0NjA1ODY0) by Mostafa Ibrahim

