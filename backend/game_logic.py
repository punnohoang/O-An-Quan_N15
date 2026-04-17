# -*- coding: utf-8 -*-
"""
game_logic.py - Engine game O An Quan
======================================
Bo cuc ban (12 o, index 0-11):
  index 0  : o Quan TRAI  (chu so huu: top)
  index 1-5: 5 o dan hang TREN (player top)
  index 6  : o Quan PHAI  (chu so huu: bottom)
  index 7-11: 5 o dan hang DUOI (player bottom)

Chieu di vong: 0->1->...->11->0 (CW, direction=+1)
               0->11->...->1->0 (CCW, direction=-1)

Luat diem:
  - Moi quan dan  = 1 diem
  - Moi quan quan = 5 diem

Trang thai ban dau:
  - Moi o dan: 5 quan dan
  - Moi o Quan: 1 quan quan

Luat choi (theo tai lieu):
  1. Chon 1 o dan ben minh co quan, chon chieu.
  2. Boc toan bo quan, rai tung quan mot theo chieu.
  3. Sau khi rai het quan:
       a) O ke tiep co quan (bat ke o dan hay o Quan):
            boc len rai tiep (lien hoan rai).
       b) O ke tiep trong:
            -> Kiem tra an: o sau o trong co quan (va khong phai Quan non)
               thi an, roi tiep tuc kiem tra.
            -> O sau cung trong HOAC la o Quan: mat luot.
  4. Quan non: o Quan co < 5 quan -> KHONG duoc an o Quan do.
  5. Muon quan: khi den luot ma ca 5 o dan deu trong:
       - Lay 5 quan tu kho cua chinh minh, chia moi o 1 quan.
       - Neu kho < 5: vay them tu kho doi thu (ghi no).
       - Neu tong cong van < 5: xu thua (game ket thuc).
  6. Ket thuc: khi CA HAI o Quan deu het quan (== 0).
       - Thu het quan dan con lai cua ca 2 ben vao kho tuong ung.
       - Tinh diem, tru no, xac dinh winner.
"""

import copy

# --- Hang so -------------------------------------------------------------------

NUM_PITS           = 12
QUAN_INDICES       = {0, 6}
TOP_PITS           = list(range(1, 6))
BOTTOM_PITS        = list(range(7, 12))

INITIAL_STONES     = 5   # quan dan moi o dan ban dau
INITIAL_QUAN_COUNT = 1   # so quan quan trong moi o Quan ban dau
QUAN_POINT_VALUE   = 5   # 1 quan quan = 5 diem
QUAN_NON_THRESHOLD = 5   # o Quan co < 5 quan -> quan non, khong duoc an
REFILL_COUNT       = 5   # so quan can de rai lai khi het o dan


# --- Khoi tao ------------------------------------------------------------------

def make_board():
    board = [0] * NUM_PITS
    board[0] = INITIAL_QUAN_COUNT
    board[6] = INITIAL_QUAN_COUNT
    for i in TOP_PITS + BOTTOM_PITS:
        board[i] = INITIAL_STONES
    return board


def make_state(first_player="bottom"):
    return {
        "board":          make_board(),
        "scores":         {"top": 0, "bottom": 0},
        "current_player": first_player,
        "status":         "playing",   # "playing" | "finished"
        "winner":         None,
        "debt":           {"top": 0, "bottom": 0},  # no muon quan
    }


# --- Tien ich ------------------------------------------------------------------

def get_player_pits(player):
    return TOP_PITS if player == "top" else BOTTOM_PITS


def opponent(player):
    return "bottom" if player == "top" else "top"


def next_index(idx, direction):
    return (idx + direction) % NUM_PITS


def is_quan(idx):
    return idx in QUAN_INDICES


def point_value(idx, count):
    """Gia tri diem khi an 'count' quan tu o idx."""
    if is_quan(idx):
        return count * QUAN_POINT_VALUE
    return count


def is_quan_non(board, idx):
    """
    Kiem tra o Quan co phai 'quan non' khong.
    Quan non: o Quan co so quan < QUAN_NON_THRESHOLD (< 5).
    """
    return is_quan(idx) and board[idx] < QUAN_NON_THRESHOLD


def both_quan_empty(board):
    """Kiem tra ca 2 o Quan deu het quan -> dieu kien ket thuc game."""
    return board[0] == 0 and board[6] == 0


# --- Nuoc di hop le ------------------------------------------------------------

