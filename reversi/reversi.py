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
    """指定されたセルに指定された色の石を置く。
    Args:
        board (np.ndarray): 盤面を表すNumPy配列
        r (int): 行番号(0-indexed)
        c (int): 列番号(0-indexed)
        color (int): 色
    Returns:
        Bool: 石を置くことができれば真、そうでなければ偽
    """

    # 盤面をコピーする
    nboard = board.copy()
    # 石を置くことのできる場所の候補の情報を取得する
    candidate = get_candidate(nboard, color)
    # 指定されたセルに置いても石を1つも得られないなら、そのセルに石を置くことができない。
    if np.sum(candidate, axis=2)[r, c] == 0:
        return None

    # 指定されたセルに石を置く。
    nboard[r, c] = color

    # 石を裏返す
    # 8方向それぞれについて走査する
    for i, (dr, dc) in enumerate(zip(DR, DC)):
        # その方向に対して1つも石が裏返らないならスキップする
        if candidate[r, c, i] == 0:
            continue
        # 走査中の行番号と列番号
        nr: int = r
        nc: int = c
        # 走査していく
        while True:
            nr += dr
            nc += dc

            # 置いた石と同じ色の石にたどり着いたら終了する
            if nboard[nr, nc] == color:
                break
            # 石を裏返していく
            nboard[nr, nc] = color

    # 処理後の盤面を返す
    return nboard


def get_candidate(board: np.ndarray, color: int) -> np.ndarray:
    """そのセルに石を置いたことによって何枚の石が裏返るかの情報を返す

    Args:
        board (np.ndarray): 盤面を表すNumPy配列
        color (int): 石の色
    Return:
        np.ndarray: そのセルに石を置いたことによって得られる、各方向における石の枚数
        を表したNumPy3次元配列
    """

    # 結果を格納するNumPy配列
    result: np.ndarray = np.array(
        [[[0 for k in range(8)] for j in range(8)] for i in range(8)], dtype=np.int32
    )
    # 全てのセルに対して走査
    for i, j in itertools.product(range(8), repeat=2):
        # 空でないセルには石を置けないのでスキップする
        if board[i, j] != EMPTY:
            continue

        # 8方向について走査する
        for k, (dr, dc) in enumerate(zip(DR, DC)):
            r: int = i
            c: int = j
            count: int = 0

            # 石をおけるかどうかの真偽値
            ok: bool = False

            # 走査開始
            while True:
                r += dr
                c += dc

                # 盤面の外に出てはいけない
                if not (0 <= r < 8 and 0 <= c < 8):
                    break

                # 途中に空白が現れたら中止
                if board[r, c] == EMPTY:
                    break

                # 途中に空白が無く、指定した色と同じ色が現れたら、その間にある石を裏返せるので
                # okにTrueを設定して終了する
                if board[r, c] == color:
                    ok = True
                    break
                else:
                    # 指定した色でない色は裏返る
                    count += 1

            # カウントした個数を記録する
            # 裏返せないなら0が設定される
            result[i, j, k] = count if ok else 0

    # 結果を返す
    return result


def main():
    # 盤面を表す2次元配列
    board: np.ndarray = np.array(
        [[EMPTY for j in range(8)] for i in range(8)], dtype=np.int32
    )
    # 現在のターンを表す変数
    turn: int = 0

    # 初期状態
    board[3, 3] = WHITE
    board[3, 4] = BLACK
    board[4, 3] = BLACK
    board[4, 4] = WHITE

    # 1つ前の盤面の状態を記録しておくバックアップ変数
    # 無効な入力が与えられたときに盤面を巻き戻すために使用する
    board_backup: np.ndarray = board.copy()

    # CUIをクリアする
    os.system("clear")
    # 盤面を表示する
    print(display_board(board))
    print("")

    # ゲームを開始する
    while True:
        # 盤面上の石の数を数える
        white_count: int = np.count_nonzero(board == WHITE)
        black_count: int = np.count_nonzero(board == BLACK)
        # 盤面が全て埋まったらゲームを終了する
        if white_count + black_count == 64:
            print("Game set.")
            if white_count > black_count:
                print("Winner: WHITE.")
            elif white_count < black_count:
                print("Winner: BLACK.")
            break

        # どちらかの石がゼロになった時点でもゲームを終了する
        if white_count == 0:
            print("Game set.")
            print("Winner: BLACK")
            break
        elif black_count == 0:
            print("Game set.")
            print("Winner: WHITE")
            break

        # 石を置ける場所の候補を取得する
        candidate = get_candidate(board, turn)
        # 現在のターンのプレイヤーが石を置けない場合は、ターンを更新する
        if np.sum(candidate) == 0:
            print("")
            print(f"Player {turn} cannot put stone. Turn has been passed.")
            turn = 1 - turn
            candidate = get_candidate(board, turn)

        # ゲーム情報を表示する
        print("Current Turn: {}".format("WHITE" if turn == 0 else "BLACK"))
        # 石をおける場所のヒントを表示する
        print(
            "Candidate space is:",
            *[
                (i, j)
                for i, j in itertools.product(range(8), repeat=2)
                if np.sum(candidate, axis=2)[i, j] != 0
            ],
        )
        # プレイヤーからの入力を受け取る
        S: str = input(
            (
                "Enter row and column numbers of where you want to "
                "put the stone, separated by spaces: "
            )
        )

        # 受け取った入力を分解する
        try:
            r, c = map(int, S.split())
        except ValueError:
            # 無効な入力が与えられた場合はエラーメッセージを表示してもう一度入力を促す
            os.system("clear")
            print(display_board(board))
            print("")
            print("[ERROR}: Invalid input. Enter valid input again.", file=sys.stderr)
            continue

        # 石を置く処理を実施する
        board = put_stone(board, r, c, turn)
        # 石を置けないセルが指定されていた場合、盤面を巻き戻して入力し直させる
        if board is None:
            board = board_backup.copy()

            os.system("clear")
            print(display_board(board))
            print("")
            print("[ERROR]: Cannot put the stone there. Enter valid input again.")
            continue

        # ターンを更新する
        turn = 1 - turn
        # バックアップを取る
        board_backup = board.copy()

        # 表示を更新する
        os.system("clear")
        print(display_board(board))
        print("")


if __name__ == "__main__":
    main()
