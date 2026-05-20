# core/ultimate_ttt.py

class UltimateTTTEngine:
    def __init__(self):
        # NEW: Permanent session memory counters
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.reset_game()

    def reset_game(self):
        # Notice we do NOT reset the win counters here, only the board!
        self.board = [None] * 9
        self.current_player = 'X'
        self.winner = None
        self.winning_combo_idx = None

        self.WIN_COMBOS = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

    def make_move(self, idx: int) -> bool:
        if self.winner or self.board[idx] is not None:
            return False

        self.board[idx] = self.current_player

        for combo_idx, combo in enumerate(self.WIN_COMBOS):
            if self.board[combo[0]] and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                self.winner = self.board[combo[0]]
                self.winning_combo_idx = combo_idx

                # NEW: Add a point to the winner's total tally
                if self.winner == 'X':
                    self.x_wins += 1
                else:
                    self.o_wins += 1

                return True

        if None not in self.board:
            self.winner = "Draw"
            self.draws += 1  # NEW: Add a point to the tie total
            return True

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True