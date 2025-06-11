import os
import random
import time
from termcolor import colored

# ==== Konfigurasi ====
SIZE = 3
FILENAME = "scores.txt"

# ==== Fungsi ====
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_solvable(flat_board):
    inv = 0
    for i in range(len(flat_board)):
        for j in range(i+1, len(flat_board)):
            if flat_board[i] > flat_board[j] != 0:
                inv += 1
    return inv % 2 == 0

def create_board(size):
    nums = list(range(size * size))
    while True:
        random.shuffle(nums)
        if is_solvable(nums):
            break
    return [nums[i*size:(i+1)*size] for i in range(size)]

def display_board(board):
    clear()
    print("==== Numerik Shuffle ====")
    for row in board:
        for val in row:
            if val == 0:
                print(colored("   ", 'white', 'on_white'), end=" ")
            else:
                print(colored(f"{val:2}", 'cyan', 'on_grey'), end=" ")
        print()
    print()

def find_blank(board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                return i, j

def is_solved(board):
    expected = list(range(1, SIZE*SIZE)) + [0]
    flat = [num for row in board for num in row]
    return flat == expected

def move_tile(board, direction):
    i, j = find_blank(board)
    di = {'w': 1, 's': -1, 'a': 0, 'd': 0}
    dj = {'w': 0, 's': 0, 'a': 1, 'd': -1}
    ni, nj = i + di[direction], j + dj[direction]
    if 0 <= ni < SIZE and 0 <= nj < SIZE:
        board[i][j], board[ni][nj] = board[ni][nj], board[i][j]
        return True
    return False

def save_score(name, moves, duration):
    with open(FILENAME, "a") as f:
        f.write(f"{name},{moves},{duration:.2f}\n")

def show_scores():
    print("=== High Scores ===")
    try:
        with open(FILENAME, "r") as f:
            scores = [line.strip().split(",") for line in f.readlines()]
            scores.sort(key=lambda x: float(x[2]))
            for idx, (name, moves, dur) in enumerate(scores[:5], 1):
                print(f"{idx}. {name} - {moves} langkah, {dur} detik")
    except FileNotFoundError:
        print("Belum ada skor tersimpan.")
    print()

# ==== Main ====
def main():
    name = input("Masukkan nama Anda: ")
    board = create_board(SIZE)
    moves = 0
    start = time.time()

    while True:
        display_board(board)
        print("Gunakan W A S D untuk menggerakkan ubin, Q untuk keluar.")
        print(f"Langkah: {moves}")
        cmd = input("Arah: ").lower()
        if cmd == 'q':
            print("Keluar dari permainan.")
            break
        if cmd in ['w', 'a', 's', 'd']:
            if move_tile(board, cmd):
                moves += 1
        if is_solved(board):
            duration = time.time() - start
            display_board(board)
            print(colored(f"🎉 Selamat, {name}! Puzzle selesai dalam {moves} langkah dan {duration:.2f} detik.", 'green'))
            save_score(name, moves, duration)
            show_scores()
            break

main()
