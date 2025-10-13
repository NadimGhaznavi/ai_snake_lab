# AI Snake Lab

---

![AI Snake Lab](/images/ai-snake-lab.png)
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

# Technical Docs

- [Filesystem Layout](/pages/project_layout.html)
- [Database Schema Documentation](/pages/db_schema.html)
- Organization and Naming of [Constants](/pages/constants.html)
- [Git Commit Standards](/pages/git_commit_standards.html)
- [Git Branching Strategy](/pages/git_branching_strategy.html)
- [Change Log](/CHANGELOG.md)

---

# Acknowledgements

The original code for this project was based on a YouTube tutorial, [Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake](https://www.youtube.com/watch?v=L8ypSXwyBds) by Patrick Loeber. You can access his original code [here](https://github.com/patrickloeber/snake-ai-pytorch) on GitHub. Thank you Patrick!!! You are amazing!!!! This project is a port of the pygame and matplotlib solution.

Thanks also go out to Will McGugan and the [Textual](https://textual.textualize.io/) team. Textual is an amazing framework. Talk about *Rapid Application Development*. Porting this from a Pygame and MatPlotLib solution to Textual took less than a day.

---

# Inspiration

Creating an artificial intelligence agent, letting it loose and watching how it performs is an amazing process. It's not unlike having children, except on a much, much, much smaller scale, at least today! Watching the AI driven Snake Game is mesmerizing. I'm constantly thinking of ways I could improve it. I credit Patrick Loeber for giving me a fun project to explore the AI space.

Much of my career has been as a Linux Systems administrator. My comfort zone is on the command line. I've never worked as a programmer and certainly not as a front end developer. [Textual](https://textual.textualize.io/), as a framework for building rich *Terminal User Interfaces* is exactly my speed and when I saw [Dolphie](https://github.com/charles-001/dolphie), I was blown away. Built-in, real-time plots of MySQL metrics: Amazing! 

Richard S. Sutton is also an inspiration to me. His thoughts on *Reinforcement Learning* are a slow motion revolution. His criticisms of the existing AI landscape with it's focus on engineering a specific AI to do a specific task and then considering the job done is spot on. His vision for an AI agent that does continuous, non-linear learning remains the next frontier on the path to *General Artificial Intelligence*.

---

# Links

- Patrick Loeber's [YouTube Tutorial](https://www.youtube.com/watch?v=L8ypSXwyBds)
- Will McGugan's [Textual](https://textual.textualize.io/) *Rapid Application Development* framework
- [Dolphie](https://github.com/charles-001/dolphie): *A single pane of glass for real-time analytics into MySQL/MariaDB & ProxySQL*
- Richard Sutton's [Homepage](http://www.incompleteideas.net/)
- Richard Sutton [quotes](/pages/richard-sutton.html) and other materials.