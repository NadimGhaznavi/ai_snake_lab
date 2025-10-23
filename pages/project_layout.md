---
Title: Project Layout
---

# Directory Structure

```
ai_snake_lab/
├── ai_snake_lab/
│   ├── ai/
│   │   ├── AIAgent.py
│   │   ├── AITrainer.py
│   │   ├── EpsilonAlgo.py
│   │   ├── EpsilonAlgoN.py
│   │   ├── ReplayMemory.py
│   │   └── models/
│   │       ├── ModelL.py
│   │       └── ModelRNN.py
│   ├── constants/
│   │   ├── DAIAgent.py
│   │   ├── DColors.py
│   │   ├── DDef.py
│   │   ├── DDir.py
│   │   ├── DEpsilon.py
│   │   ├── DFile.py
│   │   ├── DLabels.py
│   │   ├── DLayout.py
│   │   ├── DModelL.py
│   │   ├── DModelRNN.py
│   │   ├── DPlot.py
│   │   ├── DReplayMemory.py
│   │   ├── DSim.py
│   │   └── __init__.py
│   ├── game/
│   │   ├── GameBoard.py
│   │   ├── GameElements.py
│   │   └── SnakeGame.py
│   ├── ui/
│   │   ├── AISim.py
│   │   ├── AISim.tcss
│   │   └── TabbedPlots.py
│   ├── utils/
│   │   └── ConstGroup.py
│   └── sim_server.py                  
├── pages                              Project website pages
│   ├── project_layout.md
|   └── db_schema.md
├── images                             Project website images
│   ├── ai-snake-lab.png
|   ├── ai-snake-lab-schema.png 
│   └── ...
├── pyproject.toml
├── README.md
├── index.md                           Project website homepage
├── CHANGELOG.md                       Project changelog
├── LICENSE
└── .gitignore
```