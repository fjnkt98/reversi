from typing import List
import pytest
import sys
import io
import numpy as np
from reversi import reversi


def test_display_board():
    board: np.ndarray = np.array(
        [[reversi.EMPTY for j in range(8)] for i in range(8)], dtype=np.int32
    )

    assert reversi.display_board(board) == (
        "   0 1 2 3 4 5 6 7\n"
        "  ----------------\n"
        "0|                \n"
        "1|                \n"
        "2|                \n"
        "3|                \n"
        "4|                \n"
        "5|                \n"
        "6|                \n"
        "7|                "
    )

    board[3, 3] = reversi.WHITE
    board[3, 4] = reversi.BLACK
    board[4, 3] = reversi.BLACK
    board[4, 4] = reversi.WHITE

    reversi.display_board(board)

    assert reversi.display_board(board) == (
        "   0 1 2 3 4 5 6 7\n"
        "  ----------------\n"
        "0|                \n"
        "1|                \n"
        "2|                \n"
        "3|       o x      \n"
        "4|       x o      \n"
        "5|                \n"
        "6|                \n"
        "7|                "
    )


def test_get_candidate():
    board: np.ndarray = np.array(
        [
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 0, 1, -1, -1, -1],
            [-1, -1, -1, 1, 0, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
        ]
    )

    case: np.ndarray = np.array(
        [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    assert np.array_equal(np.sum(reversi.get_candidate(board, 0), axis=2), case)

    board = np.array(
        [
            [-1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, -1, -1, -1, -1, -1, -1],
            [1, -1, 1, -1, -1, -1, -1, -1],
            [1, -1, -1, 1, -1, -1, -1, -1],
            [1, -1, -1, -1, 1, -1, -1, -1],
            [1, -1, -1, -1, -1, 1, -1, -1],
            [1, -1, -1, -1, -1, -1, 1, -1],
            [0, -1, -1, -1, -1, -1, -1, 0],
        ]
    )

    case = np.array(
        [
            [18, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    assert np.array_equal(np.sum(reversi.get_candidate(board, 0), axis=2), case)

    board = np.array(
        [
            [-1, 1, 1, 1, 0, 1, 1, 0],
            [1, 1, -1, -1, -1, -1, -1, -1],
            [1, -1, 1, -1, -1, -1, -1, -1],
            [1, -1, -1, 1, -1, -1, -1, -1],
            [1, -1, -1, -1, 1, -1, -1, -1],
            [1, -1, -1, -1, -1, 1, -1, -1],
            [1, -1, -1, -1, -1, -1, 1, -1],
            [0, -1, -1, -1, -1, -1, -1, 0],
        ]
    )

    case = np.array(
        [
            [15, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    )

    assert np.array_equal(np.sum(reversi.get_candidate(board, 0), axis=2), case)
