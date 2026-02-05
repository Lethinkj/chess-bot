# Chess Arena - Quick Start Guide

## Starting a Game

1. **Launch the application:**
   ```bash
   python chess_gui.py
   ```

2. **Select Time Control** (before clicking New Game):
   - **No limit**: Unlimited thinking time (good for blitz training)
   - **1 min**: Blitz format
   - **3 min**: Blitz plus
   - **5 min**: Rapid blitz
   - **10 min**: Rapid
   - **15 min**: Rapid plus

3. **Click "New Game"** and choose your color
   - Yes = Play as White (you move first)
   - No = Play as Black (engine moves first)

## During the Game

### Clocks
- **White Clock**: Shows time remaining for White player
- **Black Clock**: Shows time remaining for Black player
- Shows as **∞** for unlimited time control
- Shows **MM:SS** format for timed games
- **Clocks only count during opponent's turn** (not during your thinking)

### Using Hints
- **"Get Hint" button**: Shows the engine's best move
- **Limited to 5 hints per match** (no time limit on reading)
- Hint counter shows: `Hints: X / 5`
- Hints reset when you start a new game

### Game Actions
| Action | Purpose |
|--------|---------|
| **New Game** | Start a fresh game (resets hints & board) |
| **Get Hint** | See engine's best move (max 5 per game) |
| **Analyze** | Deep analysis with top 5 moves |
| **Flip Board** | Change board orientation |
| **Undo Move** | Take back 2 moves (your move + engine's response) |

## Setting Difficulty

Use the **Difficulty slider** (0-20):
- **0-5**: Beginner (makes mistakes)
- **6-10**: Intermediate
- **11-15**: Advanced
- **16-19**: Expert
- **20**: Maximum (≈3500 ELO, nearly unbeatable)

## Engine Think Time

Select how long the engine thinks per move:
- **0.5s**: Very fast
- **1s**: Fast
- **2s**: Normal (recommended)
- **5s**: Deep analysis

## Status Display

The status line at the top shows:
- **"Your turn - White"**: It's your move
- **"Engine's turn - Black"**: Engine is thinking
- **"Game Over - [result]"**: Game has ended

## Tips for Better Play

1. **Against weaker opponents (level 0-10)**: Can use all 5 hints freely
2. **Against stronger opponents (level 15+)**: Save hints for critical positions
3. **Time management**: In timed games, manage your time like real chess
4. **Analysis mode**: Use "Analyze" to understand positions better after games
5. **Study openings**: Play with high difficulty to learn strong opening moves

## Color Scheme

- **Light blue**: Actions and highlights
- **Green**: Status OK, hints remaining
- **Light gray**: Secondary information
- **Dark theme**: Reduces eye strain during long sessions

## Keyboard & Mouse

- **Click pieces**: Select and move (show valid moves with highlights)
- **Valid moves**: Highlighted in green when piece is selected
- **Game buttons**: Use mouse to click all action buttons

## Resetting a Game

Want to restart?
- Click **"New Game"** button
- Confirm you want a new game
- Choose your color again
- Game board clears and hints reset

## Common Issues

**Time ran out?**
- Game ends immediately, opponent wins
- Start a new game with more time or higher time limit

**Out of hints?** 
- Message shows "No hints remaining"
- Continue playing without hints or start new game

**Engine not responding?**
- Download stockfish: `python download_stockfish.py`
- Engine status shows in bottom left

## Advanced: Analyzing Your Games

After finishing a game:
1. **Don't click "New Game"** yet
2. **Click "Analyze"** to see where you could improve
3. **Flip board** to see from different perspective
4. **"Undo Move"** to try different variations

---
**Chess Arena v2 - Train Hard, Play Smart! ♞**
