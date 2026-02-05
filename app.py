"""
Chess Arena - Flask Web App
Hostable on PythonAnywhere
"""

from flask import Flask, render_template, request, jsonify
import chess
import os
import sys
from typing import Optional, Dict, List

try:
    from stockfish import Stockfish
except ImportError:
    print("Warning: Stockfish not installed. Install with: pip install stockfish")

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global game state
games = {}
game_counter = 0

class ChessGame:
    """Manages a single chess game."""
    
    def __init__(self, game_id: int, difficulty: int = 20, time_limit: Optional[int] = None):
        self.game_id = game_id
        self.board = chess.Board()
        self.difficulty = difficulty
        self.time_limit = time_limit  # in minutes
        self.stockfish = self._init_stockfish()
        self.move_count = 0
        self.hints_used = 0
        self.max_hints = 5
        self.game_over = False
        self.winner = None
        self.reason = None
    
    def _init_stockfish(self) -> Optional[Stockfish]:
        """Initialize Stockfish engine."""
        try:
            stockfish_path = None
            
            # Try common paths
            paths = [
                "stockfish.exe",
                "stockfish",
                r"C:\stockfish\stockfish.exe",
                os.path.join(os.path.dirname(__file__), "stockfish.exe"),
            ]
            
            for path in paths:
                if os.path.exists(path):
                    stockfish_path = path
                    break
            
            if stockfish_path:
                return Stockfish(
                    path=stockfish_path,
                    depth=20,
                    parameters={
                        "Skill Level": self.difficulty,
                        "Threads": 2,
                        "Hash": 128,
                    }
                )
        except Exception as e:
            print(f"Stockfish error: {e}")
        
        return None
    
    def get_best_move(self, depth: int = 15) -> Optional[str]:
        """Get best move from Stockfish or fallback to heuristic."""
        if self.stockfish:
            try:
                self.stockfish.set_fen_position(self.board.fen())
                return self.stockfish.get_best_move_time(1000)
            except Exception as e:
                print(f"Error getting best move: {e}")
        
        # Fallback: smarter move selection without Stockfish
        return self._get_heuristic_move()
    
    def _get_heuristic_move(self) -> Optional[str]:
        """Get intelligent move using deep evaluation (no engine needed)."""
        best_move = None
        best_score = -float('inf')
        
        for move in self.board.legal_moves:
            score = self._evaluate_move(move)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move.uci() if best_move else None
    
    def _evaluate_move(self, move) -> float:
        """Evaluate a move with detailed scoring."""
        score = 0.0
        
        # 1. CHECKMATE = Instant win
        self.board.push(move)
        if self.board.is_checkmate():
            self.board.pop()
            return 100000
        
        # 2. Check if move puts us in check (invalid logically for human but python-chess prevents)
        in_check = self.board.is_check()
        
        # 3. Escape check = very high priority
        if self.board.is_check() and self.board.turn == chess.WHITE:
            score += 5000
        
        piece = self.board.piece_at(move.to_square)
        moving_piece = self.board.piece_at(move.from_square)
        
        # 4. CAPTURES with piece values
        if self.board.is_capture(move) and piece:
            piece_values = {
                chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3.5,
                chess.ROOK: 5, chess.QUEEN: 9
            }
            capture_value = piece_values.get(piece.piece_type, 1)
            score += capture_value * 100
        
        self.board.pop()
        
        # 5. GIVE CHECK to opponent
        self.board.push(move)
        if self.board.is_check():
            score += 200
        self.board.pop()
        
        # 6. PAWN PROMOTION
        if moving_piece and moving_piece.piece_type == chess.PAWN:
            if (self.board.turn == chess.WHITE and move.to_square >= 56) or \
               (self.board.turn == chess.BLACK and move.to_square < 8):
                score += 5000
        
        # 7. CONTROL CENTER
        center_squares = [chess.D4, chess.E4, chess.D5, chess.E5]
        if move.to_square in center_squares:
            score += 50
        
        # 8. PIECE DEVELOPMENT (not from back rank)
        if moving_piece and moving_piece.piece_type != chess.KING:
            from_rank = move.from_square // 8
            to_rank = move.to_square // 8
            # Reward moving forward
            if self.board.turn == chess.WHITE and to_rank > from_rank:
                score += 30
            elif self.board.turn == chess.BLACK and to_rank < from_rank:
                score += 30
        
        # 9. AVOID HANGING PIECES
        self.board.push(move)
        undefended = self._count_undefended_pieces()
        self.board.pop()
        
        if undefended > 0:
            score -= undefended * 200
        
        # 10. ATTACK OPPONENT'S PIECES
        dest_piece = self.board.piece_at(move.to_square)
        if dest_piece:
            piece_values = {
                chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3.5,
                chess.ROOK: 5, chess.QUEEN: 9
            }
            score += piece_values.get(dest_piece.piece_type, 1) * 50
        
        return score
    
    def _count_undefended_pieces(self) -> int:
        """Count pieces that are under attack and not defended."""
        undefended = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                # Check if piece is attacked
                attackers = list(self.board.attackers(not self.board.turn, square))
                defenders = list(self.board.attackers(self.board.turn, square))
                
                if len(attackers) > len(defenders):
                    piece_values = {
                        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3.5,
                        chess.ROOK: 5, chess.QUEEN: 9
                    }
                    undefended += piece_values.get(piece.piece_type, 1)
        return undefended
    
    def make_move(self, move_uci: str) -> bool:
        """Make a move on the board."""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_count += 1
                self._check_game_over()
                return True
        except Exception:
            pass
        return False
    
    def get_engine_move(self) -> Optional[str]:
        """Get best move and make it."""
        best_move = self.get_best_move()
        
        if best_move and self.make_move(best_move):
            return best_move
        return None
    
    def get_hint(self) -> Optional[str]:
        """Get a hint (limited to 5 per game)."""
        if self.hints_used >= self.max_hints:
            return None
        
        self.hints_used += 1
        return self.get_best_move()
    
    def _check_game_over(self):
        """Check if game is over."""
        if self.board.is_game_over():
            self.game_over = True
            
            if self.board.is_checkmate():
                self.winner = "Black" if self.board.turn == chess.WHITE else "White"
                self.reason = "Checkmate"
            elif self.board.is_stalemate():
                self.winner = "Draw"
                self.reason = "Stalemate"
            elif self.board.is_insufficient_material():
                self.winner = "Draw"
                self.reason = "Insufficient material"
            else:
                self.winner = "Draw"
                self.reason = "Game ended"
    
    def to_dict(self) -> Dict:
        """Convert game state to JSON-serializable dict."""
        return {
            "game_id": self.game_id,
            "fen": self.board.fen(),
            "pgn": str(self.board.move_stack),
            "turn": "White" if self.board.turn == chess.WHITE else "Black",
            "is_check": self.board.is_check(),
            "legal_moves": [move.uci() for move in self.board.legal_moves],
            "move_count": self.move_count,
            "hints_used": self.hints_used,
            "max_hints": self.max_hints,
            "game_over": self.game_over,
            "winner": self.winner,
            "reason": self.reason,
            "difficulty": self.difficulty,
            "time_limit": self.time_limit,
        }


