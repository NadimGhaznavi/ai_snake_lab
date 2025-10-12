---
Constants
---

# Introduction

The *AI Snake Lab* codebase includes a large number of constants. This page outlines how these constants are named and organized. The files that contain the constants are in the `ai_sim_lab/constants` directory.

---

# Types of Constants

There are three types of constants, as shown in the table below:

**Constant Type** | **Example Name**   | **Example Value**
------------------|--------------------|------------------
Fields            | `DModelRNN.MODEL`  | `"rnn_model"`
Labels            | `DLabel.RNN_MODEL` | `"RNN"`
Defaults          | `DDef.MODEL`       | `DSim.RNN_MODEL`

---

# Categories of Constants

Constants are further organized into categories as outlined in the table below:

**Category** | **Category File** | **Category Decription**
-------------|-------------------|------------------------
Labels       | `DLabel.py`       | Human readable labels for constants.
Defaults     | `DDef.py`         | Default values for constants.
Fields       | *N/A*             | *N/A*

As you can see from the table above, the files that contain the constant field definitions are not listed. See the next section, [Constant Domains](#constant_domains). below.

---

# Constant Domains

Constant fields are organized into domains.

| **Domain File**    | **Domain Description**
|--------------------|------------------------
| `DColors.py`       | Colors used in the TUI.
| `DDir.py`          | Directory names. These are a type of *default constant*.
| `DEpsilon.py`      | Constants related to the *Epsilon Greedy* algorithm.
| `DFile.py`         | File names. These are a type of *default constant*.
| `DLayout.py`       | Field definitions used in the TUI.
| `DModelL.py`       | Constants related to the *Linear Model*.
| `DModelRNN.py`     | Constants related to the *RNN Model*.
| `DPlot.py`         | Constants related to plotting.
| `DReplayMemory.py` | Constants related to the *Replay Memory*.
| `DSim.py`          | Simulation wide constants.




---