# -*- coding: utf-8 -*-
"""
test_console.py - Choi O An Quan tren console
==============================================
Che do:
  1. Nguoi vs Nguoi (PvP)
  2. Nguoi vs AI    (PvE) - ban la bottom, AI la top
  3. AI vs AI       (demo tu chay)

Cach chay:
  python test_console.py
"""

import sys
import time

from game_logic import make_state, apply_move, get_valid_moves, TOP_PITS, BOTTOM_PITS
from ai import get_ai_move

DIR_LABEL = {1: "-> (CW)", -1: "<- (CCW)"}


# --- Hien thi ban co -----------------------------------------------------------

def print_board(state):
    board  = state["board"]
    scores = state["scores"]
    player = state["current_player"]
    status = state["status"]

    print()
    print("=" * 62)
    if player == "top":
        print("  Luot: TOP (May/B)")
    else:
        print("  Luot: BOTTOM (Nguoi/A)")
    print("  Kho TOP=%d  |  Kho BOTTOM=%d" % (scores["top"], scores["bottom"]))
    print("=" * 62)

    top_row    = [board[i] for i in range(1, 6)]
    bottom_row = [board[i] for i in range(11, 6, -1)]
    ql = board[0]
    qr = board[6]

    top_idx    = "  ".join("[%2d]" % i for i in range(1, 6))
    bottom_idx = "  ".join("[%2d]" % i for i in range(11, 6, -1))

    print()
    print("          " + top_idx)
    print("  Q[0]=%2d  " % ql + "  ".join("  %2d " % v for v in top_row) + "  Q[6]=%2d" % qr)
    print("          " + "-" * 34)
    print("  Q[0]=%2d  " % ql + "  ".join("  %2d " % v for v in bottom_row) + "  Q[6]=%2d" % qr)
    print("          " + bottom_idx)
    print()

    if status == "finished":
        winner = state["winner"]
        print("  *** GAME KET THUC ***")
        if winner == "draw":
            print("  Ket qua: HOA!")
        else:
            print("  Nguoi thang: %s" % winner.upper())
        print("  Diem cuoi -- TOP: %d  |  BOTTOM: %d" % (scores["top"], scores["bottom"]))
        print()


def print_valid_moves(state):
    moves  = get_valid_moves(state)
    player = state["current_player"]
    print("  Nuoc di hop le (%s):" % player)
    for i, (pit, direction) in enumerate(moves):
        print("    [%d] O %d  %s" % (i, pit, DIR_LABEL[direction]))
    return moves


# --- Luot nguoi ---------------------------------------------------------------

def human_turn(state):
    moves = print_valid_moves(state)
    while True:
        try:
            raw = input("  Chon so thu tu nuoc di (hoac 'q' de thoat): ").strip()
            if raw.lower() == "q":
                print("  Thoat game.")
                sys.exit(0)
            idx = int(raw)
            if 0 <= idx < len(moves):
                return moves[idx]
            print("  Vui long nhap so tu 0 den %d." % (len(moves) - 1))
        except ValueError:
            print("  Nhap khong hop le.")


# --- Luot AI ------------------------------------------------------------------

def ai_turn(state, label="AI", depth=4):
    print("  %s dang suy nghi..." % label)
    t0   = time.time()
    move = get_ai_move(state, depth=depth)
    dt   = time.time() - t0
    if move is None:
        print("  %s khong co nuoc di!" % label)
        return None
    pit, direction = move
    print("  %s chon: O %d  %s  (%.2fs)" % (label, pit, DIR_LABEL[direction], dt))
    return move


# --- Vong lap game ------------------------------------------------------------

def run_pvp():
    state = make_state(first_player="bottom")
    print("\n  === CHE DO: NGUOI vs NGUOI ===")
    while state["status"] == "playing":
        print_board(state)
        pit, direction = human_turn(state)
        state = apply_move(state, pit, direction)
    print_board(state)


def run_pve(ai_depth=4):
    state = make_state(first_player="bottom")
    print("\n  === CHE DO: NGUOI (bottom) vs AI (top) ===")
    while state["status"] == "playing":
        print_board(state)
        if state["current_player"] == "bottom":
            pit, direction = human_turn(state)
        else:
            move = ai_turn(state, label="AI (top)", depth=ai_depth)
            if move is None:
                break
            pit, direction = move
        state = apply_move(state, pit, direction)
    print_board(state)


def run_ai_vs_ai(ai_depth=4, delay=0.3):
    state = make_state(first_player="bottom")
    print("\n  === CHE DO: AI vs AI (demo) ===")
    turn = 0
    while state["status"] == "playing":
        print_board(state)
        label = "AI-%s" % state["current_player"].upper()
        move  = ai_turn(state, label=label, depth=ai_depth)
        if move is None:
            break
        pit, direction = move
        state = apply_move(state, pit, direction)
        turn += 1
        time.sleep(delay)
    print_board(state)
    print("  Tong so luot: %d" % turn)


# --- Menu chinh ---------------------------------------------------------------

def main():
    print()
    print("+================================+")
    print("|    O AN QUAN - Console Test    |")
    print("+================================+")
    print("  1. Nguoi vs Nguoi")
    print("  2. Nguoi vs AI")
    print("  3. AI vs AI (demo)")
    print()

    while True:
        choice = input("  Chon che do (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            break
        print("  Vui long nhap 1, 2 hoac 3.")

    if choice == "1":
        run_pvp()
    elif choice == "2":
        run_pve(ai_depth=4)
    else:
        run_ai_vs_ai(ai_depth=4, delay=0.3)


if __name__ == "__main__":
    main()
