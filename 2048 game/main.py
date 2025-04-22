# ------------------------------------------------------------------------------------------------------
# Project: 2048 - GUI Version
# Author: Arsheya Raj
# Date: 22nd April 2025
#
# A simple 2048 game using Python and Tkinter.
# Features colored tiles, arrow key controls, a game over popup window,
# a score counter, and a restart button.
# -------------------------------------------------------------------------------------------------------

import tkinter as tk
import random

GRID_LEN = 4
TILE_COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}

class Game2048(tk.Frame):
    def __init__(self):
        super().__init__()
        self.master.title("2048 Game")
        self.grid()
        self.score = 0
        self.create_header()
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.master.bind("<Key>", self.key_down)
        self.mainloop()

    def create_header(self):
        header = tk.Frame(self, bg="#faf8ef")
        header.grid(row=0, column=0, sticky="ew", pady=10)

        self.score_label = tk.Label(header, text=f"Score: {self.score}", font=("Verdana", 16, "bold"), bg="#faf8ef")
        self.score_label.pack(side="left", padx=20)

        restart_btn = tk.Button(header, text="Restart", font=("Verdana", 14), command=self.restart_game)
        restart_btn.pack(side="right", padx=20)

    def update_score(self, points):
        self.score += points
        self.score_label.config(text=f"Score: {self.score}")

    def restart_game(self):
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.init_matrix()
        self.update_grid_cells()

    def init_grid(self):
        bg = tk.Frame(self, bg="#bbada0", width=400, height=400)
        bg.grid(row=1, column=0)  # grid position changed to row 1
        for i in range(GRID_LEN):
            row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(bg, bg=TILE_COLORS[0][0], width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(cell, text="", justify=tk.CENTER, font=("Verdana", 24, "bold"), width=4, height=2)
                label.grid()
                row.append(label)
            self.grid_cells.append(row)

    def init_matrix(self):
        self.matrix = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty = [(i, j) for i in range(GRID_LEN) for j in range(GRID_LEN) if self.matrix[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.matrix[i][j] = random.choice([2] * 9 + [4])

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                value = self.matrix[i][j]
                color, fg = TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                cell = self.grid_cells[i][j]
                cell.configure(text=str(value) if value != 0 else "", bg=color, fg=fg)
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        if key in ("Up", "Down", "Left", "Right"):
            if self.move(key):
                self.add_new_tile()
                self.update_grid_cells()
                if self.check_game_over():
                    self.game_over()

    def move(self, direction):
        def slide(row):
            row = [i for i in row if i != 0]
            score_gain = 0
            i = 0
            while i < len(row) - 1:
                if row[i] == row[i + 1]:
                    row[i] *= 2
                    score_gain += row[i]
                    row.pop(i + 1)
                    row.append(0)
                    i += 1
                else:
                    i += 1
            return row + [0] * (GRID_LEN - len(row)), score_gain

        moved = False
        score_gain_total = 0
        old_matrix = [row[:] for row in self.matrix]

        for i in range(GRID_LEN):
            if direction == "Left":
                new_row, score_gain = slide(self.matrix[i])
                self.matrix[i] = new_row
                score_gain_total += score_gain
            elif direction == "Right":
                reversed_row, score_gain = slide(list(reversed(self.matrix[i])))
                self.matrix[i] = list(reversed(reversed_row))
                score_gain_total += score_gain
            elif direction == "Up":
                col = [self.matrix[x][i] for x in range(GRID_LEN)]
                new_col, score_gain = slide(col)
                for x in range(GRID_LEN):
                    self.matrix[x][i] = new_col[x]
                score_gain_total += score_gain
            elif direction == "Down":
                col = [self.matrix[x][i] for x in reversed(range(GRID_LEN))]
                new_col, score_gain = slide(col)
                for x in range(GRID_LEN):
                    self.matrix[GRID_LEN - 1 - x][i] = new_col[x]
                score_gain_total += score_gain

        if self.matrix != old_matrix:
            moved = True
            self.update_score(score_gain_total)
        return moved

    def check_game_over(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                if self.matrix[i][j] == 0:
                    return False
                if j < GRID_LEN - 1 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
                if i < GRID_LEN - 1 and self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
        return True

    def game_over(self):
        over = tk.Toplevel(self)
        over.title("Game Over")
        tk.Label(over, text="Game Over!", font=("Verdana", 32, "bold")).pack(padx=50, pady=30)
        tk.Button(over, text="Quit", font=("Verdana", 16), command=self.master.destroy).pack(pady=20)

if __name__ == "__main__":
    Game2048()
