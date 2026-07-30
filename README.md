# Reversi — Pygame

A two-player implementation of the classic strategy board game **Reversi**, created in Python using the Pygame library.

## About Reversi

Reversi is a strategy board game for two players, played using black and white pieces on an 8×8 board. The modern game is generally traced back to England in **1883**, when both Lewis Waterman and John W. Mollett claimed to have invented it.

A later commercial version of the game became widely known as **Othello**, although Reversi remains the general name for the original game.

## How to Play

The game begins with four pieces placed in the centre of the board:

* Two black pieces
* Two white pieces
* Matching colours positioned diagonally from one another

Black takes the first turn, after which the players alternate.

To make a valid move, a player must place a piece so that one or more of their opponent's pieces are trapped in a straight line between:

1. The newly placed piece
2. Another piece belonging to the current player

Pieces can be captured horizontally, vertically or diagonally. All trapped pieces are then flipped to the current player's colour.

A player may only place a piece in a position that captures at least one opposing piece.

The game normally ends when neither player can make another valid move or when the board is full. The player with the greatest number of pieces on the board wins.

## About This Project

This project provides a graphical, local two-player version of Reversi built entirely with Python and Pygame.

The program includes:

* A standard 8×8 Reversi board
* Local two-player gameplay
* Automatic detection of valid moves
* Highlighted available positions
* Piece capture in all eight directions
* Automatic flipping of captured pieces
* A display showing whose turn it is
* A clickable restart button
* Automatic score counting
* A game-over screen showing the winner and final score
* Support for drawn games

The game logic and graphical interface are separated into two main classes:

* `Game` manages the board, validates moves, flips pieces and determines the winner.
* `Application` manages the Pygame window, rendering, mouse input and game loop.

## Requirements

You will need:

* Python 3
* Pygame

No additional assets or image files are required.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Install Pygame

```bash
python3 -m pip install pygame
```

On Windows, you may instead need to use:

```bash
py -m pip install pygame
```

## Running the Game

Run the Python file containing the game:

```bash
python3 main.py
```

On Windows:

```bash
py main.py
```

Replace `main.py` with the actual filename if the game is stored under a different name.

## Controls

| Action           | Control                                 |
| ---------------- | --------------------------------------- |
| Place a piece    | Left-click a highlighted board position |
| Restart the game | Left-click the **Restart** button       |
| Close the game   | Close the application window            |

Valid moves are represented by grey markers on the board. Click one of these markers to place the current player's piece.

## Known Limitation

In standard Reversi, a player who has no valid move must pass their turn if the other player can still move.

The current version ends the game whenever the active player has no available moves. Support for automatically passing the turn could therefore be added in a future version to fully match the standard rules.

## Technologies Used

* Python
* Pygame

## Future Improvements

Possible future additions include:

* Correct turn passing when a player has no valid moves
* An AI computer-controlled opponent with difficulty settings
* A main menu
* Sound effects and animations
* A live score display during gameplay
* Move history and undo functionality

## Author

Created by Dan Wright.
