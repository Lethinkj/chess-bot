"""
Strong Chess Engine using Stockfish
A powerful chess engine for educational purposes and practice.
"""

import chess
import chess.svg
import os
import sys
from typing import Optional, Tuple
import platform


class ChessEngine:
    """A powerful chess engine wrapper using Stockfish."""
    
    def __init__(self, skill_level: int = 20, depth: int = 20, think_time: float = 2.0):
        """
        Initialize the chess engine.
        
        Args:
            skill_level: Engine strength from 0 (weakest) to 20 (strongest/unbeatable)
            depth: Search depth for move analysis
            think_time: Time in seconds for the engine to think per move
        """
        self.board = chess.Board()
        self.skill_level = skill_level
        self.depth = depth
        self.think_time = think_time
        self.stockfish = None
        self.move_history = []
        
        self._init_stockfish()
    
    def _init_stockfish(self):
        """Initialize Stockfish engine."""
        try:
            from stockfish import Stockfish
            
            # Try common Stockfish paths
            stockfish_paths = []
            
            if platform.system() == "Windows":
                stockfish_paths = [
                    "stockfish.exe",
                    "stockfish",
                    r"C:\stockfish\stockfish.exe",
                    r"C:\Program Files\Stockfish\stockfish.exe",
                    os.path.join(os.path.dirname(__file__), "stockfish.exe"),
                ]
            else:
                stockfish_paths = [
                    "stockfish",
                    "/usr/bin/stockfish",
                    "/usr/local/bin/stockfish",
                    "/usr/games/stockfish",
                    os.path.join(os.path.dirname(__file__), "stockfish"),
                ]
            
            stockfish_path = None
            for path in stockfish_paths:
                if os.path.exists(path) or self._check_command_exists(path):
                    stockfish_path = path
                    break
            
            if stockfish_path:
                self.stockfish = Stockfish(
                    path=stockfish_path,
                    depth=self.depth,
                    parameters={
                        "Skill Level": self.skill_level,
                        "Threads": 4,
                        "Hash": 256,
                        "Minimum Thinking Time": int(self.think_time * 1000)
                    }
                )
                print(f"Stockfish initialized at skill level {self.skill_level}/20")
            else:
                print("WARNING: Stockfish not found. Please install it.")
                print("Download from: https://stockfishchess.org/download/")
                self.stockfish = None
                
        except ImportError:
            print("Stockfish module not installed. Run: pip install stockfish")
            self.stockfish = None
        except Exception as e:
            print(f"Error initializing Stockfish: {e}")
            self.stockfish = None
    
    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists in system PATH."""
        import shutil
        return shutil.which(command) is not None
    
    def reset(self):
        """Reset the board to starting position."""
        self.board = chess.Board()
        self.move_history = []
        if self.stockfish:
            self.stockfish.set_position([])
        print("Board reset to starting position.")
    
    def display_board(self):
        """Display the current board state in ASCII."""
        print("\n" + "=" * 40)
        print(self.board)
        print("=" * 40)
        print(f"Turn: {'White' if self.board.turn else 'Black'}")
        print(f"FEN: {self.board.fen()}")
        if self.board.is_check():
            print("CHECK!")
        print()
    
    def get_legal_moves(self) -> list:
        """Get all legal moves in current position."""
        return [move.uci() for move in self.board.legal_moves]
    
    def make_move(self, move_str: str) -> bool:
        """
        Make a move on the board.
        
        Args:
            move_str: Move in UCI format (e.g., 'e2e4') or SAN format (e.g., 'e4')
        
        Returns:
            True if move was legal and made, False otherwise.
        """
        try:
            # Try UCI format first
            move = chess.Move.from_uci(move_str)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move_str)
                if self.stockfish:
                    self.stockfish.set_position(self.move_history)
                return True
        except ValueError:
            pass
        
        try:
            # Try SAN format
            move = self.board.parse_san(move_str)
            if move in self.board.legal_moves:
                uci_move = move.uci()
                self.board.push(move)
                self.move_history.append(uci_move)
                if self.stockfish:
                    self.stockfish.set_position(self.move_history)
                return True
        except ValueError:
            pass
        
        print(f"Illegal move: {move_str}")
        print(f"Legal moves: {', '.join(self.get_legal_moves()[:10])}...")
        return False
    
    def get_best_move(self) -> Optional[str]:
        """Get the best move from Stockfish."""
        if not self.stockfish:
            return self._get_fallback_move()
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            best_move = self.stockfish.get_best_move_time(int(self.think_time * 1000))
            return best_move
        except Exception as e:
            print(f"Engine error: {e}")
            return self._get_fallback_move()
    
    def _get_fallback_move(self) -> Optional[str]:
        """Get a random legal move as fallback."""
        import random
        legal_moves = list(self.board.legal_moves)
        if legal_moves:
            return random.choice(legal_moves).uci()
        return None
    
    def engine_move(self) -> Optional[str]:
        """Make the engine play its best move."""
        if self.is_game_over():
            return None
        
        best_move = self.get_best_move()
        if best_move:
            self.make_move(best_move)
            return best_move
        return None
    
    def get_evaluation(self) -> dict:
        """Get position evaluation from Stockfish."""
        if not self.stockfish:
            return {"type": "none", "value": 0}
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            evaluation = self.stockfish.get_evaluation()
            return evaluation
        except Exception:
            return {"type": "none", "value": 0}
    
    def get_top_moves(self, n: int = 3) -> list:
        """Get top N moves with evaluations."""
        if not self.stockfish:
            return []
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            return self.stockfish.get_top_moves(n)
        except Exception:
            return []
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board.is_game_over()
    
    def get_game_result(self) -> str:
        """Get the result of the game."""
        if not self.is_game_over():
            return "Game in progress"
        
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn else "White"
            return f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            return "Stalemate - Draw!"
        elif self.board.is_insufficient_material():
            return "Insufficient material - Draw!"
        elif self.board.is_fifty_moves():
            return "50-move rule - Draw!"
        elif self.board.is_repetition():
            return "Threefold repetition - Draw!"
        else:
            return "Game over - Draw!"
    
    def undo_move(self) -> bool:
        """Undo the last move."""
        if len(self.move_history) > 0:
            self.board.pop()
            self.move_history.pop()
            if self.stockfish:
                self.stockfish.set_position(self.move_history)
            return True
        return False
    
    def set_difficulty(self, level: int):
        """
        Set engine difficulty.
        
        Args:
            level: 0-20, where 20 is the strongest (virtually unbeatable)
        """
        self.skill_level = max(0, min(20, level))
        if self.stockfish:
            self.stockfish.update_engine_parameters({"Skill Level": self.skill_level})
        print(f"Difficulty set to {self.skill_level}/20")
    
    def analyze_position(self) -> str:
        """Analyze the current position."""
        evaluation = self.get_evaluation()
        top_moves = self.get_top_moves(3)
        
        analysis = []
        analysis.append("\n=== Position Analysis ===")
        
        if evaluation["type"] == "cp":
            score = evaluation["value"] / 100
            analysis.append(f"Evaluation: {score:+.2f} pawns")
            if score > 2:
                analysis.append("White is winning")
            elif score > 0.5:
                analysis.append("White has an advantage")
            elif score < -2:
                analysis.append("Black is winning")
            elif score < -0.5:
                analysis.append("Black has an advantage")
            else:
                analysis.append("Position is roughly equal")
        elif evaluation["type"] == "mate":
            analysis.append(f"Mate in {evaluation['value']} moves!")
        
        if top_moves:
            analysis.append("\nBest moves:")
            for i, move_info in enumerate(top_moves, 1):
                move = move_info.get("Move", "?")
                centipawn = move_info.get("Centipawn")
                mate = move_info.get("Mate")
                
                if mate:
                    analysis.append(f"  {i}. {move} (Mate in {mate})")
                elif centipawn is not None:
                    analysis.append(f"  {i}. {move} ({centipawn/100:+.2f})")
                else:
                    analysis.append(f"  {i}. {move}")
        
        return "\n".join(analysis)
    
    def export_pgn(self) -> str:
        """Export the game in PGN format."""
        import chess.pgn
        import io
        from datetime import datetime
        
        game = chess.pgn.Game()
        game.headers["Event"] = "Practice Game"
        game.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
        game.headers["White"] = "Human"
        game.headers["Black"] = "ChessEngine"
        game.headers["Result"] = "*"
        
        node = game
        temp_board = chess.Board()
        for move_uci in self.move_history:
            move = chess.Move.from_uci(move_uci)
            node = node.add_variation(move)
            temp_board.push(move)
        
        if self.is_game_over():
            if self.board.is_checkmate():
                game.headers["Result"] = "0-1" if self.board.turn else "1-0"
            else:
                game.headers["Result"] = "1/2-1/2"
        
        exporter = io.StringIO()
        exporter.write(str(game))
        return exporter.getvalue()


def main():
    """Main function to run the chess engine."""
    print("=" * 50)
    print("    CHESS ENGINE - Educational Practice Tool")
    print("=" * 50)
    print("\nInitializing engine...")
    
    engine = ChessEngine(skill_level=20, depth=20, think_time=2.0)
    
    print("\nCommands:")
    print("  [move]  - Make a move (e.g., 'e4', 'e2e4', 'Nf3')")
    print("  'hint'  - Get a hint for the best move")
    print("  'eval'  - Analyze current position")
    print("  'undo'  - Undo last move (undoes 2 to skip engine move)")
    print("  'level [0-20]' - Set difficulty (20 = hardest)")
    print("  'moves' - Show all legal moves")
    print("  'pgn'   - Export game in PGN format")
    print("  'reset' - Start a new game")
    print("  'quit'  - Exit the program")
    print()
    
    engine.display_board()
    
    player_color = input("Play as (w)hite or (b)lack? [w]: ").strip().lower()
    player_is_white = player_color != 'b'
    
    if not player_is_white:
        print("\nEngine is playing as White...")
        move = engine.engine_move()
        if move:
            print(f"Engine plays: {move}")
        engine.display_board()
    
    while True:
        if engine.is_game_over():
            print("\n" + "=" * 50)
            print(engine.get_game_result())
            print("=" * 50)
            print("\nGame over! Type 'reset' to play again or 'quit' to exit.")
        
        try:
            cmd = input("\nYour move: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not cmd:
            continue
        
        cmd_lower = cmd.lower()
        
        if cmd_lower == 'quit' or cmd_lower == 'exit':
            print("Thanks for playing!")
            break
        
        elif cmd_lower == 'reset':
            engine.reset()
            engine.display_board()
            player_color = input("Play as (w)hite or (b)lack? [w]: ").strip().lower()
            player_is_white = player_color != 'b'
            if not player_is_white:
                print("\nEngine is playing as White...")
                move = engine.engine_move()
                if move:
                    print(f"Engine plays: {move}")
                engine.display_board()
            continue
        
        elif cmd_lower == 'hint':
            best = engine.get_best_move()
            if best:
                print(f"Hint: Consider playing {best}")
            continue
        
        elif cmd_lower == 'eval':
            print(engine.analyze_position())
            continue
        
        elif cmd_lower == 'undo':
            # Undo player's move and engine's response
            engine.undo_move()
            engine.undo_move()
            engine.display_board()
            continue
        
        elif cmd_lower.startswith('level'):
            parts = cmd_lower.split()
            if len(parts) == 2:
                try:
                    level = int(parts[1])
                    engine.set_difficulty(level)
                except ValueError:
                    print("Usage: level [0-20]")
            else:
                print(f"Current level: {engine.skill_level}/20")
            continue
        
        elif cmd_lower == 'moves':
            moves = engine.get_legal_moves()
            print(f"Legal moves ({len(moves)}): {', '.join(moves)}")
            continue
        
        elif cmd_lower == 'pgn':
            print("\n" + engine.export_pgn())
            continue
        
        # Try to make the move
        if engine.is_game_over():
            print("Game is over. Type 'reset' to start a new game.")
            continue
        
        if engine.make_move(cmd):
            engine.display_board()
            
            if not engine.is_game_over():
                print("Engine is thinking...")
                engine_move = engine.engine_move()
                if engine_move:
                    print(f"Engine plays: {engine_move}")
                engine.display_board()


if __name__ == "__main__":
    main()
