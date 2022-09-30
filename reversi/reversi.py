from typing import List, Union
import itertools
import os
import sys
import numpy as np


EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1

DR: List[int] = [0, -1, -1, -1, 0, 1, 1, 1]
DC: List[int] = [1, 1, 0, -1, -1, -1, 0, 1]


def display_board(board: np.ndarray) -> bool:
    def convert(x: int) -> str:
        if x == EMPTY:
            return " "
        elif x == WHITE:
            return "o"
        else:
            return "x"

    print("   {} {} {} {} {} {} {} {}".format(*list(range(8))))
    print("  ----------------")
    for i, row in enumerate(board):
        print("{}| {} {} {} {} {} {} {} {}".format(i, *list(map(convert, row))))

    return True


def put_stone(board: np.ndarray, r: int, c: int, color: int) -> Union[np.ndarray, None]:
    """Put specified color stone into specified place.
    Args:
        board (np.ndarray): A 2-D list indicating the board.
        r (int): Number of row of the place.
        c (int): Number of column of the place.
        color (int): Color of the stone. (WHITE -> 0, BLACK -> 1)
    Returns:
        Bool: True If the stone has been successfully put, False otherwise.
    """

    nboard = board.copy()
    candidate = get_candidate(nboard, color)
    if np.sum(candidate, axis=2)[r, c] == 0:
        return None

    nboard[r, c] = color

    for i, (dr, dc) in enumerate(zip(DR, DC)):
        if candidate[r, c, i] == 0:
            continue
        nr: int = r
        nc: int = c
        while True:
            nr += dr
            nc += dc

            if nboard[nr, nc] == color:
                break
            nboard[nr, nc] = color

    return nboard


def get_candidate(board: np.ndarray, color: int) -> np.ndarray:
    """Get a list of places where stones can be placed.

    Arg:
        board (np.ndarray): A 2-D list indicating the board.
    Return:
        List[List[bool]]: True if stone can ben placed there, False otherwise.
    """

    result: np.ndarray = np.array(
        [[[0 for k in range(8)] for j in range(8)] for i in range(8)], dtype=np.int32
    )
    for i, j in itertools.product(range(8), repeat=2):
        if board[i, j] != EMPTY:
            continue

        for k, (dr, dc) in enumerate(zip(DR, DC)):
            r: int = i
            c: int = j
            count: int = 0

            ok: bool = False

            while True:
                r += dr
                c += dc

                if not (0 <= r < 8 and 0 <= c < 8):
                    break

                if board[r, c] == EMPTY:
                    break

                if board[r, c] == color:
                    ok = True
                    break
                else:
                    count += 1

            result[i, j, k] = count if ok else 0

    return result


def main():
    board: np.ndarray = np.array(
        [[EMPTY for j in range(8)] for i in range(8)], dtype=np.int32
    )
    turn: int = 0

    board[3, 3] = WHITE
    board[3, 4] = BLACK
    board[4, 3] = BLACK
    board[4, 4] = WHITE

    display_board(board)
    board = put_stone(board, 2, 4, 0)
    display_board(board)


if __name__ == "__main__":
    main()
