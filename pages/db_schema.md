---
Title: AI Snake Lab - Constants
---

# Introduction

The *AI Snake Lab* codebase includes a large number of constants. This page outlines how these constants are named and organized.

---

# Types of Constants

There are three types of constants, as shown in the table below:

**Constant Type** | **Example Name**   | **Example Value**
------------------|--------------------|------------------
Fields            | `DSim.RNN_MODEL`   | `"rnn_model"`
Labels            | `DLabel.RNN_MODEL` | `"RNN"`
Defaults          | `DDef.MODEL`       | `DSim.RNN_MODEL`

---

# Categories of Constants

Constants are further organized into categories as outlined in the table below:

**Category** | **Category File** | **Category Decription**
-------------|-------------------|------------------------
Labels       | `DLabel.py`       | Human readable labels for constants
Defaults     | `DDef.py`         | Default values for constants
Fields       | *N/A*             | *N/A*

As you can see from the table above, the files that contain the constant field definitions are not listed. See the next section, [Constant Domains](#constant_domains). below.

---

# Constant Domains

Constant fields are organized into domains.

| **Domain File** | **Domain Description**
|-----------------|------------------------
| 