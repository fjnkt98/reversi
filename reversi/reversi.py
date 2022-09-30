from typing import List
import os
import sys


EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1


def display_board(board: List[List[int]]) -> bool:
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


def put_stone(board: List[List[int]], r: int, c: int, color: int) -> bool:
    """Put specified color stone into specified place.
    Args:
        board (List[List[int]]): A 2-D list indicating the board.
        r (int): Number of row of the place.
        c (int): Number of column of the place.
        color (int): Color of the stone. (WHITE -> 0, BLACK -> 1)
    Returns:
        Bool: True If the stone has been successfully put, False otherwise.
    """

    return True


def show_candidate(board: List[List[int]]) -> List[List[bool]]:
    """View a list of places where stones can be placed.

    Arg:
        board (List[List[int]]): A 2-D list indicating the board.
    Return:
        List[List[bool]]: True if stone can ben placed there, False otherwise.
    """

    return []


def main():
    board: List[List[int]] = [[EMPTY for j in range(8)] for i in range(8)]
    turn: int = 0

    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    display_board(board)


if __name__ == "__main__":
    main()
