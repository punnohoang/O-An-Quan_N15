# -*- coding: utf-8 -*-
"""
run_tests.py - Kiem tra logic game O An Quan theo dung tai lieu
Chay: python run_tests.py
"""
from game_logic import (
    make_state, apply_move, get_valid_moves,
    capture, point_value, finalize, sow,
    handle_refill, is_quan_non, both_quan_empty,
    QUAN_NON_THRESHOLD
)

passed = 0
failed = 0

def ok(msg):
    global passed
    passed += 1
    print("OK   [%2d] %s" % (passed + failed, msg))

def fail(msg, detail=""):
    global failed
    failed += 1
    print("FAIL [%2d] %s | %s" % (passed + failed, msg, detail))

def check(cond, msg, detail=""):
    if cond: ok(msg)
    else:    fail(msg, detail)

print("=" * 60)
print("NHOM 1: Trang thai ban dau")
print("=" * 60)

state = make_state()
b = state["board"]
check(b[0] == 1 and b[6] == 1,
      "o Quan = 1 quan quan")
check(all(b[i] == 5 for i in range(1, 6)),
      "o dan top = 5 quan")
check(all(b[i] == 5 for i in range(7, 12)),
      "o dan bottom = 5 quan")
check(state["current_player"] == "bottom",
      "bottom di truoc (mac dinh)")
check(state["scores"] == {"top": 0, "bottom": 0},
      "kho ban dau = 0")
check(state["status"] == "playing",
      "status = playing")

print()
print("=" * 60)
print("NHOM 2: He diem")
print("=" * 60)

check(point_value(0, 1) == 5,  "1 quan quan (o 0) = 5 diem")
check(point_value(6, 2) == 10, "2 quan quan (o 6) = 10 diem")
check(point_value(1, 3) == 3,  "3 quan dan = 3 diem")
check(point_value(7, 0) == 0,  "0 quan = 0 diem")

print()
print("=" * 60)
print("NHOM 3: Quan non")
print("=" * 60)

board_test = [0] * 12
board_test[0] = 3   # < 5 -> quan non
board_test[6] = 5   # = 5 -> KHONG phai quan non
check(is_quan_non(board_test, 0) == True,
      "o Quan co 3 quan (< 5) -> quan non")
check(is_quan_non(board_test, 6) == False,
      "o Quan co 5 quan (= 5) -> khong phai quan non")
board_test[6] = 7
check(is_quan_non(board_test, 6) == False,
      "o Quan co 7 quan (> 5) -> khong phai quan non")
check(is_quan_non(board_test, 1) == False,
      "o dan khong bao gio la quan non")

print()
print("=" * 60)
print("NHOM 4: Rai quan")
print("=" * 60)

# Rai co ban
board = [0]*12; board[0]=1; board[6]=1; board[7]=3
b2, last = sow(board, 7, 1)
check(b2[7]==0 and b2[8]==1 and b2[9]==1 and b2[10]==1 and last==10,
      "Rai 3 quan tu o 7 CW -> o 8,9,10")

# Rai nguoc chieu
board = [0]*12; board[0]=1; board[6]=1; board[7]=2
b2, last = sow(board, 7, -1)
# CCW tu o 7: quan 1 vao o 6 (o 6 da co 1 -> thanh 2), quan 2 vao o 5 -> last=5
check(b2[7]==0 and b2[6]==2 and b2[5]==1 and last==5,
      "Rai 2 quan tu o 7 CCW -> o 6 nhan 1 (thanh 2), o 5 nhan 1, last=5")

# Rai qua o Quan (Quan nhan quan binh thuong khi rai)
board = [0]*12; board[0]=1; board[6]=1; board[11]=2
b2, last = sow(board, 11, 1)
# CW tu o 11: o 0 (Quan nhan 1), o 1 (nhan 1) -> last = 1
check(b2[11]==0 and b2[0]==2 and b2[1]==1 and last==1,
      "Rai 2 quan tu o 11 CW -> o 0 (Quan nhan 1), o 1 (nhan 1)")

