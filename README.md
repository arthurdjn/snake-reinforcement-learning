![GitHub](https://img.shields.io/github/license/arthurdjn/pysnake) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/arthurdjn/pysnake/master) ![GitHub issues](https://img.shields.io/github/issues/arthurdjn/pysnake) 


# PySnake

**Deep Learning** and **Genetic Algorithm** applied to the snake game.

## Overview

**PySnake** is an artificial intelligence that learns to control a snake. This AI learns to recognize its environment and choose the best direction to survive.
This model uses Genetic Algorithm theory, as there is no training data provided. Genetic Algorithm provides an alternative as each agents (snakes) learned to evolve in a new environment.

<p align="center">
  <b>PySnake Interface</b><br>
  <img src="img/pysnake_intro.png">
  <br>
</p>


### Snake Game

The game is simple. The player / AI control a snake in four directions : UP, RIGHT, DOWN, LEFT. The goal is to eat as many apples as possible, increasing the snake's length.
The snake dies when it eats itself or crash in a wall.

### SAGA

The model has been trained on [SAGA servers](https://documentation.sigma2.no/quick/saga.html), in 3000 generations of 1500 snakes each.
With 8GB ram and 4 nodes, the training session lasted 4 days.

## Getting Started

### Install



### Config

The application settings are available from the config.ini file. You can create a custom one, as long as you have the necessary parameters.
  

### Play

### Train

#### Save

#### Load

## Development

### Vision

<p align="center">
  <b>8-mode vision</b><br>
  <img src="img/pysnake_vision.png">
  <br>
</p>

### Neural Network

### Genetic Algorithm
