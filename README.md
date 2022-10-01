# Reversi

Simplest reversi game program implemented by Python 3.8

## Requirements

- Python 3.8.x
- Ubuntu 20.04

## Installation

1. Clone this repository

```bash
git clone https://github.com/fjnkt98/reversi.git
```

2. Create virtual environment by using `venv`

```bash
cd reversi
python3 -m venv env
source env/bin/activate
```

3. Install this package

```bash
pip install -e .
```

## Play this game

Execute entrypoint command to launch game.

```bash
reversi
```

Execute this, you will see following display:

```
   0 1 2 3 4 5 6 7
  ----------------
0|
1|
2|
3|       o x
4|       x o
5|
6|
7|

Current Turn: WHITE
Candidate space is: (2, 4) (3, 5) (4, 2) (5, 3)
Enter row and column numbers of where you want to put the stone, separated by spaces:
```

`o` indicates white stone, `x` indicates black stone.

The game starts with white's turn.

Enter row and column numbers of where you want to put the stone.
Only single-byte numbers separated by spaces are accepted.

Hints of where stones can be put are displayed, so you can refer them.