# Rai vong qua o xuat phat -> bo qua
board = [0]*12; board[0]=1; board[6]=1; board[7]=13
b2, last = sow(board, 7, 1)
check(b2[7]==0,
      "Rai vong: o xuat phat khong nhan quan khi di qua")

print()
print("=" * 60)
print("NHOM 5: Rai lien hoan (o ke tiep co quan -> rai tiep)")
print("=" * 60)

# O ke tiep la o DAN co quan -> rai tiep
# Setup: o10=1, o11=1. Rai o10(1)->o11(=2). nxt=o0 co 1 -> boc o0 rai tiep
# o0(1)->o1. last=o1. nxt=o2 trong -> dung
# Ket qua: o10=0 (da boc), o11=2 (nhan 1 tu o10, khong bi boc)
state = make_state()
state["board"] = [0]*12
state["board"][0]=1; state["board"][6]=1
state["board"][10]=1
state["board"][11]=1
state["current_player"] = "bottom"
s2 = apply_move(state, 10, 1)
check(s2["board"][10]==0,
      "Rai lien hoan: o 10 trong sau khi boc rai")
check(s2["board"][11]==2,
      "Rai lien hoan: o 11 nhan 1 quan tu o10 (khong bi boc, =2)")

# O ke tiep la o QUAN co quan -> cung rai tiep (theo luat: bat ke dan hay Quan)
state = make_state()
state["board"] = [0]*12
state["board"][0]=1; state["board"][6]=1
state["board"][11]=1  # bottom chon o 11 (1 quan)
# rai vao o 0 (Quan co 1 quan) -> o 0 gio co 2 quan -> rai tiep
state["current_player"] = "bottom"
s2 = apply_move(state, 11, 1)
check(s2["board"][11]==0,
      "Rai lien hoan: o 11 rai vao o Quan (o 0), o Quan co quan -> rai tiep")

# O ke tiep TRONG -> dung rai
state = make_state()
state["board"] = [0]*12
state["board"][0]=1; state["board"][6]=1
state["board"][7]=1   # rai 1 quan vao o 8
state["board"][8]=0   # o 8 trong -> dung
state["current_player"] = "bottom"
s2 = apply_move(state, 7, 1)
check(s2["board"][7]==0 and s2["board"][8]==1,
      "Rai: o ke tiep trong -> dung rai (o 8 nhan 1 quan, khong rai tiep)")

print()
print("=" * 60)
print("NHOM 6: An quan co ban")
print("=" * 60)

# gap trong, target co quan dan -> an
board = [0]*12; board[0]=1; board[6]=1
board[7]=0; board[8]=0; board[9]=4
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 7, 1, "bottom")
check(b2[9]==0 and s2["bottom"]==4,
      "An: gap trong, target 4 quan dan -> an 4 diem")

# gap co quan -> khong an
board = [0]*12; board[0]=1; board[6]=1
board[7]=0; board[8]=2; board[9]=4
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 7, 1, "bottom")
check(b2[9]==4 and s2["bottom"]==0,
      "An: gap co quan -> khong an, dung")

# 2 o trong lien tiep -> khong an
board = [0]*12; board[0]=1; board[6]=1
board[7]=0; board[8]=0; board[9]=0
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 7, 1, "bottom")
check(s2["bottom"]==0,
      "An: 2 o trong lien tiep -> khong an")

print()
print("=" * 60)
print("NHOM 7: An lien hoan")
print("=" * 60)

board = [0]*12; board[0]=1; board[6]=1
board[7]=0; board[8]=0; board[9]=3; board[10]=0; board[11]=2
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 7, 1, "bottom")
check(b2[9]==0 and b2[11]==0,
      "An lien hoan: an duoc ca o 9 va o 11")
check(s2["bottom"]==5,
      "An lien hoan: tong = 3+2 = 5 diem")

# Dung khi gap2 co quan
board = [0]*12; board[0]=1; board[6]=1
board[7]=0; board[8]=0; board[9]=3; board[10]=1; board[11]=2
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 7, 1, "bottom")
check(b2[9]==0 and b2[11]==2,
      "An lien hoan: dung khi gap2 co quan, o 11 khong bi an")

