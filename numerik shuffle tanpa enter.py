# 
import os
import time
import random
from termcolor import colored

# Deteksi OS & fungsi input real-time
try:
    import msvcrt  # Windows
    def get_key():
        return msvcrt.getch().decode('utf-8').lower()
except ImportError:
    import sys
    import tty
    import termios
    def get_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# Konfigurasi
SIZE = 3
SCORE_FILE = "scores.txt"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_solvable(nums):
    inv = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j] and nums[j] != 0:
                inv += 1
    return inv % 2 == 0

def create_board(size):
    nums = list(range(size * size))
    while True:
        random.shuffle(nums)
        if is_solvable(nums):
            break
    return [nums[i*size:(i+1)*size] for i in range(size)]

def display_board(board, moves):
    clear()
    print("=== 15 Puzzle ===\n")
    for row in board:
        for val in row:
            tile = "   " if val == 0 else f"{val:2d} "
            print(colored(tile, 'cyan', 'on_grey') if val != 0 else colored(tile, 'white', 'on_white'), end="")
        print()
    print(f"\nLangkah: {moves} (Tekan q untuk keluar)\n")

def find_blank(board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                return i, j

def move_tile(board, key):
    i, j = find_blank(board)
    di = {'w': 1, 's': -1, 'a': 0, 'd': 0}
    dj = {'w': 0, 's': 0, 'a': 1, 'd': -1}
    ni, nj = i + di.get(key, 0), j + dj.get(key, 0)
    if 0 <= ni < SIZE and 0 <= nj < SIZE:
        board[i][j], board[ni][nj] = board[ni][nj], board[i][j]
        return True
    return False

def is_solved(board):
    expected = list(range(1, SIZE*SIZE)) + [0]
    flat = [val for row in board for val in row]
    return flat == expected

def save_score(name, moves, duration):
    with open(SCORE_FILE, 'a') as f:
        f.write(f"{name},{moves},{duration:.2f}\n")

def show_scores():
    try:
        with open(SCORE_FILE, 'r') as f:
            lines = f.readlines()
            lines.sort(key=lambda x: float(x.strip().split(',')[2]))
            print("\n=== Top Skor ===")
            for i, line in enumerate(lines[:5], 1):
                name, moves, dur = line.strip().split(',')
                print(f"{i}. {name} - {moves} langkah, {dur} detik")
    except FileNotFoundError:
        print("Belum ada skor.")

def main():
    name = input("Masukkan nama Anda: ")
    board = create_board(SIZE)
    moves = 0
    start = time.time()

    while True:
        display_board(board, moves)
        key = get_key()
        if key == 'q':
            print("Keluar dari permainan.")
            break
        if key in 'wasd':
            if move_tile(board, key):
                moves += 1
            if is_solved(board):
                duration = time.time() - start
                display_board(board, moves)
                print(colored(f"🎉 Selamat, {name}! Selesai dalam {moves} langkah dan {duration:.2f} detik", 'green'))
                save_score(name, moves, duration)
                show_scores()
                break

main()
