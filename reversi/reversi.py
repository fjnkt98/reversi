from typing import List, Dict, Union
import itertools
import os
import sys
import numpy as np


EMPTY: int = -1
WHITE: int = 0
BLACK: int = 1

DR: List[int] = [0, -1, -1, -1, 0, 1, 1, 1]
DC: List[int] = [1, 1, 0, -1, -1, -1, 0, 1]


def display_board(board: np.ndarray) -> str:
    """盤面の状態を表すフォーマットされた文字列を返す。

    Arg:
        board (np.ndarray): 盤面を表すNumPy配列
    Return:
        str: フォーマットされた文字列
    """

    # セルの数値を対応する文字に変換する辞書
    convert: Dict[int, str] = {
        EMPTY: " ",
        WHITE: "o",
        BLACK: "x",
    }

    # 結果を格納する配列
    result: List[str] = []

    # ヘッダを記録する
    result.append("   {} {} {} {} {} {} {} {}".format(*list(range(8))))
    result.append("  ----------------")
    # 各行を記録する
    for i, row in enumerate(board):
        result.append(
            "{}| {} {} {} {} {} {} {} {}".format(i, *[convert[cell] for cell in row])
        )

    # 改行文字で区切って結合し返す
    return "\n".join(result)


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

    board_backup: np.ndarray = board.copy()

    os.system("clear")
    print(display_board(board))
    print("")

    while True:
        white_count: int = np.count_nonzero(board == WHITE)
        black_count: int = np.count_nonzero(board == BLACK)
        if white_count + black_count == 64:
            print("Game set.")
            if white_count > black_count:
                print("Winner: WHITE.")
            elif white_count < black_count:
                print("Winner: BLACK.")

            break

        if white_count == 0:
            print("Game set.")
            print("Winner: BLACK")
            break
        elif black_count == 0:
            print("Game set.")
            print("Winner: WHITE")
            break

        candidate = get_candidate(board, turn)
        if np.sum(candidate) == 0:
            print("")
            print(f"Player {turn} cannot put stone. Turn has been passed.")
            turn = 1 - turn
            candidate = get_candidate(board, turn)

        print("Current Turn: {}".format("WHITE" if turn == 0 else "BLACK"))
        print(
            "Candidate space is:",
            *[
                (i, j)
                for i, j in itertools.product(range(8), repeat=2)
                if np.sum(candidate, axis=2)[i, j] != 0
            ],
        )
        S: str = input(
            (
                "Enter row and column numbers of where you want to "
                "put the stone, separated by spaces: "
            )
        )

        try:
            r, c = map(int, S.split())
        except ValueError:
            os.system("clear")
            print(display_board(board))
            print("")
            print("[ERROR}: Invalid input. Enter valid input again.", file=sys.stderr)
            continue

        board = put_stone(board, r, c, turn)
        if board is None:
            board = board_backup.copy()

            os.system("clear")
            print(display_board(board))
            print("")
            print("[ERROR]: Cannot put the stone there. Enter valid input again.")
            continue

        turn = 1 - turn
        board_backup = board.copy()

        os.system("clear")
        print(display_board(board))
        print("")


if __name__ == "__main__":
    main()
