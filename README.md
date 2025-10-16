# 🐍 AI Snake Lab

---

![AI Snake Lab](/images/ai-snake-lab.png)
# 📝 Introduction

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

# 🔄 Dynamic Training

The *Dynamic Training* checkbox implements an increasing amount of *long training* that is executed at the end of each *epoch*. The `AIAgent:train_long_memory()` code is run an increasing number of times at the end of each epoch as the total number of epochs increases to a maximum of `MAX_ADAPTIVE_TRAINING_LOOPS`, which is currently `16` according to the calculation shown below:

```
    if self.dynamic_training():
        loops = max(
            1, min(self.epoch() // 250, DAIAgent.MAX_DYNAMIC_TRAINING_LOOPS)
        )
    else:
        loops = 1

    while loops > 0:
        loops -= 1
        self.train_long_memory()
```

---

# 🧩 Epsilon N

The *Epsilon N* class, inspired by Richard Sutton's [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html), is a drop-in replacement for the traditional *Epsilon Greedy* algorithm. It instantiates a traditional *Epsilon Greedy* instance for each score. For example, when the AI has a score of 7, an *Epsilon Greedy* instance at `self._epsilons[7]` is used.

The screenshot below shows the *Highscores* plot with the traditional, single instance *Epsilon Greedy* algorithm and with [Dynamic Training](#dynamic-training) enabled. The single-instance epsilon algorithm quickly converges but shows uneven progress. The abrupt jumps in the high score line indicate that exploration declines before the AI fully masters each stage of play.

![Traditional Epsilon Greedy](/images/highscores-epsilon.png)

The next screenshot shows the *Highscores* plot without [Dynamic Training](#dynamic-training) enabled and with the *Epsilon N* being used. By maintaining a separate epsilon for each score level, *Epsilon N* sustains exploration locally. This results in a smoother, more linear high-score curve as the AI consolidates learning at each stage before progressing.

![Epsilon N](/images/highscores-epsilon-n.png)

As shown above, the traditional Epsilon Greedy approach leads to slower improvement, with the highscore curve flattening early. By contrast, Epsilon N maintains steady progress as the AI masters each score level independently.

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

From within your *venv* environment:

```shell
ai-snake-lab
```

---

# ⚠️ Limitations

Because the simulation runs in a Textual TUI, terminal resizing and plot redraws can subtly affect the simulation timing. As a result, highscore achievements may appear at slightly different game numbers across runs. This behavior is expected and does not indicate a bug in the AI logic.

If you have a requirement to make simulation runs repeatable, drop me a note and I can implement a **headless mode** where the simulation runs in a separate process outside of Textual.

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

- [Filesystem Layout](/pages/project_layout.html)
- [Database Schema Documentation](/pages/db_schema.html)
- Organization and Naming of [Constants](/pages/constants.html)
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