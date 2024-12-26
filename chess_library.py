import csv
import os
import threading
from pathlib import Path

import chess
import chess.engine
import chess.svg

import logging
from IPython.display import display, SVG, clear_output
import time
import random

import matplotlib.pyplot as plt
import io
import cairosvg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
from IPython.display import display
from PIL import Image
import time

logging.basicConfig(level=logging.INFO)


class ChessLibrary:
    def __init__(self, output_folder='chess_svgs'):
        self.output_folder = output_folder
        self.move_count = 0
        os.makedirs(self.output_folder, exist_ok=True)
        self.board = chess.Board()
        botDict = {
            "Stockfish": "/Users/marcokaferbeck/Documents/DataAndKnowledgeEngineering/stockfish/stockfish-macos-m1-apple-silicon",
            "LCZero": "/opt/homebrew/Cellar/lc0/0.31.2/libexec/lc0"
        }
        self.bot1Name = random.choice(list(botDict.keys()))
        self.bot2Name = random.choice(list(botDict.keys()))
        self.bot1 = chess.engine.SimpleEngine.popen_uci(botDict[self.bot1Name])
        self.bot2 = chess.engine.SimpleEngine.popen_uci(botDict[self.bot2Name])
        logging.debug(f"Assigned Bots: White - {self.bot1Name}, Black - {self.bot2Name}")

    def initialize_game(self):
        self.board.reset()

    def make_move(self, move):
        try:
            uci_move = chess.Move.from_uci(move)
            if uci_move in self.board.legal_moves:
                self.board.push(uci_move)
                logging.debug(f"Move {move} executed.")
            else:
                logging.debug(f"Move {move} is illegal.")
        except ValueError as e:
            logging.debug(f"InvalidMoveError: {e}")


    def play_engine_move(self):
        if self.board.is_game_over():
            logging.debug("Game over.")
            return
        bot = self.bot1 if self.board.turn == chess.WHITE else self.bot2
        result = bot.play(self.board, chess.engine.Limit(time=1.0))
        self.board.push(result.move)
        logging.debug(f"Engine played move: {result.move}")


    def play_full_game(self, max_turns):
        for turn in range(int(max_turns)):
            if self.board.is_game_over():
                return self.evaluate_board()
            bot = self.bot1 if self.board.turn == chess.WHITE else self.bot2
            result = bot.play(self.board, chess.engine.Limit(time=1.0))
            self.board.push(result.move)
        return "Game ended after reaching the maximum number of turns."



    def evaluate_board(self):
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


    def save_result_to_file(self, opening_moves, result, file_path='game_results.csv'):
        moves = opening_moves.split(" ")
        moves = moves[:3]
        moves = moves + [""] * (3 - len(moves))
        file = Path(file_path)
        write_header = not file.is_file()
        with open(file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            if write_header:
                writer.writerow(["move1", "move2", "move3", "Result", "bot1", "bot2"])
            writer.writerow(moves + [result, self.bot1Name, self.bot2Name])
        logging.debug(f"Game result saved to {file_path}")


    def shutdown(self):
        self.bot1.quit()
        self.bot2.quit()
        logging.debug("Chess engines have been shut down.")
        logging.debug("Checking for remaining active threads...")
        active_threads = threading.enumerate()
        for thread in active_threads:
            if thread != threading.main_thread():
                logging.debug(f"Stopping thread: {thread.name}")
                thread.join(timeout=1)


    def make_move_visual(self, move):
        logging.debug("make_move_visual called")
        self.make_move(move)
        self.display_board()
        #time.sleep(0.5)  # Add a short delay to allow the display to update



    def play_full_game_visual(self, max_turns):
        logging.debug("play_full_game_visual called")
        for turn in range(int(max_turns)):
            if self.board.is_game_over():
                self.display_board()
                return self.evaluate_board()
            bot = self.bot1 if self.board.turn == chess.WHITE else self.bot2
            result = bot.play(self.board, chess.engine.Limit(time=1.0))
            self.board.push(result.move)
            self.display_board()
            #time.sleep(0.5)  # Add a short delay to allow the display to update
        self.display_board()
        return "Game ended after reaching the maximum number of turns."



    def save_result_to_file_visual(self, opening_moves, result, file_path='game_results.csv'):
        logging.debug("save_result_to_file_visual called")
        self.save_result_to_file(opening_moves, result, file_path)
        self.display_board()



    def evaluate_board_visual(self):
        logging.debug("evaluate_board_visual called")
        result = self.evaluate_board()
        self.display_board()
        return result



    def shutdown_visual(self):
        logging.debug("shutdown_visual called")
        self.shutdown()
        self.display_board()



    def play_engine_move_visual(self):
        logging.debug("play_engine_move_visual called")
        self.play_engine_move()
        self.display_board()
        #time.sleep(0.5)

    def initialize_game_visual(self):
        logging.debug("initialize_game_visual called")
        self.initialize_game()
        self.display_board()

    def display_board(self):
        clear_output(wait=True)
        svg_data = chess.svg.board(board=self.board)
        file_path_svg = os.path.join(self.output_folder, f"move_{self.move_count}.svg")
        file_path_png = os.path.join(self.output_folder, f"move_{self.move_count}.png")

        # Save SVG
        with open(file_path_svg, 'w') as f:
            f.write(svg_data)

        # Convert SVG to PNG
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=file_path_png)

        self.move_count += 1

    def show_all_boards(self, delay=1.0):
        for i in range(self.move_count):
            file_path = os.path.join(self.output_folder, f"move_{i}.svg")
            clear_output(wait=True)
            display(SVG(filename=file_path))
            time.sleep(delay)

