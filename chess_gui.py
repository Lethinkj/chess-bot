"""
Chess Engine with Graphical Interface
A powerful chess engine with a visual board using tkinter.
"""

import chess
import os
import sys
import threading
from typing import Optional, Tuple, List

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ImportError:
    print("tkinter not available. Please run chess_engine.py for command-line version.")
    sys.exit(1)


class ChessGUI:
    """Graphical chess interface using tkinter."""
    
    LIGHT_SQUARE = "#F0D9B5"
    DARK_SQUARE = "#B58863"
    HIGHLIGHT = "#CDD26A"
    MOVE_HINT = "#829769"
    CHECK_COLOR = "#FF6B6B"
    
    # Unicode chess pieces
    PIECES = {
        'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
        'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
    }
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chess Arena - Engine Trainer")
        self.root.resizable(True, True)
        
        # Get screen dimensions for better default size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1400, int(screen_width * 0.9))
        window_height = min(850, int(screen_height * 0.9))
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Fullscreen state
        self.is_fullscreen = False
        
        self.board = chess.Board()
        self.selected_square = None
        self.valid_moves = []
        self.player_color = chess.WHITE
        self.engine_thinking = False
        self.stockfish = None
        self.skill_level = 20
        self.think_time = 2.0

        # Match options - time-based
        self.time_control_var = tk.StringVar(value="no_limit")
        self.white_time_ms: Optional[int] = None
        self.black_time_ms: Optional[int] = None
        self.clock_job_id: Optional[str] = None
        self.game_in_progress = False

        # Time presets (in minutes)
        self.TIME_PRESETS = {
            "no_limit": None,
            "1": 1 * 60 * 1000,
            "3": 3 * 60 * 1000,
            "5": 5 * 60 * 1000,
            "10": 10 * 60 * 1000,
            "15": 15 * 60 * 1000,
        }

        # Hint usage per game (5 hints without time limit)
        self.max_hints_per_game = 5
        self.hints_used = 0
        
        self._init_stockfish()
        self._create_widgets()
        self._draw_board()
        
        # Keyboard bindings
        self.root.bind("<F11>", lambda e: self._toggle_fullscreen())
        self.root.bind("<Escape>", lambda e: self._exit_fullscreen())
    
    def _init_stockfish(self):
        """Initialize Stockfish engine."""
        try:
            from stockfish import Stockfish
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            stockfish_paths = [
                os.path.join(script_dir, "stockfish.exe"),
                "stockfish.exe",
                "stockfish",
                r"C:\stockfish\stockfish.exe",
            ]
            
            for path in stockfish_paths:
                try:
                    if os.path.exists(path):
                        self.stockfish = Stockfish(
                            path=path,
                            depth=20,
                            parameters={
                                "Skill Level": self.skill_level,
                                "Threads": 4,
                                "Hash": 256,
                            }
                        )
                        print(f"Stockfish loaded from {path}")
                        return
                except Exception as e:
                    continue
            
            # Try system PATH
            import shutil
            if shutil.which("stockfish"):
                self.stockfish = Stockfish(
                    depth=20,
                    parameters={
                        "Skill Level": self.skill_level,
                        "Threads": 4,
                        "Hash": 256,
                    }
                )
                print("Stockfish loaded from system PATH")
                
        except Exception as e:
            print(f"Stockfish not available: {e}")
            print("Please run download_stockfish.py first")
    
    def _create_widgets(self):
        """Create GUI widgets with modern, web-like design."""
        # Modern color scheme
        BG_DARK = "#0f1419"
        BG_MEDIUM = "#1a1d25"
        BG_LIGHT = "#252a33"
        ACCENT_BLUE = "#0066ff"
        ACCENT_GREEN = "#00d084"
        TEXT_PRIMARY = "#ffffff"
        TEXT_SECONDARY = "#a0a5b0"
        
        self.root.config(bg=BG_DARK)
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=BG_DARK)
        main_frame.pack(padx=16, pady=16, fill=tk.BOTH, expand=True)
        
        # Top header with title and game status
        header_frame = tk.Frame(main_frame, bg=BG_DARK)
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        title_label = tk.Label(
            header_frame,
            text="♞ CHESS ARENA ♞",
            font=("Segoe UI", 20, "bold"),
            bg=BG_DARK,
            fg=ACCENT_BLUE,
        )
        title_label.pack(anchor="w")
        
        # Game info section
        info_frame = tk.Frame(main_frame, bg=BG_LIGHT, relief=tk.FLAT)
        info_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Player clocks with modern styling
        clocks_container = tk.Frame(info_frame, bg=BG_LIGHT)
        clocks_container.pack(fill=tk.X, padx=12, pady=8)
        
        # White player
        white_frame = tk.Frame(clocks_container, bg=BG_LIGHT)
        white_frame.pack(side=tk.LEFT, padx=(0, 20))
        tk.Label(white_frame, text="White", font=("Segoe UI", 10, "bold"), bg=BG_LIGHT, fg=TEXT_PRIMARY).pack(anchor="w")
        self.white_clock_label = tk.Label(
            white_frame,
            text="∞",
            font=("Segoe UI", 16, "bold"),
            bg=BG_LIGHT,
            fg=ACCENT_GREEN,
        )
        self.white_clock_label.pack(anchor="w")
        
        # Black player
        black_frame = tk.Frame(clocks_container, bg=BG_LIGHT)
        black_frame.pack(side=tk.LEFT)
        tk.Label(black_frame, text="Black", font=("Segoe UI", 10, "bold"), bg=BG_LIGHT, fg=TEXT_SECONDARY).pack(anchor="w")
        self.black_clock_label = tk.Label(
            black_frame,
            text="∞",
            font=("Segoe UI", 16, "bold"),
            bg=BG_LIGHT,
            fg=TEXT_SECONDARY,
        )
        self.black_clock_label.pack(anchor="w")
        
        # Status and evaluation
        status_eval_frame = tk.Frame(info_frame, bg=BG_LIGHT)
        status_eval_frame.pack(fill=tk.X, padx=12, pady=(0, 8))
        
        self.status_label = tk.Label(
            status_eval_frame, 
            text="Ready for new game",
            font=("Segoe UI", 12, "bold"),
            bg=BG_LIGHT,
            fg=ACCENT_GREEN,
        )
        self.status_label.pack(anchor="w")
        
        self.eval_label = tk.Label(
            status_eval_frame,
            text="Evaluation: 0.00",
            font=("Segoe UI", 10),
            bg=BG_LIGHT,
            fg=TEXT_SECONDARY,
        )
        self.eval_label.pack(anchor="w")
        
        # Content area: Board + Controls side by side
        content_frame = tk.Frame(main_frame, bg=BG_DARK)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Board on the left
        self.square_size = 70
        board_size = self.square_size * 8
        
        self.canvas = tk.Canvas(
            content_frame,
            width=board_size,
            height=board_size,
            highlightthickness=1,
            highlightbackground=BG_MEDIUM,
            bg=BG_MEDIUM,
        )
        self.canvas.pack(side=tk.LEFT, padx=(0, 16))
        self.canvas.bind("<Button-1>", self._on_click)
        
        # Right panel with controls (scrollable)
        control_frame = tk.Frame(content_frame, bg=BG_DARK)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a scrollable canvas for controls
        canvas = tk.Canvas(control_frame, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(control_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_DARK)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Allow mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Time control section
        time_ctrl_frame = tk.Frame(scrollable_frame, bg=BG_LIGHT, relief=tk.FLAT)
        time_ctrl_frame.pack(fill=tk.X, pady=(0, 8))
        
        tk.Label(
            time_ctrl_frame,
            text="Time Control",
            font=("Segoe UI", 10, "bold"),
            bg=BG_LIGHT,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", padx=8, pady=(8, 4))
        
        time_choices_frame = tk.Frame(time_ctrl_frame, bg=BG_LIGHT)
        time_choices_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        choices = [
            ("No limit", "no_limit"),
            ("1 min", "1"),
            ("3 min", "3"),
            ("5 min", "5"),
            ("10 min", "10"),
            ("15 min", "15"),
        ]
        for text, value in choices:
            tk.Radiobutton(
                time_choices_frame,
                text=text,
                value=value,
                variable=self.time_control_var,
                bg=BG_LIGHT,
                fg=TEXT_PRIMARY,
                selectcolor=BG_MEDIUM,
                activebackground=BG_LIGHT,
                activeforeground=ACCENT_BLUE,
                font=("Segoe UI", 9),
            ).pack(side=tk.LEFT, padx=4, pady=2)
        
        # Difficulty and engine settings
        settings_frame = tk.Frame(scrollable_frame, bg=BG_LIGHT, relief=tk.FLAT)
        settings_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            settings_frame,
            text="Difficulty",
            font=("Segoe UI", 10, "bold"),
            bg=BG_LIGHT,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", padx=8, pady=(8, 4))
        
        self.difficulty_var = tk.IntVar(value=20)
        self.difficulty_slider = tk.Scale(
            settings_frame,
            from_=0,
            to=20,
            orient=tk.HORIZONTAL,
            variable=self.difficulty_var,
            command=self._on_difficulty_change,
            bg=BG_LIGHT,
            fg=ACCENT_BLUE,
            highlightthickness=0,
            troughcolor=BG_MEDIUM,
            activebackground=ACCENT_BLUE,
            length=200,
        )
        self.difficulty_slider.pack(fill=tk.X, padx=8, pady=(0, 4))
        
        tk.Label(
            settings_frame,
            text="Engine Think Time (seconds)",
            font=("Segoe UI", 9),
            bg=BG_LIGHT,
            fg=TEXT_SECONDARY,
        ).pack(anchor="w", padx=8, pady=(4, 4))
        
        self.time_var = tk.DoubleVar(value=2.0)
        time_frame = tk.Frame(settings_frame, bg=BG_LIGHT)
        time_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        for t in [0.5, 1, 2, 5]:
            tk.Radiobutton(
                time_frame, 
                text=str(t), 
                variable=self.time_var, 
                value=t,
                bg=BG_LIGHT,
                fg=TEXT_PRIMARY,
                selectcolor=BG_MEDIUM,
                activebackground=BG_LIGHT,
                activeforeground=ACCENT_BLUE,
                font=("Segoe UI", 9),
            ).pack(side=tk.LEFT, padx=4)
        
        # Action buttons
        buttons_frame = tk.Frame(scrollable_frame, bg=BG_LIGHT, relief=tk.FLAT)
        buttons_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(
            buttons_frame,
            text="Actions",
            font=("Segoe UI", 10, "bold"),
            bg=BG_LIGHT,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", padx=8, pady=(8, 4))
        
        btn_container = tk.Frame(buttons_frame, bg=BG_LIGHT)
        btn_container.pack(fill=tk.BOTH, padx=8, pady=(0, 8))
        
        btn_style = {
            "font": ("Segoe UI", 9, "bold"),
            "bg": ACCENT_BLUE,
            "fg": TEXT_PRIMARY,
            "activebackground": "#0052cc",
            "activeforeground": TEXT_PRIMARY,
            "border": 0,
            "padx": 8,
            "pady": 6,
        }
        
        tk.Button(btn_container, text="New Game", command=self._new_game, **btn_style).pack(fill=tk.X, pady=3)
        tk.Button(btn_container, text="Get Hint", command=self._get_hint, **btn_style).pack(fill=tk.X, pady=3)
        tk.Button(btn_container, text="Analyze", command=self._analyze_position, **btn_style).pack(fill=tk.X, pady=3)
        tk.Button(btn_container, text="Flip Board", command=self._flip_board, **btn_style).pack(fill=tk.X, pady=3)
        tk.Button(btn_container, text="Undo Move", command=self._undo_move, **btn_style).pack(fill=tk.X, pady=3)
        tk.Button(btn_container, text="Fullscreen (F11)", command=self._toggle_fullscreen, **btn_style).pack(fill=tk.X, pady=3)

        # Hint usage info
        self.hint_label = tk.Label(
            buttons_frame,
            text=f"Hints: 0 / {self.max_hints_per_game}",
            font=("Segoe UI", 9),
            bg=BG_LIGHT,
            fg=ACCENT_GREEN,
        )
        self.hint_label.pack(anchor="w", padx=8, pady=(0, 8))
        
        # Move history section
        history_frame_outer = tk.Frame(scrollable_frame, bg=BG_LIGHT, relief=tk.FLAT)
        history_frame_outer.pack(fill=tk.BOTH, expand=True, pady=8)
        
        tk.Label(
            history_frame_outer,
            text="Move History",
            font=("Segoe UI", 10, "bold"),
            bg=BG_LIGHT,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", padx=8, pady=(8, 4))
        
        history_frame = tk.Frame(history_frame_outer, bg=BG_MEDIUM)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(
            history_frame,
            width=20,
            height=8,
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set,
            bg=BG_MEDIUM,
            fg=TEXT_PRIMARY,
            insertbackground=ACCENT_BLUE,
            selectbackground=ACCENT_BLUE,
        )
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Engine status
        engine_status = "Ready" if self.stockfish else "Not Available"
        status_color = ACCENT_GREEN if self.stockfish else "#ff4444"
        
        self.engine_label = tk.Label(
            scrollable_frame,
            text=f"Engine: {engine_status}",
            font=("Segoe UI", 8),
            fg=status_color,
            bg=BG_DARK,
        )
        self.engine_label.pack(pady=(4, 8))
    
    def _draw_board(self):
        """Draw the chess board."""
        self.canvas.delete("all")
        
        # Check if king is in check
        check_square = None
        if self.board.is_check():
            king_square = self.board.king(self.board.turn)
            check_square = king_square
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                
                # Calculate actual square index based on board orientation
                if self.player_color == chess.WHITE:
                    square = chess.square(col, 7 - row)
                else:
                    square = chess.square(7 - col, row)
                
                # Determine square color
                light = (row + col) % 2 == 0
                color = self.LIGHT_SQUARE if light else self.DARK_SQUARE
                
                # Highlight selected square
                if square == self.selected_square:
                    color = self.HIGHLIGHT
                # Highlight valid move destinations
                elif square in self.valid_moves:
                    color = self.MOVE_HINT
                # Highlight check
                elif square == check_square:
                    color = self.CHECK_COLOR
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Draw piece
                piece = self.board.piece_at(square)
                if piece:
                    symbol = self.PIECES.get(piece.symbol(), "?")
                    # Make white pieces bright and black pieces dark so they are
                    # clearly distinguishable on both light and dark squares.
                    if piece.color == chess.WHITE:
                        # Slight shadow + white foreground for contrast
                        self.canvas.create_text(
                            x1 + self.square_size // 2 + 1,
                            y1 + self.square_size // 2 + 1,
                            text=symbol,
                            font=("Arial", 42, "bold"),
                            fill="#000000",
                        )
                        self.canvas.create_text(
                            x1 + self.square_size // 2,
                            y1 + self.square_size // 2,
                            text=symbol,
                            font=("Arial", 42, "bold"),
                            fill="#FFFFFF",
                        )
                    else:
                        # Solid black pieces with a light outline
                        self.canvas.create_text(
                            x1 + self.square_size // 2 + 1,
                            y1 + self.square_size // 2 + 1,
                            text=symbol,
                            font=("Arial", 42, "bold"),
                            fill="#FFFFFF",
                        )
                        self.canvas.create_text(
                            x1 + self.square_size // 2,
                            y1 + self.square_size // 2,
                            text=symbol,
                            font=("Arial", 42, "bold"),
                            fill="#000000",
                        )
        
        # Draw coordinates
        for i in range(8):
            # Files (a-h)
            file_label = chr(ord('a') + i) if self.player_color == chess.WHITE else chr(ord('h') - i)
            self.canvas.create_text(
                i * self.square_size + self.square_size // 2,
                8 * self.square_size - 8,
                text=file_label,
                font=("Arial", 10),
                fill="#666"
            )
            
            # Ranks (1-8)
            rank_label = str(8 - i) if self.player_color == chess.WHITE else str(i + 1)
            self.canvas.create_text(
                8,
                i * self.square_size + self.square_size // 2,
                text=rank_label,
                font=("Arial", 10),
                fill="#666"
            )
    
    def _on_click(self, event):
        """Handle board click."""
        if self.engine_thinking:
            return
        
        if self.board.is_game_over():
            return
        
        # Don't allow moves when it's not player's turn
        if self.board.turn != self.player_color:
            return
        
        col = event.x // self.square_size
        row = event.y // self.square_size
        
        if self.player_color == chess.WHITE:
            square = chess.square(col, 7 - row)
        else:
            square = chess.square(7 - col, row)
        
        piece = self.board.piece_at(square)
        
        if self.selected_square is None:
            # Select a piece
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.valid_moves = [
                    move.to_square for move in self.board.legal_moves 
                    if move.from_square == square
                ]
        else:
            # Try to make a move
            if square in self.valid_moves:
                move = self._make_move(self.selected_square, square)
                if move:
                    self._update_after_move()
                    if not self.board.is_game_over():
                        self._engine_move()
            
            self.selected_square = None
            self.valid_moves = []
        
        self._draw_board()
    
    def _make_move(self, from_sq, to_sq) -> Optional[chess.Move]:
        """Make a move, handling promotion if needed."""
        # Check for promotion
        piece = self.board.piece_at(from_sq)
        if piece and piece.piece_type == chess.PAWN:
            to_rank = chess.square_rank(to_sq)
            if (piece.color == chess.WHITE and to_rank == 7) or \
               (piece.color == chess.BLACK and to_rank == 0):
                # Always promote to queen for simplicity
                move = chess.Move(from_sq, to_sq, promotion=chess.QUEEN)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    return move
        
        move = chess.Move(from_sq, to_sq)
        if move in self.board.legal_moves:
            self.board.push(move)
            return move
        
        return None
    
    def _engine_move(self):
        """Make the engine play a move."""
        if not self.stockfish:
            self._update_status("Engine not available!")
            return
        
        self.engine_thinking = True
        self._update_status("Engine thinking...")
        
        def think():
            try:
                self.stockfish.set_fen_position(self.board.fen())
                think_time_ms = int(self.time_var.get() * 1000)
                best_move = self.stockfish.get_best_move_time(think_time_ms)
                
                if best_move:
                    self.root.after(0, lambda: self._apply_engine_move(best_move))
            except Exception as e:
                print(f"Engine error: {e}")
                self.root.after(0, lambda: self._update_status("Engine error!"))
            finally:
                self.engine_thinking = False
        
        thread = threading.Thread(target=think)
        thread.daemon = True
        thread.start()
    
    def _apply_engine_move(self, move_uci: str):
        """Apply the engine's move to the board."""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self._update_after_move()
        except Exception as e:
            print(f"Error applying move: {e}")
        
        self.engine_thinking = False
        self._draw_board()
    
    def _update_after_move(self):
        """Update GUI after a move."""
        self._draw_board()
        self._update_history()
        self._update_evaluation()
        self._start_clock_for_current_player()
        
        if self.board.is_game_over():
            self._show_game_over()
        else:
            turn = "White" if self.board.turn == chess.WHITE else "Black"
            if self.board.turn == self.player_color:
                self._update_status(f"Your turn - {turn}")
            else:
                self._update_status(f"Engine's turn - {turn}")
    
    def _update_status(self, text: str):
        """Update the status label."""
        self.status_label.config(text=text)
        self.root.update_idletasks()
    
    def _update_history(self):
        """Update move history display."""
        self.history_text.delete(1.0, tk.END)
        moves = list(self.board.move_stack)

        # Use a fresh temporary board to generate SAN that is always
        # consistent with the move sequence so we never call san() on
        # an illegal move in the current position.
        temp_board = chess.Board()
        line_parts = []

        for idx, move in enumerate(moves):
            try:
                san = temp_board.san(move)
            except Exception:
                # Fallback: if something goes wrong, just use UCI
                san = move.uci()

            move_number = idx // 2 + 1
            if idx % 2 == 0:
                # White move – start a new line
                line_parts.append(f"{move_number}. {san}")
            else:
                # Black move – append to current line
                line_parts[-1] += f" {san}"

            temp_board.push(move)

        history_text = "\n".join(line_parts) + ("\n" if line_parts else "")
        self.history_text.insert(tk.END, history_text)
        
        self.history_text.see(tk.END)
    
    def _update_evaluation(self):
        """Update position evaluation."""
        if not self.stockfish:
            return
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            evaluation = self.stockfish.get_evaluation()
            
            if evaluation["type"] == "cp":
                score = evaluation["value"] / 100
                self.eval_label.config(text=f"Evaluation: {score:+.2f}")
            elif evaluation["type"] == "mate":
                self.eval_label.config(text=f"Mate in {evaluation['value']}")
        except Exception:
            pass
    
    def _show_game_over(self):
        """Show game over message."""
        self.game_in_progress = False
        self._stop_clock()
        
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            message = f"Checkmate! {winner} wins!"
        elif self.board.is_stalemate():
            message = "Stalemate - Draw!"
        elif self.board.is_insufficient_material():
            message = "Insufficient material - Draw!"
        else:
            message = "Game Over - Draw!"
        
        self._update_status(message)
        messagebox.showinfo("Game Over", message)
    
    def _new_game(self):
        """Start a new game with time control."""
        result = messagebox.askyesnocancel(
            "New Game",
            "Play as White?\n\n(Yes = White, No = Black, Cancel = Cancel)"
        )
        
        if result is None:
            return
        
        # Stop any existing clock
        self._stop_clock()
        
        # Reset board and game state
        self.board = chess.Board()
        self.selected_square = None
        self.valid_moves = []
        self.player_color = chess.WHITE if result else chess.BLACK
        self.game_in_progress = True
        self.hints_used = 0
        
        # Initialize time based on selected control
        time_control = self.time_control_var.get()
        total_time = self.TIME_PRESETS.get(time_control)
        
        if total_time:
            self.white_time_ms = total_time
            self.black_time_ms = total_time
        else:
            self.white_time_ms = None
            self.black_time_ms = None
        
        # Clear history and evaluation
        self.history_text.delete(1.0, tk.END)
        self.eval_label.config(text="Evaluation: 0.00")
        self._update_hint_label()
        self._update_clocks()
        
        # Start the game
        if self.player_color == chess.BLACK:
            self._update_status("Engine thinking...")
            self._draw_board()
            self.root.after(500, self._engine_move)
        else:
            self._update_status("Your turn - White")
            self._draw_board()
    
    def _flip_board(self):
        """Flip the board orientation."""
        self.player_color = not self.player_color
        self._draw_board()
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
    
    def _exit_fullscreen(self):
        """Exit fullscreen mode."""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
    
    def _undo_move(self):
        """Undo the last two moves (player + engine)."""
        if len(self.board.move_stack) >= 2:
            self.board.pop()
            self.board.pop()
        elif len(self.board.move_stack) == 1:
            self.board.pop()
        
        self.selected_square = None
        self.valid_moves = []
        self._update_after_move()
    
    def _get_hint(self):
        """Get a hint for the best move (limited to 5 per match)."""
        if not self.stockfish:
            messagebox.showinfo("Hint", "Engine not available")
            return
        
        if self.board.is_game_over():
            messagebox.showinfo("Hint", "Game is over")
            return
        
        if self.hints_used >= self.max_hints_per_game:
            messagebox.showinfo(
                "Hint",
                f"No hints remaining!\nYou have used {self.hints_used} / {self.max_hints_per_game} hints."
            )
            return
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            best_move = self.stockfish.get_best_move_time(1000)
            if best_move:
                self.hints_used += 1
                self._update_hint_label()
                messagebox.showinfo("Hint", f"Best move: {best_move}")
        except Exception as e:
            messagebox.showinfo("Hint", f"Error: {e}")
    
    def _analyze_position(self):
        """Analyze the current position."""
        if not self.stockfish:
            messagebox.showinfo("Analysis", "Engine not available")
            return
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            top_moves = self.stockfish.get_top_moves(5)
            evaluation = self.stockfish.get_evaluation()
            
            analysis = "Position Analysis\n" + "=" * 30 + "\n\n"
            
            if evaluation["type"] == "cp":
                score = evaluation["value"] / 100
                analysis += f"Evaluation: {score:+.2f} pawns\n\n"
            elif evaluation["type"] == "mate":
                analysis += f"Mate in {evaluation['value']} moves!\n\n"
            
            analysis += "Top moves:\n"
            for i, move_info in enumerate(top_moves, 1):
                move = move_info.get("Move", "?")
                cp = move_info.get("Centipawn")
                mate = move_info.get("Mate")
                
                if mate is not None:
                    analysis += f"{i}. {move} (Mate in {mate})\n"
                elif cp is not None:
                    analysis += f"{i}. {move} ({cp/100:+.2f})\n"
                else:
                    analysis += f"{i}. {move}\n"
            
            messagebox.showinfo("Analysis", analysis)
        except Exception as e:
            messagebox.showinfo("Analysis", f"Error: {e}")
    
    def _on_difficulty_change(self, value):
        """Handle difficulty slider change."""
        level = int(float(value))
        self.skill_level = level
        if self.stockfish:
            try:
                self.stockfish.update_engine_parameters({"Skill Level": level})
            except Exception:
                pass
    
    def _update_hint_label(self):
        """Update the hint usage label."""
        remaining = self.max_hints_per_game - self.hints_used
        self.hint_label.config(
            text=f"Hints: {self.hints_used} / {self.max_hints_per_game}"
        )
    
    def _format_time(self, ms: Optional[int]) -> str:
        """Format milliseconds to MM:SS or return infinity symbol."""
        if ms is None:
            return "∞"
        
        total_seconds = max(0, ms // 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def _update_clocks(self):
        """Update the clock display."""
        white_time_str = self._format_time(self.white_time_ms)
        black_time_str = self._format_time(self.black_time_ms)
        
        self.white_clock_label.config(text=white_time_str)
        self.black_clock_label.config(text=black_time_str)
    
    def _start_clock_for_current_player(self):
        """Start the clock countdown for the current player."""
        self._stop_clock()
        
        # Only run clock if time control is active
        time_control = self.time_control_var.get()
        if time_control == "no_limit" or not self.game_in_progress:
            return
        
        def tick():
            if self.game_in_progress:
                if self.board.turn == chess.WHITE:
                    if self.white_time_ms is not None:
                        self.white_time_ms -= 100
                        if self.white_time_ms <= 0:
                            self.white_time_ms = 0
                            self._end_game_on_timeout("Black", "White out of time!")
                            return
                else:
                    if self.black_time_ms is not None:
                        self.black_time_ms -= 100
                        if self.black_time_ms <= 0:
                            self.black_time_ms = 0
                            self._end_game_on_timeout("White", "Black out of time!")
                            return
                
                self._update_clocks()
                self.clock_job_id = self.root.after(100, tick)
        
        self.clock_job_id = self.root.after(100, tick)
    
    def _stop_clock(self):
        """Stop the active clock."""
        if self.clock_job_id:
            self.root.after_cancel(self.clock_job_id)
            self.clock_job_id = None
    
    def _end_game_on_timeout(self, winner: str, message: str):
        """End game due to timeout."""
        self.game_in_progress = False
        self._stop_clock()
        self._update_status(message)
        messagebox.showinfo("Time Over", f"Game Over!\n{winner} wins!\n{message}")


def main():
    """Main function to run the chess GUI."""
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
