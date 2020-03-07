![GitHub](https://img.shields.io/github/license/arthurdjn/pysnake) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/arthurdjn/pysnake/master) ![GitHub issues](https://img.shields.io/github/issues/arthurdjn/pysnake) 


# PySnake

**Deep Learning** and **Genetic Algorithm** applied to the snake game.

## Overview

**PySnake** is an artificial intelligence that learns to control a snake. This AI learns to recognize its environment and choose the best direction to survive.
This model uses Genetic Algorithm theory, as there is no training data available.
<p align="center">
  <b>PySnake Interface</b><br>
  <img src="img/pysnake_ai.gif">
  <br>
</p>


### Snake Game

The game is simple. The player / AI control a snake in four directions : UP, RIGHT, DOWN, LEFT. The goal is to eat as many apples as possible, increasing the snake's length.
The snake dies when it eats itself or crash in a wall.

### SAGA

The model has been trained on [SAGA](https://documentation.sigma2.no/quick/saga.html) servers, through 3000 generations of 1500 snakes each.

## Getting Started

### Install

To install, run the command in the root folder:

```pycon
$ pip install .
```

Or simply clone this repository:

```
$ git clone https://github.com/arthurdjn/pysnake
```

Note that pysnake requires [pygame](https://www.pygame.org/news) to visualize the game.
I you installed **pysnake** through pip, it will automatically download all required dependencies. Otherwise, use:

```
$ pip install pygame
$ pip install numpy
$ pip install json
```

### Config

The application settings are available from the config.ini file. You can create a custom one, as long as you have the necessary parameters.
  

### Play

To simply play the game and test all options available:
```
$ python pysnake
```
You can explicitly use:
```
$ python pysnake --mode play
```

If you created a custom config.ini:
```
$ python pysnake --config path/to/your/config.ini
```


### Train

```
$ python pysnake --mode train
```

#### Save

#### Load


```
$ python pysnake --snake pysnake/snake.json
```


```
$ python pysnake --replay pysnake/snake.json
```


```
$ python pysnake --mode train --population pysnake/saves/generation_1500
```

## Development

### Vision

<p align="center">
  <b>8-mode vision</b><br>
  <img src="img/pysnake_vision.gif">
  <br>
</p>

### Neural Network

### Genetic Algorithm
