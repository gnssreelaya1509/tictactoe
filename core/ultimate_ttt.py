class UltimateTTTEngine:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = [None] * 9
        self.current_player = 'X'
        self.winner = None
        self.winning_combo_idx = None  # NEW: Tracks which combo index won the match

        self.WIN_COMBOS = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows (Indices 0, 1, 2)
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns (Indices 3, 4, 5)
            [0, 4, 8], [2, 4, 6]             # Diagonals (Indices 6, 7)
        ]

    def make_move(self, idx: int) -> bool:
        if self.winner or self.board[idx] is not None:
            return False

        self.board[idx] = self.current_player

        # Evaluate win matrices and save the combo index
        for combo_idx, combo in enumerate(self.WIN_COMBOS):
            if self.board[combo[0]] and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                self.winner = self.board[combo[0]]
                self.winning_combo_idx = combo_idx  # Save the winning track index
                return True

        if None not in self.board:
            self.winner = "Draw"
            return True

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True