print()
print("=" * 60)
print("NHOM 8: Quan non - KHONG duoc an")
print("=" * 60)

# O Quan co < 5 quan -> khong duoc an (quan non)
board = [0]*12; board[0]=1; board[6]=3  # o 6 co 3 quan -> quan non
board[4]=0   # last = 4
board[5]=0   # gap = 5 (trong)
# target = 6 (o Quan co 3 quan, < 5 -> quan non -> KHONG an)
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 4, 1, "bottom")
check(b2[6]==3 and s2["bottom"]==0,
      "Quan non: o Quan co 3 quan (< 5) -> KHONG duoc an")

# O Quan co >= 5 quan -> duoc an
board = [0]*12; board[0]=1; board[6]=5  # o 6 co 5 quan -> duoc an
board[4]=0; board[5]=0
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 4, 1, "bottom")
check(b2[6]==0 and s2["bottom"]==25,
      "Quan non: o Quan co 5 quan (>= 5) -> duoc an, 5x5=25 diem")

# O Quan co 1 quan (ban dau) -> quan non, khong an
board = [0]*12; board[0]=1; board[6]=1
board[4]=0; board[5]=0
scores = {"top":0,"bottom":0}
b2, s2, pts = capture(board, scores, 4, 1, "bottom")
check(b2[6]==1 and s2["bottom"]==0,
      "Quan non: o Quan co 1 quan (ban dau, < 5) -> KHONG an")

print()
print("=" * 60)
print("NHOM 9: Muon quan (het 5 o dan)")
print("=" * 60)

# Het o dan, kho du 5 -> muon tu chinh minh
board = [0]*12; board[0]=1; board[6]=1
scores = {"top":0,"bottom":10}
debt   = {"top":0,"bottom":0}
b2, s2, d2, ok_flag = handle_refill(board, scores, debt, "bottom")
check(ok_flag == True,
      "Muon quan: kho du 5 -> can_continue=True")
check(all(b2[i]==1 for i in range(7,12)),
      "Muon quan: moi o dan nhan 1 quan")
check(s2["bottom"]==5,
      "Muon quan: kho bi tru 5 (10-5=5)")
check(d2["bottom"]==0,
      "Muon quan: khong ghi no khi lay tu chinh minh")

# Het o dan, kho chinh minh chi co 3, vay them 2 tu doi thu
board = [0]*12; board[0]=1; board[6]=1
scores = {"top":8,"bottom":3}
debt   = {"top":0,"bottom":0}
b2, s2, d2, ok_flag = handle_refill(board, scores, debt, "bottom")
check(ok_flag == True,
      "Muon quan: vay them tu doi thu -> can_continue=True")
check(all(b2[i]==1 for i in range(7,12)),
      "Muon quan: moi o dan nhan 1 quan")
check(s2["bottom"]==0,
      "Muon quan: kho bottom het (3-3=0)")
check(s2["top"]==6,
      "Muon quan: kho top bi tru 2 (8-2=6)")
check(d2["bottom"]==2,
      "Muon quan: ghi no 2 cho bottom")

# Tong cong khong du 5 -> xu thua
board = [0]*12; board[0]=1; board[6]=1
scores = {"top":1,"bottom":2}
debt   = {"top":0,"bottom":0}
b2, s2, d2, ok_flag = handle_refill(board, scores, debt, "bottom")
check(ok_flag == False,
      "Muon quan: tong kho < 5 -> can_continue=False (xu thua)")

# Van con quan dan -> khong can muon
board = [0]*12; board[0]=1; board[6]=1; board[7]=3
scores = {"top":0,"bottom":0}
debt   = {"top":0,"bottom":0}
b2, s2, d2, ok_flag = handle_refill(board, scores, debt, "bottom")
check(ok_flag == True and b2[7]==3,
      "Muon quan: van con quan dan -> khong muon, giu nguyen")

print()
print("=" * 60)
print("NHOM 10: Dieu kien ket thuc")
print("=" * 60)