# Routes

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Create a new game."""
    global game_counter
    
    data = request.json
    difficulty = data.get('difficulty', 20)
    time_limit = data.get('time_limit')
    
    game_counter += 1
    game = ChessGame(game_counter, difficulty, time_limit)
    games[game_counter] = game
    
    return jsonify({
        "success": True,
        "game_id": game_counter,
        "game": game.to_dict()
    })

@app.route('/api/game/<int:game_id>')
def get_game(game_id: int):
    """Get game state."""
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    return jsonify({"success": True, "game": game.to_dict()})

@app.route('/api/move/<int:game_id>', methods=['POST'])
def make_move(game_id: int):
    """Make a player move."""
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    data = request.json
    move_uci = data.get('move')
    
    # Handle automatic bot move
    if move_uci == 'auto':
        if game.game_over:
            return jsonify({"error": "Game is over"}), 400
        
        engine_move = game.get_engine_move()
        if not engine_move:
            return jsonify({"error": "Could not generate move"}), 400
        
        return jsonify({"success": True, "game": game.to_dict()})
    
    # Handle user move
    if not move_uci or not game.make_move(move_uci):
        return jsonify({"error": "Invalid move"}), 400
    
    return jsonify({"success": True, "game": game.to_dict()})

@app.route('/api/hint/<int:game_id>')
def get_hint(game_id: int):
    """Get a hint for the current position."""
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    
    hint = game.get_hint()
    if hint is None:
        return jsonify({
            "success": False,
            "error": f"No hints remaining. Used {game.hints_used}/{game.max_hints}"
        }), 400
    
    return jsonify({
        "success": True,
        "hint": hint,
        "hints_used": game.hints_used,
        "max_hints": game.max_hints
    })

@app.route('/api/analysis/<int:game_id>')
def analyze_position(game_id: int):
    """Analyze current position."""
    game = games.get(game_id)
    if not game or not game.stockfish:
        return jsonify({"error": "Game not found or engine unavailable"}), 404
    
    try:
        game.stockfish.set_fen_position(game.board.fen())
        top_moves = game.stockfish.get_top_moves(5)
        evaluation = game.stockfish.get_evaluation()
        
        analysis = {
            "evaluation": evaluation,
            "top_moves": top_moves
        }
        
        return jsonify({"success": True, "analysis": analysis})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Chess Arena API is running"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
