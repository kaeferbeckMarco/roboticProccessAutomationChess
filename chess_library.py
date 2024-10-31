import csv
import threading
import random
from pathlib import Path
import chess
import chess.engine

class ChessLibrary:
    def __init__(self):
        self.board = chess.Board()

        botDict = {
            "Stockfish": "/Users/marcokaferbeck/Documents/DataAndKnowledgeEngineering/stockfish/stockfish-macos-m1-apple-silicon",
            "LCZero": "/opt/homebrew/Cellar/lc0/0.31.2/libexec/lc0"
        }

        self.bot1Name = random.choice(list(botDict.keys()))
        self.bot2Name = random.choice(list(botDict.keys()))
        self.bot1 = chess.engine.SimpleEngine.popen_uci(botDict[self.bot1Name])
        self.bot2 = chess.engine.SimpleEngine.popen_uci(botDict[self.bot2Name])

        # Randomly assign bots to each side if random.choice([True, False]): self.bot1Name = "Stockfish"
        # self.bot2Name = "LCZero" self.bot1 = chess.engine.SimpleEngine.popen_uci(
        # "/Users/marcokaferbeck/Documents/DataAndKnowledgeEngineering/stockfish/stockfish-macos-m1-apple-silicon")
        # self.bot2 = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/Cellar/lc0/0.31.2/libexec/lc0") else:
        # self.bot1Name = "LCZero" self.bot2Name = "Stockfish" self.bot1 = chess.engine.SimpleEngine.popen_uci(
        # "/opt/homebrew/Cellar/lc0/0.31.2/libexec/lc0") self.bot2 = chess.engine.SimpleEngine.popen_uci(
        # "/Users/marcokaferbeck/Documents/DataAndKnowledgeEngineering/stockfish/stockfish-macos-m1-apple-silicon")

        print(f"Assigned Bots: White - {self.bot1Name}, Black - {self.bot2Name}")

    def initialize_game(self):
        """Resets the board to the initial position."""
        self.board.reset()

    def make_move(self, move):
        """Executes a move on the board using UCI format."""
        try:
            uci_move = chess.Move.from_uci(move)
            if uci_move in self.board.legal_moves:
                self.board.push(uci_move)
                print(f"Move {move} executed.")
            else:
                print(f"Move {move} is illegal.")
        except ValueError as e:
            print(f"InvalidMoveError: {e}")

    def play_full_game(self, max_turns):
        """
        Plays a full game between two bots until max_turns or a game-over condition.
        """
        for turn in range(int(max_turns)):
            if self.board.is_game_over():
                return self.evaluate_board()

            # Choose the appropriate bot based on the current turn
            bot = self.bot1 if self.board.turn == chess.WHITE else self.bot2
            result = bot.play(self.board, chess.engine.Limit(time=1.0))
            self.board.push(result.move)

        # If the maximum number of turns is reached and the game is not over, return a status
        return "Game ended after reaching the maximum number of turns."

    def save_result_to_file(self, opening_moves, result, file_path="game_results.csv"):
        """Saves the opening moves and game result to a specified CSV file."""

        # Ensure opening_moves is a list and pad to 3 moves if necessary
        moves = opening_moves.split(" ")
        moves = moves[:3]  # Limit to the first 3 moves if needed
        moves = moves + [""] * (3 - len(moves))  # Pad with empty strings if fewer than 3 moves

        # Check if we need to add headers to a new file
        file = Path(file_path)
        write_header = not file.is_file()  # Check if file exists

        with open(file_path, mode="a", newline='') as file:
            writer = csv.writer(file)

            # Write the header only once if the file is new
            if write_header:
                writer.writerow(["move1", "move2", "move3", "Result", "bot1", "bot2"])

            # Write the game result as a row
            writer.writerow(moves + [result, self.bot1Name, self.bot2Name])
        print(f"Game result saved to {file_path}")

    def evaluate_board(self):
        """Evaluates the board and returns the result of the game."""
        if self.board.is_checkmate():
            return "White wins!" if self.board.turn == chess.BLACK else "Black wins!"
        elif self.board.is_stalemate():
            return "Draw (stalemate)"
        elif self.board.is_insufficient_material():
            return "Draw (insufficient material)"
        elif self.board.is_seventyfive_moves():
            return "Draw (75-move rule)"
        elif self.board.is_fivefold_repetition():
            return "Draw (fivefold repetition)"
        else:
            return "Game still ongoing"

    def shutdown(self):
        """Closes the chess engines."""
        self.bot1.quit()
        self.bot2.quit()
        print("Chess engines have been shut down.")

        # Check and join active threads
        print("Checking for remaining active threads...")
        active_threads = threading.enumerate()
        for thread in active_threads:
            if thread != threading.main_thread():
                print(f"Stopping thread: {thread.name}")
                thread.join(timeout=1)

    def play_engine_move(self):
        """Let the engine play the next move for the side to move."""
        if self.board.is_game_over():
            print("Game over.")
            return

        # Choose the appropriate bot based on the current turn
        bot = self.bot1 if self.board.turn == chess.WHITE else self.bot2
        result = bot.play(self.board, chess.engine.Limit(time=1.0))
        self.board.push(result.move)
        print(f"Engine played move: {result.move}")