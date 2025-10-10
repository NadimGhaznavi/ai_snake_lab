---
Title: Project Layout
---

# Directory Structure

```
ai_snake_lab/
├── ai_snake_lab/
│   ├── __init__.py
│   ├── ai/
│   │   ├── ai_agent.py
│   │   ├── replay_memory_db.py
│   │   └── models/
│   │       ├── linear_model.py
│   │       ├── rnn_model.py
│   │       └── ...
│   ├── db/
│   │   ├── schema.sql
│   │   └── __init__.py
│   ├── game/
│   │   ├── snake_game.py
│   │   ├── game_board.py
│   │   └── agent_interface.py
│   ├── ui/
│   │   ├── simulator_app.py
│   │   └── plots.py
│   └── utils/
│       ├── config.py
│       └── logger.py
├── pages
│   ├── project_layout.md
|   └── db_schema.md
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```