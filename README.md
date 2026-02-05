# Chess Engine & Board Analyzer - Educational Tools

A powerful chess toolkit using **Stockfish** (one of the world's strongest chess engines, ~3500+ ELO) for educational purposes, practice, and position analysis.

## Features

### Play Against the Engine
- **Skill Level 20**: Maximum strength - virtually unbeatable at the highest setting
- **Adjustable Difficulty**: 0 (beginner) to 20 (grandmaster+)
- **Position Analysis**: Get detailed evaluation and best move suggestions
- **Smart Hint System**: 5 hints per match (no time limit on reading hints)
- **Time-Based Match Options**: Play with time controls:
  - No Limit (unlimited thinking time)
  - Blitz: 1 minute, 3 minutes, 5 minutes
  - Rapid: 10 minutes, 15 minutes
- **Real-Time Clocks**: Live countdown timers for both players
- **Modern Web-Like UI**: Professional dark theme with responsive design

### Analyze Positions from Any Website
- **Board Analyzer**: Capture and analyze positions from any chess website
- **Arrow Overlay**: Shows best move arrows directly on your screen
- **Quick Analyzer**: Hotkey-based analysis (Ctrl+Shift+A)
- **Multiple Lines**: See top 1-5 best moves with evaluations

## Installation

The dependencies should already be installed. If not:

```bash
pip install -r requirements.txt
pip install mss pillow pyautogui keyboard opencv-python numpy
python download_stockfish.py
```

## Usage

### 1. Arrow Overlay (Recommended for Website Analysis)

Shows analysis arrows directly on top of any chess board on your screen:

```bash
python arrow_overlay.py
```

**How to use:**
1. Open any chess website with a game
2. Measure the board position (X, Y coordinates) and size in pixels
3. Click "Show Overlay Position" - adjust until grid aligns with squares
4. Copy the FEN from the website (most sites have a "Copy FEN" option)
5. Paste FEN and click "Analyze"
6. Arrows appear over the board showing best moves!

### 2. Quick Analyzer (Hotkey-based)

Floating analysis panel with hotkey support:

```bash
python quick_analyzer.py
```

**Hotkeys:**
- `Ctrl+Shift+V` = Paste FEN and analyze
- `Ctrl+Shift+A` = Analyze current FEN

### 3. Board Analyzer (Full GUI)

Complete analysis tool with screen capture:

```bash
python board_analyzer.py
```

### 4. Play Against Engine - GUI

**Modern Graphical Interface with Time Controls:**
```bash
python chess_gui.py
```

**Features:**
- ♞ **Time-Based Matches**: Select from 6 time control options (No Limit, 1min, 3min, 5min, 10min, 15min)
- ⏱️ **Real-Time Clocks**: Watch countdown timers as you play
- 💡 **Smart Hints**: Get 5 hints per match (no time pressure to read them)
- 🎯 **Adjustable Difficulty**: Scale from 0 (beginner) to 20 (expert)
- 📊 **Position Evaluation**: Live evaluation score shown during play
- 📜 **Move History**: Complete game transcript
- 🔍 **Position Analysis**: Analyze any position with top 5 moves
- 🎨 **Modern UI**: Professional dark theme optimized for long sessions

**How to Play:**
1. Click "New Game" and choose your color (White or Black)
2. Select desired time control before starting
3. Make moves by clicking pieces
4. Use "Get Hint" if you're stuck (limited to 5 hints per match)
5. Watch the clocks count down during play
6. Game ends on checkmate, stalemate, or timeout

**Command-Line Interface:**
```bash
python chess_engine.py
```

## Difficulty Levels

| Level | Description |
|-------|-------------|
| 0-5   | Beginner (makes mistakes) |
| 6-10  | Intermediate |
| 11-15 | Advanced |
| 16-19 | Expert |
| 20    | Maximum Strength (≈3500+ ELO) |

At level 20 with sufficient think time, this engine is stronger than any human player in history!

## Tips for Improving Your Game

1. **Analyze your games**: Use the `eval` command to understand positions
2. **Study tactics**: Practice against lower difficulty levels first
3. **Learn openings**: See what moves the engine plays in the opening
4. **Review mistakes**: Use `undo` and try different moves

## Files

| File | Description |
|------|-------------|
| `arrow_overlay.py` | Shows analysis arrows on top of any chess board |
| `quick_analyzer.py` | Quick analyzer with hotkey support |
| `board_analyzer.py` | Full GUI analyzer with screen capture |
| `chess_gui.py` | Graphical chess game interface |
| `chess_engine.py` | Command-line chess interface |
| `download_stockfish.py` | Downloads Stockfish engine |
| `stockfish.exe` | Stockfish engine binary |
| `requirements.txt` | Python dependencies |

## How to Get FEN from Chess Websites

Most chess websites allow you to copy the FEN (position notation):

- **Lichess**: Click the hamburger menu → "FEN & PGN" → Copy FEN
- **Chess24**: Right-click board → "Copy FEN"
- **Other sites**: Look for "Share" or "Analysis" options

**Tip**: FEN looks like this: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`

## Educational Purpose

This toolkit is designed for:
- Learning chess strategy and tactics
- Analyzing positions from completed games
- Practicing against a strong opponent
- Understanding chess engine evaluation
- Studying openings and endgames
- Improving your chess skills

**Important**: These tools analyze positions for learning. Use them ethically:
- ✅ Analyze your completed games
- ✅ Study positions from chess books/videos
- ✅ Practice against the engine locally
- ✅ Learn from engine suggestions after games

## Credits

- [Stockfish](https://stockfishchess.org/) - Open source chess engine
- [python-chess](https://python-chess.readthedocs.io/) - Chess library for Python
