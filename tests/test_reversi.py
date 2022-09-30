from typing import List
import pytest
import sys
import io
from reversi import reversi


def test_display_board(capsys, monkeypatch):

    board: List[List[int]] = [[reversi.EMPTY for j in range(8)] for i in range(8)]
    monkeypatch.setattr("sys.stdin", io.StringIO())

    reversi.display_board(board)

    captured, _ = capsys.readouterr()

    assert captured == (
        "   0 1 2 3 4 5 6 7\n"
        "  ----------------\n"
        "0|                \n"
        "1|                \n"
        "2|                \n"
        "3|                \n"
        "4|                \n"
        "5|                \n"
        "6|                \n"
        "7|                \n"
    )

    board[3][3] = reversi.WHITE
    board[3][4] = reversi.BLACK
    board[4][3] = reversi.BLACK
    board[4][4] = reversi.WHITE

    reversi.display_board(board)

    captured, _ = capsys.readouterr()

    assert captured == (
        "   0 1 2 3 4 5 6 7\n"
        "  ----------------\n"
        "0|                \n"
        "1|                \n"
        "2|                \n"
        "3|       o x      \n"
        "4|       x o      \n"
        "5|                \n"
        "6|                \n"
        "7|                \n"
    )
