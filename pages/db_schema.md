---
Title: Database Schema
---

# Introduction

The *AI Snake Lab* codebase has a backend SQLite3 database. The database is used to house the following information:

Table                                       | Description
--------------------------------------------|------------------------------------
[Games](#games_table)                       | Holds a *game ID* and the number of moves.
[Frames](#frames_table)                     | State: *state*, *action*, *reward*, ...
[Highscore Events](#highscore_events_table) | *Highscores widget* and *highscores plot widget* data.
[Average Loss](#avgerage_loss_table)        | *Loss plot widget* data.
[Game Score](#game_score_table)            | *Game score widget* data.

---

# Games Table

This table represents a single game. The table is used by the `ReplayMemory` class.

A new row is added at the end of each epoch by the `ReplayMemory` class.

- Table name: `games`

Column          | Data Type | Description
----------------|-----------|-------------------------
id              | INTEGER   | The *primary key* for the table.
score           | INTEGER   | The final game score
total_frames    | INTEGER   | The number of frames or moves in the game

---

# Frames Table

This table represents a single frame within a single game. This table is used by the `ReplayMemory` class.

At the end of each epoch, the `ReplayMemory` loads all of the game frame data for the completed game into this table.

- Table name: `frames`

Column          | Data Type | Description
----------------|-----------|-------------------------
id              | INTEGER   | The *primary key* for the table.
game_id         | INTEGER   | A *foreign key* to the `id` field of the `games` table.
frame_index     | INTEGER   | The move number within a game.
state           | BLOB      | A blob containing the *state map*.
action          | BLOB      | A blob containing the action: Move left, right or straight ahead.
reward          | INTEGER   | The current reward value.
next_state      | BLOB      | The next *state map*.
done            | INTEGER   | 0 or 1, indicating if the game is over or not.

---

# Highscore Events Table

This table holds a *highscore event*: The *epoch*, *game number* and a *runtime string* that represents when the highscore was achieved. This table is used in the TUI's *highscores widget* and in the TUI's *highscores plot widget*.

When a new highscore is achieved the `SimServer` inserts a row into this table.

When a `SimClient` connects connect to the `SimRouter`. It sends a `GET_CUR_HIGHSCORE` message, which is routed to the `SimServer`. The `SimServer` sends a `OLD_HIGHSCORE_EVENTS` message back to the `SimRouter` which routes it to the `SimClient`. The payload is the contents of the `highscore_events` table.

- Table name: `highscore_events`

Column          | Data Type | Description
----------------|-----------|-------------------------
id              | INTEGER   | The *primary key* for the table.
epoch           | INTEGER   | The game number when the highscore was achieved.
score           | INTEGER   | The highscore value.
runtime         | TEXT      | A string (e.g. *1h 23m*) indicating when the score was achieved.

---

# Average Loss Table

This table holds the *average loss* calulated by averaging the loss of each step within an epoch. This table is used in the TUI's *loss plot widget*.

At the end of every step, the `AITrainer` captures the loss and adds it to a list. At the end of epoch, the `SimServer` asks the `AITrainer` for the average loss. The `AITrainer` averages all of the loss values it collected, zero's out the list and returns the average. The `SimServer` inserts a row into the `avg_loss` table.

When a `SimClient` connects to the `SimRouter`. It sends a `GET_AVG_LOSS_DATA` message, which is routed to the `SimServer`. The `SimServer` sends a `AVG_LOSS_DATA` message back to the `SimRouter` which routes it back to the `SimClient`. The payload is the contents of the `avg_loss` table.

- Table name: `avg_loss`

Column          | Data Type | Description
----------------|-----------|-------------------------
id              | INTEGER   | The *primary key* for the table.
epoch           | INTEGER   | The epoch or game number.
avg_loss        | REAL      | The average loss value.

---

# Game Score Table

The table holds the *score* for each *game*. It is used in the TUI's *game score plot widget*.

At the end of each epoch, the `SimServer` inserts a row with the epoch number and the game score into the `game_score` table.

When a `SimClient` connects to the `SimRouter`. It sends a `GET_GAME_SCORE_DATA` message, which is routed to the `SimServer`. The `SimServer` sends a `OLD_GAME_SCORE_DATA` message back to the `SimRouter` which routes it back to the `SimClient`. The payload is the contents of the `game_score` table.

- Table name: `game_score`

Column          | Data Type | Description
----------------|-----------|-------------------------
id              | INTEGER   | The *primary key* for the table.
epoch           | INTEGER   | The epoch or game number.
score           | INTEGER   | The score achieved for the epoch.