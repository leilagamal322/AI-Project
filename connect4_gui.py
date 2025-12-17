import tkinter as tk
from tkinter import messagebox
from env.connect4_env import Connect4Env
from algos.adversarial_search import alphabeta_search


class Connect4GUI:
    def __init__(self, search_depth: int = 4, human_player: int = 1):
        self.env = Connect4Env()
        self.search_depth = search_depth
        self.human_player = human_player
        self.ai_player = -human_player
        self.cell_size = 80
        self.padding = 20
        self.width = self.env.COLS * self.cell_size + 2 * self.padding
        self.height = (self.env.ROWS + 1) * self.cell_size + 2 * self.padding
        self.root = tk.Tk()
        self.root.title("Connect 4 - Human vs AI")
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="#1E1E1E")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.status_label = tk.Label(self.root, text="", fg="white", bg="#1E1E1E", font=("Arial", 14))
        self.status_label.pack(fill=tk.X)
        self.root.configure(bg="#1E1E1E")
        self.game_over = False
        self.draw_board()
        self.update_status()
        if self.env.current_player == self.ai_player:
            self.root.after(500, self.ai_move)

    def board_to_screen(self, row, col):
        x0 = self.padding + col * self.cell_size
        y0 = self.padding + (row + 1) * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        return x0, y0, x1, y1

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            self.padding,
            self.padding + self.cell_size,
            self.padding + self.env.COLS * self.cell_size,
            self.padding + (self.env.ROWS + 1) * self.cell_size,
            fill="#0047AB",
            outline="#003580",
            width=3,
        )
        for c in range(self.env.COLS):
            x = self.padding + c * self.cell_size + self.cell_size / 2
            self.canvas.create_text(
                x,
                self.padding + self.cell_size / 2,
                text=str(c),
                fill="white",
                font=("Arial", 16, "bold"),
            )
        for r in range(self.env.ROWS):
            for c in range(self.env.COLS):
                x0, y0, x1, y1 = self.board_to_screen(r, c)
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                radius = self.cell_size * 0.35
                self.canvas.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    fill="white",
                    outline="black",
                    width=2,
                )
        for r in range(self.env.ROWS):
            for c in range(self.env.COLS):
                cell = self.env.board[r, c]
                if cell == 0:
                    continue
                x0, y0, x1, y1 = self.board_to_screen(r, c)
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                radius = self.cell_size * 0.35
                if cell == 1:
                    color = "#FF4444"
                    outline = "#AA0000"
                else:
                    color = "#FFD700"
                    outline = "#B8860B"
                self.canvas.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    fill=color,
                    outline=outline,
                    width=2,
                )

    def update_status(self, text: str = None):
        if text is not None:
            self.status_label.config(text=text)
            return
        if self.game_over:
            winner = self.env.check_winner()
            if winner == 1:
                msg = "Game over: Player 1 (X) wins"
            elif winner == -1:
                msg = "Game over: Player 2 (O) wins"
            else:
                msg = "Game over: Draw"
        else:
            if self.env.current_player == self.human_player:
                symbol = "X" if self.human_player == 1 else "O"
                msg = f"Your turn ({symbol}) - click a column"
            else:
                msg = "AI thinking..."
        self.status_label.config(text=msg)

    def handle_click(self, event):
        if self.game_over:
            return
        if self.env.current_player != self.human_player:
            return
        col = int((event.x - self.padding) // self.cell_size)
        if col < 0 or col >= self.env.COLS:
            return
        if not self.env.is_valid_action(col):
            self.update_status("Invalid move, column is full")
            return
        self.env.make_move(col)
        self.draw_board()
        winner = self.env.check_winner()
        if winner is not None:
            self.game_over = True
            self.update_status()
            messagebox.showinfo("Game Over", self.status_label.cget("text"))
            return
        self.update_status()
        self.root.after(200, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
        if self.env.current_player != self.ai_player:
            return
        self.update_status()
        self.root.update_idletasks()
        best_move, tracker = alphabeta_search(self.env, max_depth=self.search_depth)
        if best_move is None:
            self.game_over = True
            self.update_status("Game over: No valid moves")
            messagebox.showinfo("Game Over", "No valid moves")
            return
        self.env.make_move(best_move)
        self.draw_board()
        winner = self.env.check_winner()
        if winner is not None:
            self.game_over = True
            self.update_status()
            messagebox.showinfo("Game Over", self.status_label.cget("text"))
            return
        self.update_status()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = Connect4GUI(search_depth=4, human_player=1)
    gui.run()


