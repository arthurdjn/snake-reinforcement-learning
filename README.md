![GitHub](https://img.shields.io/github/license/arthurdjn/pysnake)


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


### Config

The application settings are available from the config.ini file. You can create a custom one, as long as you have the necessary parameters : 

<div class="tg-wrap"><table>
  <tr>
    <th colspan="3"><b>Config.ini File</th>
  </tr>
  <tr>
    <th><b>Parameter</th>
    <th><b>Type</th>
    <th><b>Description</th>
  </tr>
  <tr>
    <th colspan="3"><b>Game<br></th>
  </tr>
  <tr>
    <td><b>board_size<br></td>
    <td><i>tuple(int, int)<br></td>
    <td>Size of the game, in number of cells. <i>Default is (15, 15).</td>
  </tr>
  <tr>
    <td><b>seed<br></td>
    <td><i>int or None<br></td>
    <td>Fix random numbers. <i>Default is None.</td>
  </tr>
  <tr>
    <th colspan="3"><b>WindowGame<br></th>
  </tr>
  <tr>
    <td><b>render<br></td>
    <td><i>bool<br></td>
    <td>Display a window for the game in pygame. <br>It can be better to set False when training.<br><i>Default is True.</td>
  </tr>
  <tr>
    <td><b>show_grid<br></td>
    <td><i>bool<br></td>
    <td>Show a grid on the game.<br> You can activate it by pressing the <b>key g.</b><br><i>Default is True.</td>
  </tr>
  <tr>
    <td><b>show_vision<br></td>
    <td><i>bool<br></td>
    <td>Show the snakes' vision.<br>You can activate it by pressing the <b>key v.</b><br><i>Default is False.</td>
  </tr>
  <tr>
    <td><b>cell_size<br></td>
    <td><i>int<br></td>
    <td>Width & height of a cell, in pixel.<br><i>Default is 50.</td>
  </tr>
  <tr>
    <td><b>fps_play<br></td>
    <td><i>int<br></td>
    <td>FPS of the playble game.<br><i>Default is 10.</td>
  </tr>
  <tr>
    <td><b>fps_train<br></td>
    <td><i>int<br></td>
    <td>FPS when training snakes.<br><i>Default is 1000.</td>
  </tr>
  <tr>
    <th colspan="3"><b>Snake<br></th>
  </tr>
  <tr>
    <td><b>length<br></td>
    <td><i>int<br></td>
    <td>Initial length of a snake.<br><i>Default is 3.</td>
  </tr>
  <tr>
    <td><b>vision_type<br></td>
    <td><i>str<br></td>
    <td>Vision type used as input in the neural network.<br>If "distance", it will normalize distance from detected objects in a range from 0 to 1.<br>If "binary", it will one-hot encoded in 3-bit as follow : <br>is there a wall ?<br>is there an apple ?<br>is there a snake ?<br><i>Default is "distance".</td>
  </tr>
  <tr>
    <td><b>vision_mode<br></td>
    <td><i>int<br></td>
    <td>Number of vision / ray object used to detect objects.<br><i>Default is 8.</td>
  </tr>
  <tr>
    <td><b>max_lifespan<br></td>
    <td><i>int or None<br></td>
    <td>Maximal lifespan of a snake.<br>Note that a snake that still score 0 after 100 steps will die.<br><i>Default is 1000.</td>
  </tr>
  <tr>
    <th colspan="3"><b>NeuralNetwork</th>
  </tr>
  <tr>
    <td><b>hidden_layers<br></td>
    <td><i>list(*int)<br></td>
    <td>Hidden layers dimensions.<br><i>Default is [20, 12]</td>
  </tr>
  <tr>
    <td><b>activation_hidden<br></td>
    <td><i>function<br></td>
    <td>Activation function used in the hidden layers.<br>Options are sigmoid, tanh, relu, leaky_relu, linear, softmax.<br>You can add in addition custom function.<br><i>Default is relu.</td>
  </tr>
  <tr>
    <td><b>activation_output<br></td>
    <td><i>function<br></td>
    <td>Activation function used in the last layer.<br>Options are sigmoid, tanh, relu, leaky_relu, linear, softmax<br>You can add in addition custom function.<br><i>Default is softmax.<br></td>
  </tr>
  <tr>
    <th colspan="3"><b>GeneticAlgorithm<br></th>
  </tr>
  <tr>
    <td><b>save_best_individuals<br></td>
    <td><i>bool<br></td>
    <td>Save the best individuals from a generation.<br><i>Default is True.</td>
  </tr>
  <tr>
    <td><b>save_generations<br></td>
    <td><i>bool<br></td>
    <td>Save all individuals from a generation.<br><i>Default is False.</td>
  </tr>
  <tr>
    <td><b>save_steps<br></td>
    <td><i>int<br></td>
    <td>Save each x steps.<br><i>Default is 20.</td>
  </tr>
  <tr>
    <td><b>save_dir<br></td>
    <td><i>str<br></td>
    <td>Directory where individuals are saved.<br><i>Default is "saves"</td>
  </tr>
  <tr>
    <td><b>num_generations<br></td>
    <td><i>int<br></td>
    <td>Number of generations.<br><i>Default is 3000.</td>
  </tr>
  <tr>
    <td><b>num_parents<br></td>
    <td><i>int<br></td>
    <td>Number of parents. Parents won't have mutated genes and crossover.<br><i>Default is 500.</td>
  </tr>
  <tr>
    <td><b>num_offspring<br></td>
    <td><i>int<br></td>
    <td>Number of offspring. Offspring may have mutated genes and crossover.<br><i>Default is 1000.</td>
  </tr>
  <tr>
    <td><b>probability_SBX<br></td>
    <td><i>float<br></td>
    <td>Probability that Simulated Binary Crossover (SBX) occurs.<br><i>Default is 0.5.</td>
  </tr>
  <tr>
    <td><b>probability_SPBX<br></td>
    <td><i>float<br></td>
    <td>Probability that Single Point Binary Crossover (SPBX) occurs.<br><i>Default is 0.5.</td>
  </tr>
  <tr>
    <td><b>eta_SBX<br></td>
    <td><i>int<br></td>
    <td>eta parameter for Simulated Binary Crossover.<br><i>Default is 100.</td>
  </tr>
  <tr>
    <td><b>mutation_rate<br></td>
    <td><i>float<br></td>
    <td>Probability that a chromosome mutate.<br><i>Default is 0.005.</td>
  </tr>
</table></div>
  

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
