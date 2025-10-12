---
Title: AI Snake Lab - SQLite3 Schema
---

# Phase I

The diagram below shows the database schema used by the AI Snake Lab. The backend is SQLite3. This database is created when `ai-snake-lab` is started and deleted when the program exits.

![AI Snake Lab Database Schema](/images/ai-snake-lab-schema.png)

---

# Long Term Vision

The long term vision is to house all of the information needed to recreate a given simulation. This includes:

- Model description
- Hyper parameters
- Replay memory configuration
- Reward system configuraton
- AI Snake Lab code version
- AI Snake Lab schema version
- Random seed value

Additionally, runtime performance information will also be stored including:

- Highscores table (game # : score)
- Replay memory
- Weighted model
- Start time
- End time

This information can be used to restart a simulation, clone a simulation and repeat a simulation.
