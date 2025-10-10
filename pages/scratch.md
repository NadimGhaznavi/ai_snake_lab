# Introduction

This is a port of my old *AI Snake Game* project that was using *pygame*, *matplotlib*, a verbose log file and a bunch of terminals grepping different, interesting metrics out of the log file.

This version is based on the [Textual](https://textual.textualize.io/) *rapid application development framework*.

# Installation

You can easily clone this setup and run it yourself.

## Setup a venv environment

```shell
python3 -m venv snake_venv
. snake_venv/bin/activate
```

## Install Textual

After you activate your *venv* environment:

```
pip install textual textual-dev numpy
```

## Install Pytorch

To install pytorch go to [pytorch.org](https://pytorch.org/) and scroll down till you come to the *Install PyTorch* section. Click on your platform (Linux, Mac, Windows), choose a compute platform and cut-and-paste the *run this command*. I'm running Linux and I don't have a GPU, but your setup may be different.

## Download my Code

# Introduction

This is a port of my old *AI Snake Game* project that was using *pygame*, *matplotlib*, a verbose log file and a bunch of terminals grepping different, interesting metrics out of the log file.

This version is based on the [Textual](https://textual.textualize.io/) *rapid application development framework*.

# Installation

You can easily clone this setup and run it yourself.

## Setup a venv environment

```shell
python3 -m venv snake_venv
. snake_venv/bin/activate
```

## Install Textual

After you activate your *venv* environment:

```
pip install textual textual-dev numpy
```

## Install Pytorch

To install pytorch go to [pytorch.org](https://pytorch.org/) and scroll down till you come to the *Install PyTorch* section. Click on your platform (Linux, Mac, Windows), choose a compute platform and cut-and-paste the *run this command*. I'm running Linux and I don't have a GPU, but your setup may be different.

## Download my Code

I'll package this into a PyPI package shortly, but for now you can manually clone the repo:

```shell
git clone https://github.com/NadimGhaznavi/ai_snake
```

# Running the AI Simulator

From within your venv environment:

```shell
cd ai_snake
python AISim.py
```

Control-Q to quit.

# Acknowlegements and Links

This code is based on a YouTube tutorial, [Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake](https://www.youtube.com/watch?v=L8ypSXwyBds&t=1042s&ab_channel=freeCodeCamp.org) by Patrick Loeber. You can access his original code [here](https://github.com/patrickloeber/snake-ai-pytorch) on GitHub. Thank you Patrick!!! You are amazing!!!!

Thanks also go out to Will McGugan and the [Textual](https://textual.textualize.io/) team. Textual is an amazing framework. Talk about *rapid Application Development*. Porting this took less than a day.



# Running the AI Simulator

From within your venv environment:

```shell
python AISim.py
```

Control-Q to quit.

# Acknowlegements and Links

This code is based on a YouTube tutorial, [Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake](https://www.youtube.com/watch?v=L8ypSXwyBds&t=1042s&ab_channel=freeCodeCamp.org) by Patrick Loeber. You can access his original code [here](https://github.com/patrickloeber/snake-ai-pytorch) on GitHub. Thank you Patrick!!! You are amazing!!!!

Thanks also go out to Will McGugan and the [Textual](https://textual.textualize.io/) team. Textual is an amazing framework. Talk about *rapid Application Development*. Porting this took less than a day.