def get_valid_moves(state):
    """
    Tra ve [(pit_index, direction), ...]
    Chi o dan cua nguoi choi hien tai co quan moi duoc chon.
    """
    player = state["current_player"]
    board  = state["board"]
    moves  = []
    for pit in get_player_pits(player):
        if board[pit] > 0:
            moves.append((pit, 1))
            moves.append((pit, -1))
    return moves


# --- Rai quan ------------------------------------------------------------------

def sow(board, start, direction):
    """
    Boc toan bo quan o 'start', rai tung quan mot theo direction.
    Tra ve (board_moi, last_index) - o cuoi cung nhan quan.
    O xuat phat bi bo qua neu di vong qua no.
    """
    board  = list(board)
    stones = board[start]
    board[start] = 0
    current = start
    while stones > 0:
        current = next_index(current, direction)
        if current == start:
            current = next_index(current, direction)
        board[current] += 1
        stones -= 1
    return board, current


# --- An quan (lien hoan) -------------------------------------------------------

def capture(board, scores, last, direction, player):
    """
    Sau khi rai xong tai 'last', kiem tra va an quan lien hoan.

    Quy tac (theo tai lieu):
      gap    = o ke tiep sau last
      target = o ke tiep sau gap

      - board[gap] == 0:
          + target co quan VA khong phai quan non:
              an het target, tiep tuc tu target.
          + target trong HOAC la quan non: DUNG (mat luot).
      - board[gap] > 0: DUNG (mat luot).

    Luu y: KHONG an o Quan neu o do la quan non (< 5 quan).

    Tra ve (board_moi, scores_moi, total_points_gained).
    """
    board  = list(board)
    scores = dict(scores)
    total  = 0

    while True:
        gap    = next_index(last, direction)
        target = next_index(gap, direction)

        if board[gap] != 0:
            break   # o ke co quan -> dung

        if board[target] == 0:
            break   # o sau trong -> dung

        if is_quan_non(board, target):
            break   # quan non -> khong duoc an, dung

        # An target
        gained_pieces  = board[target]
        gained_points  = point_value(target, gained_pieces)
        board[target]  = 0
        scores[player] += gained_points
        total          += gained_points
        last = target

    return board, scores, total


# --- Muon quan (het o dan) -----------------------------------------------------

def handle_refill(board, scores, debt, player):
    """
    Khi den luot ma ca 5 o dan cua player deu trong:
      - Can REFILL_COUNT (5) quan de rai lai.
      - Lay tu kho cua chinh minh truoc.
      - Neu kho chinh minh khong du, vay them tu kho doi thu (ghi no).
      - Neu tong cong van < 5: tra ve can_continue=False (xu thua).

    Tra ve (board_moi, scores_moi, debt_moi, can_continue).
    """
    board  = list(board)
    scores = dict(scores)
    debt   = dict(debt)

    pits = get_player_pits(player)
    opp  = opponent(player)

    # Kiem tra co thuc su het o dan khong
    if any(board[p] > 0 for p in pits):
        return board, scores, debt, True   # van con quan, khong can muon

    needed = REFILL_COUNT
    taken  = 0

    # Lay tu kho chinh minh
    from_self = min(needed, scores[player])
    scores[player] -= from_self
    taken += from_self

    # Neu van thieu, vay tu kho doi thu
    if taken < needed:
        from_opp = min(needed - taken, scores[opp])
        scores[opp] -= from_opp
        debt[player] += from_opp
        taken += from_opp

    if taken < needed:
        # Khong du quan de tiep tuc -> xu thua
        return board, scores, debt, False

    # Rai lai: moi o 1 quan
    for p in pits:
        board[p] = 1

    return board, scores, debt, True


# --- Ap dung nuoc di hoan chinh ------------------------------------------------

