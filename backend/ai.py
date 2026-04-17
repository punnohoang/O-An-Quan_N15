"""
ai.py — AI Minimax + Alpha-Beta Pruning cho Ô Ăn Quan
======================================================
Chiến lược:
  1. Ưu tiên nước ăn được ô Quan đối thủ
  2. Ưu tiên nước ăn được nhiều đá nhất
  3. Nếu không có nước ăn → Minimax + Alpha-Beta
  4. Fallback: random
"""

import random
import copy
from game_logic import (
    apply_move, get_valid_moves, evaluate,
    opponent, get_player_pits, is_quan,
    next_index, sow, capture, point_value
)

MAX_DEPTH = 4   # độ sâu Minimax (tăng lên nếu muốn AI mạnh hơn)


# ─── Kiểm tra nhanh nước có ăn được gì không ────────────────────────────────

def simulate_capture_gain(board, scores, pit, direction, player):
    """
    Mô phỏng nhanh một nước đi và trả về:
      (total_captured, captures_quan)
    mà không cần deepcopy toàn bộ state.
    """
    b = list(board)
    s = dict(scores)

    # Rải liên hoàn
    current = pit
    while True:
        b, last = sow(b, current, direction)
        if b[last] > 0 and not is_quan(last):
            current = last
            continue
        break

    # Ăn
    b2 = list(b)
    s2 = dict(s)
    b2, s2, total = capture(b2, s2, last, direction, player)
    gained = s2[player] - s[player]

    # Kiểm tra có ăn được ô Quan đối thủ không
    opp = opponent(player)
    opp_quan = 0 if opp == "top" else 6
    captures_quan = (b[opp_quan] > 0 and b2[opp_quan] == 0)

    return gained, captures_quan


# ─── Rule-based filter ───────────────────────────────────────────────────────

def rule_based_move(state):
    """
    Trả về nước đi tốt nhất theo rule:
      1. Ăn được Quan → chọn ngay
      2. Ăn được nhiều nhất → chọn
      3. Không ăn được gì → trả về None (để Minimax xử lý)
    """
    moves  = get_valid_moves(state)
    board  = state["board"]
    scores = state["scores"]
    player = state["current_player"]

    best_quan  = None
    best_many  = None
    best_gain  = 0

    for pit, direction in moves:
        gained, captures_quan = simulate_capture_gain(board, scores, pit, direction, player)

        if captures_quan:
            best_quan = (pit, direction)
            break   # ưu tiên tuyệt đối

        if gained > best_gain:
            best_gain = gained
            best_many = (pit, direction)

    if best_quan:
        return best_quan
    if best_many:
        return best_many
    return None   # không ăn được gì


# ─── Minimax + Alpha-Beta ────────────────────────────────────────────────────

def minimax(state, depth, alpha, beta, maximizing, ai_player):
    if depth == 0 or state["status"] == "finished":
        return evaluate(state, ai_player), None

    moves = get_valid_moves(state)
    if not moves:
        return evaluate(state, ai_player), None

    best_move = None

    if maximizing:
        value = float("-inf")
        for pit, direction in moves:
            child = apply_move(state, pit, direction)
            score, _ = minimax(child, depth - 1, alpha, beta, False, ai_player)
            if score > value:
                value = score
                best_move = (pit, direction)
            alpha = max(alpha, value)
            if alpha >= beta:
                break   # Beta cut-off
        return value, best_move
    else:
        value = float("inf")
        for pit, direction in moves:
            child = apply_move(state, pit, direction)
            score, _ = minimax(child, depth - 1, alpha, beta, True, ai_player)
            if score < value:
                value = score
                best_move = (pit, direction)
            beta = min(beta, value)
            if alpha >= beta:
                break   # Alpha cut-off
        return value, best_move


# ─── Entry point ─────────────────────────────────────────────────────────────

def get_ai_move(state, depth=MAX_DEPTH):
    """
    Trả về (pit, direction) tốt nhất cho AI.
    Thứ tự ưu tiên:
      1. Rule-based (ăn Quan > ăn nhiều)
      2. Minimax + Alpha-Beta
      3. Random fallback
    """
    moves = get_valid_moves(state)
    if not moves:
        return None

    # 1. Rule-based
    rule_move = rule_based_move(state)
    if rule_move:
        return rule_move

    # 2. Minimax
    ai_player = state["current_player"]
    _, best = minimax(state, depth, float("-inf"), float("inf"), True, ai_player)
    if best:
        return best

    # 3. Fallback random
    return random.choice(moves)
