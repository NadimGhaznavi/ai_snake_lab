# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] 

### Added
- Added a *Time* column to the *Highscores*

### Changed
- Plotting Widget:
  - Renamed the plotting widget from `Db4EPlot` to `LabPlot`
  - Removed the code that averaged results since I'm using a sliding method instead.

### Fixed
- Cleared the *Plot Widget* when the *Restart* button is pressedn
- Reset the neural network model's learned weights when the *Restart* button is pressed.


---

## [0.6.0] - 2025-10-12

### Added
- Added a `DColors` constants file.
- Updated website content.
  - Added *Schema*, *Constants*, *Project Layout*, *Git Branching* and *Git Commit* technical documents.
  - Added a *Richard Sutton* page.
- ReplayMemory exposes the current training game ID:
  - Modified the `ReplayMemory` to return the stored game and frame IDs.
  - Modified the `AIAgent` to first load the training data, get the training game ID, then train.
  - Modified `AISim` to get the training game ID from teh `AIAgent` and display it in the TUI.

### Changed
- Set the *learning rate* in the `AITrainer`, based on the selected *model*.

### Refactor
- Made handling and definition of constants consistent.
- Renamed the `DDb4ePlot` constants file to `DPlot`

---

## [0.5.0] - 2025-10-11

### Added
- Added a highscores widget showing the game number and the high score.
- Reworked the state map in `GameBoard:get_state()`
- Moved the `ModelRNN` model parameters into the `DModelRNN` constants file.
- Updated the *SQLite* schema used by the `ReplayMemory` class.
  - See https://snakelab.osoyalce.com/db_schema.html
- Added drop down menu to select the `ReplayMemory` type i.e. *Random Game*, *Random Frames* or *None*.
    - Added a runtime widget to display the current memory type
- Added sections to the website / README file.
- Added a [Richard Sutton](https://snakelab.osoyalce.com//richart_sutton.html) page.

---

## [0.4.8] - 2025-10-11

### Fixed
- Fix path to `AISim.tcss`.

---

## [0.4.7] - 2025-10-11

### Changed
- Use `tempfile` module to get a temporary file location for *SQLite3* database.
- Use safer cleanup for *SQLite3* database.

---

## [0.4.6] - 2025-10-11


### Fixed
- Fix path issue with `ReplayMemory`'s use of SQLite.

---

## [0.4.6] - 2025-10-11

### Fixed
- Add main() function to `AISim.py` so the CLI entry point `ai-snake-lab` works after a `pip install ai-snake-lab`.

---

## [0.4.5] - 2025-10-11

### Fixed
- Fix import statements in `ai`/* and `game`/* files.

---

## [0.4.4] - 2025-10-11

### Fixed
- Fix import statements in `Constants` files.

---

## [0.4.3] - 2025-10-11

### Added
- Initial PyPI release.

### Fixed

### Changed

---