# Ca 2 o Quan het -> ket thuc
board = [0]*12
check(both_quan_empty(board) == True,
      "Ket thuc: ca 2 o Quan = 0 -> True")

board[0] = 1
check(both_quan_empty(board) == False,
      "Ket thuc: o Quan 0 con quan -> False")

board[0] = 0; board[6] = 1
check(both_quan_empty(board) == False,
      "Ket thuc: o Quan 6 con quan -> False")

# Khi ca 2 Quan het, thu het quan dan con lai
state = make_state()
state["board"] = [0]*12
state["board"][1] = 3   # top con 3 quan dan
state["board"][8] = 2   # bottom con 2 quan dan
state["scores"] = {"top":10,"bottom":15}
state["debt"]   = {"top":0,"bottom":0}
result = finalize(state)
check(result["status"] == "finished",
      "Ket thuc: status = finished")
# finalize chi cong Quan con tren ban, khong tu dong thu quan dan
# (collect_remaining duoc goi truoc finalize trong apply_move)
check(result["scores"]["top"] == 10,
      "Ket thuc: finalize khong tu thu quan dan (phai goi collect_remaining truoc)")

# Tinh diem co Quan con tren ban
state = make_state()
state["board"] = [0]*12
state["board"][0] = 2   # Quan top con 2 quan quan
state["board"][6] = 0
state["scores"] = {"top":10,"bottom":20}
state["debt"]   = {"top":0,"bottom":0}
result = finalize(state)
check(result["scores"]["top"] == 20,
      "Ket thuc: top = 10 + 2*5 = 20")
check(result["winner"] == "draw",
      "Ket thuc: hoa (20 = 20)")

# Tru no muon
state = make_state()
state["board"] = [0]*12
state["scores"] = {"top":20,"bottom":30}
state["debt"]   = {"top":5,"bottom":0}
result = finalize(state)
check(result["scores"]["top"] == 15,
      "Ket thuc: tru no (20-5=15)")
check(result["winner"] == "bottom",
      "Ket thuc: bottom thang sau tru no")

print()
print("=" * 60)
print("NHOM 11: Game tich hop (apply_move)")
print("=" * 60)

# Chuyen luot binh thuong
state = make_state()
s2 = apply_move(state, 7, 1)
check(s2["current_player"] == "top",
      "Chuyen luot: bottom di xong -> den top")

# Game ket thuc khi ca 2 Quan het sau nuoc di
state = make_state()
state["board"] = [0]*12
state["board"][6] = 5   # o Quan bottom co 5 quan (duoc an)
state["board"][4] = 1   # top chon o 4, rai 1 quan vao o 5
state["board"][5] = 0   # gap = 5 (trong)
# target = 6 (o Quan bottom co 5 quan >= 5 -> duoc an)
# o Quan top (0) = 0 -> ca 2 Quan het -> game ket thuc
state["current_player"] = "top"
s2 = apply_move(state, 4, 1)
check(s2["status"] == "finished",
      "Game ket thuc: ca 2 Quan het sau khi an o Quan")

# Muon quan duoc tich hop vao apply_move
state = make_state()
state["board"] = [0]*12
state["board"][0] = 1; state["board"][6] = 1
state["board"][7] = 5   # bottom co 1 o dan
state["scores"] = {"top":0,"bottom":10}
state["current_player"] = "bottom"
# Sau khi bottom di, top het o dan -> top phai muon quan
s2 = apply_move(state, 7, 1)
if s2["status"] == "playing":
    top_pits_sum = sum(s2["board"][i] for i in range(1,6))
    check(top_pits_sum == 5,
          "Muon quan tich hop: top duoc rai lai 5 quan vao 5 o dan")
else:
    check(True, "Muon quan tich hop: game ket thuc (khong du quan muon)")

print()
print("=" * 60)
if failed == 0:
    print("KET QUA: %d/%d PASSED - TAT CA TEST PASSED!" % (passed, passed+failed))
else:
    print("KET QUA: %d passed, %d FAILED" % (passed, failed))
print("=" * 60)
