import numpy as np
import random as rnd

# Constants for the game
PLAYER_X = 1
PLAYER_O = -1
EMPTY = 0

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)

    def print_board(self):
        print(self.board)

    def is_winner(self, player):
        # Check rows, columns, and diagonals for a win
        return any(np.all(self.board[i, :] == player) for i in range(3)) or \
               any(np.all(self.board[:, i] == player) for i in range(3)) or \
               np.all(np.diag(self.board) == player) or \
               np.all(np.diag(np.fliplr(self.board)) == player)

    def is_draw(self):
        return np.all(self.board != EMPTY)

    def get_available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r, c] == EMPTY]

    def make_move(self, row, col, player):
        self.board[row, col] = player

    def undo_move(self, row, col):
        self.board[row, col] = EMPTY

    def minmax(self, is_maximizing):
        if self.is_winner(PLAYER_X):
            return 1  # X wins
        if self.is_winner(PLAYER_O):
            return -1  # O wins
        if self.is_draw():
            return 0  # Draw

        if is_maximizing:
            best_score = -float('inf')
            for move in self.get_available_moves():
                self.make_move(move[0], move[1], PLAYER_X)
                score = self.minmax(False)
                self.undo_move(move[0], move[1])
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_available_moves():
                self.make_move(move[0], move[1], PLAYER_O)
                score = self.minmax(True)
                self.undo_move(move[0], move[1])
                best_score = min(best_score, score)
            return best_score

    def best_move(self):
        best_score = -float('inf')
        move = None
        for m in self.get_available_moves():
            self.make_move(m[0], m[1], PLAYER_X)
            score = self.minmax(False)
            self.undo_move(m[0], m[1])
            if score > best_score:
                best_score = score
                move = m
        return move
    
    def random_move(self):
        move = None
        available_moves = self.get_available_moves()
        move = rnd.choice(available_moves)
        
        return move 

def play_game():
    first_turn = False
    is_mode_best = True
    turn = input('Who is first? If you want Robot first enter R otherwise P: ')
    mode = input('Select mode if you want play simple mode enter S else H: ')

    if turn == 'R':
        first_turn = True
    if mode == 'S':
        is_mode_best = False
    
    game = TicTacToe()
    while True:
        game.print_board()

        if game.is_draw():
            print("It's a draw!")
            break
        # Player X's turn (AI)
        if first_turn:
            if is_mode_best:
                move = game.best_move()
            else:
                move = game.random_move()
            if move:
                game.make_move(move[0], move[1], PLAYER_X)
                if game.is_winner(PLAYER_X):
                    game.print_board()
                    print("Player X wins!")
                    break
            
            game.print_board()
            if game.is_draw():
                print("It's a draw!")
                break
        # Player O's turn (User)
        row, col = map(int, input("Enter your move (row and column): ").split())
        row -= 1
        col -= 1
        if game.board[row, col] == EMPTY:
            game.make_move(row, col, PLAYER_O)
            if game.is_winner(PLAYER_O):
                game.print_board()
                print("Player O wins!")
                break
        else:
            print("Invalid move. Try again.")
        
        first_turn = True

if __name__ == "__main__":
    play_game()