def apply_move(state, pit, direction):
    """
    Thuc hien mot nuoc di hoan chinh theo dung luat:
      1. Rai lien hoan (o ke tiep co quan -> boc rai tiep, ke ca o Quan)
      2. An quan lien hoan (khong an quan non)
      3. Kiem tra ket thuc (ca 2 o Quan het quan)
      4. Xu ly muon quan neu den luot ma het o dan
      5. Chuyen luot

    Tra ve state moi.
    """
    state    = copy.deepcopy(state)
    board    = state["board"]
    scores   = state["scores"]
    player   = state["current_player"]
    debt     = state["debt"]

    # --- Buoc 1: Rai lien hoan ------------------------------------------------
    # Luat: sau khi rai xong, neu o ke tiep (next sau last) co quan -> boc o do rai tiep
    current_pit = pit
    while True:
        board, last = sow(board, current_pit, direction)
        nxt = next_index(last, direction)

        # O ke tiep co quan -> boc o ke tiep do len rai tiep
        if board[nxt] > 0:
            current_pit = nxt
            continue

        # O ke tiep trong -> dung rai
        break

    # --- Buoc 2: An quan lien hoan --------------------------------------------
    board, scores, _ = capture(board, scores, last, direction, player)

    # --- Buoc 3: Kiem tra ket thuc (ca 2 o Quan het) -------------------------
    state["board"]  = board
    state["scores"] = scores
    state["debt"]   = debt

    if both_quan_empty(board):
        board, scores = collect_remaining(board, scores, "top")
        board, scores = collect_remaining(board, scores, "bottom")
        state["board"]  = board
        state["scores"] = scores
        return finalize(state)

    # --- Buoc 4 & 5: Chuyen luot, xu ly muon quan ----------------------------
    next_player = opponent(player)

    # Kiem tra doi thu co can muon quan khong
    next_pits = get_player_pits(next_player)
    if all(board[p] == 0 for p in next_pits):
        board, scores, debt, can_continue = handle_refill(board, scores, debt, next_player)
        state["board"]  = board
        state["scores"] = scores
        state["debt"]   = debt

        if not can_continue:
            # Doi thu khong du quan -> xu thua
            state = finalize(state)
            state["winner"] = player   # nguoi hien tai thang
            return state

    state["current_player"] = next_player
    return state


# --- Thu het quan dan con lai --------------------------------------------------

def collect_remaining(board, scores, player):
    """Thu tat ca quan dan con lai cua player vao kho (1 diem/quan)."""
    board  = list(board)
    scores = dict(scores)
    for pit in get_player_pits(player):
        scores[player] += board[pit]
        board[pit] = 0
    return board, scores


# --- Tinh diem cuoi & xac dinh winner -----------------------------------------

def finalize(state):
    """
    Ket thuc game:
      - Cong quan Quan con tren ban vao kho chu so huu (x QUAN_POINT_VALUE)
      - Tru no muon (debt)
      - Xac dinh winner
    """
    state  = copy.deepcopy(state)
    board  = state["board"]
    scores = state["scores"]
    debt   = state["debt"]

    # Cong quan Quan con tren ban
    scores["top"]    += board[0] * QUAN_POINT_VALUE
    scores["bottom"] += board[6] * QUAN_POINT_VALUE
    board[0] = 0
    board[6] = 0

    # Tru no muon
    for p in ("top", "bottom"):
        scores[p] = max(0, scores[p] - debt[p])

    state["board"]  = board
    state["scores"] = scores
    state["status"] = "finished"

    if state.get("winner") is None:
        if scores["top"] > scores["bottom"]:
            state["winner"] = "top"
        elif scores["bottom"] > scores["top"]:
            state["winner"] = "bottom"
        else:
            state["winner"] = "draw"

    return state


# --- Heuristic cho AI ----------------------------------------------------------

def evaluate(state, ai_player):
    """
    Ham danh gia h(x) cho Minimax.
    Duong = tot cho ai_player, am = tot cho doi thu.
    """
    if state["status"] == "finished":
        s    = state["scores"]
        diff = s[ai_player] - s[opponent(ai_player)]
        if diff > 0:  return 100000
        if diff < 0:  return -100000
        return 0

    board  = state["board"]
    scores = state["scores"]
    opp    = opponent(ai_player)

    # 1. Chenh lech kho
    score_diff = (scores[ai_player] - scores[opp]) * 10

    # 2. Quan dan tren ban
    my_pits  = sum(board[i] for i in get_player_pits(ai_player))
    opp_pits = sum(board[i] for i in get_player_pits(opp))
    pit_diff = (my_pits - opp_pits) * 2

    # 3. Ap luc len o Quan doi thu (chi co gia tri khi Quan >= QUAN_NON_THRESHOLD)
    opp_quan_idx = 0 if opp == "top" else 6
    my_quan_idx  = 6 if opp == "top" else 0
    opp_quan_val = board[opp_quan_idx]
    # Khuyen khich tan cong khi Quan doi thu >= 5 (co the an)
    if opp_quan_val >= QUAN_NON_THRESHOLD:
        quan_pressure = opp_quan_val * 3
    else:
        quan_pressure = 0
    quan_protect = board[my_quan_idx] * 4

    # 4. Mobility
    my_moves  = len(get_valid_moves(state))
    opp_moves = len(get_valid_moves({**state, "current_player": opp}))
    mobility  = (my_moves - opp_moves) * 1

    return score_diff + pit_diff + quan_pressure - quan_protect + mobility
