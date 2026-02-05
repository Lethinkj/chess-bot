# Chess Arena - Web Version (PythonAnywhere Ready)

## Overview

This is the **web-based version** of Chess Arena that you can host on PythonAnywhere for free. Play chess online with Stockfish AI directly in your browser!

## Quick Start

### Local Testing (Before Deployment)

1. **Install Flask**:
   ```bash
   pip install -r requirements-web.txt
   ```

2. **Run the app locally**:
   ```bash
   python app.py
   ```

3. **Open in browser**:
   ```
   http://localhost:5000
   ```

### Deploy to PythonAnywhere

Follow the detailed guide in **[PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)**

Quick summary:
1. Create free PythonAnywhere account
2. Upload files via Git or file manager
3. Create virtual environment
4. Configure web app
5. Reload and access at `your-username.pythonanywhere.com`

## Features

### Game Features
- ♞ **Play chess** against Stockfish AI
- 🎯 **Adjustable difficulty** (0-20 skill level)
- ⏱️ **Time limits** (1, 3, 5, 10 minutes or unlimited)
- 💡 **5 hints per game**
- 📊 **Position analysis** (top 5 moves)
- 📜 **Move history** tracking
- 🏁 **Full game status** (moves, turn, game over)

### UI Features
- 🎨 **Modern dark theme** (optimized for long sessions)
- 📱 **Responsive design** (works on desktop & mobile)
- ⚡ **Instant feedback** (real-time board updates)
- 🎪 **Professional layout** (intuitive controls)

## File Structure

```
chess-arena/
├── app.py                          # Flask backend API
├── wsgi.py                         # PythonAnywhere configuration
├── requirements-web.txt            # Python dependencies
├── templates/
│   └── index.html                  # Web interface
├── static/                         # (Optional) CSS/JS assets
├── PYTHONANYWHERE_DEPLOYMENT.md    # Deployment guide
└── README.md                       # This file
```

## API Endpoints

The Flask backend provides these REST API endpoints:

### Create Game
```
POST /api/new-game
Body: {
  "difficulty": 20,        // 0-20
  "time_limit": 5          // minutes, null for unlimited
}
Response: {
  "success": true,
  "game_id": 1,
  "game": { ... }
}
```

### Make Move
```
POST /api/move/{game_id}
Body: { "move": "e2e4" }
Response: { "success": true, "game": { ... } }
```

### Get Hint
```
GET /api/hint/{game_id}
Response: {
  "success": true,
  "hint": "e2e4",
  "hints_used": 1,
  "max_hints": 5
}
```

### Analyze Position
```
GET /api/analysis/{game_id}
Response: {
  "success": true,
  "analysis": {
    "evaluation": { "type": "cp", "value": 50 },
    "top_moves": [...]
  }
}
```

### Get Game State
```
GET /api/game/{game_id}
Response: { "success": true, "game": { ... } }
```

## Game State Object

Each game returns:
```json
{
  "game_id": 1,
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "pgn": "1. e4",
  "turn": "White",
  "is_check": false,
  "legal_moves": ["a2a3", "a2a4", ...],
  "move_count": 2,
  "hints_used": 0,
  "max_hints": 5,
  "game_over": false,
  "winner": null,
  "reason": null,
  "difficulty": 20,
  "time_limit": 5
}
```

## System Requirements

### For Local Run
- Python 3.8+
- Flask 2.3.3+
- python-chess
- stockfish (optional but recommended)

### For PythonAnywhere
- Free account (automatically Python 3.10+)
- 100MB storage (sufficient for app)
- Virtual environment (configured automatically)

## Stockfish Integration

### Automatic Setup
The app tries to find Stockfish automatically:
1. `stockfish.exe` (Windows)
2. `stockfish` (Linux/Mac)
3. Common installation paths

### Manual Setup
If Stockfish isn't found:
1. Download from: https://stockfishchess.org/download/
2. Extract to your chess-arena folder
3. Rename to `stockfish.exe` (Windows) or `stockfish` (Linux/Mac)

### On PythonAnywhere
- Free tier: Limited to uploaded binary
- Paid tier: Can install via apt-get

## Configuration

### Difficulty Levels
| Level | Strength |
|-------|----------|
| 0-5 | Beginner |
| 6-10 | Intermediate |
| 11-15 | Advanced |
| 16-19 | Expert |
| 20 | Maximum (≈3500 ELO) |

### Time Limits
- **No Limit** - Unlimited thinking
- **1 min** - Blitz
- **3 min** - Blitz Plus
- **5 min** - Rapid Blitz
- **10 min** - Rapid

## Performance

### Expected Performance
- **Game start**: < 1 second
- **Move calculation**: 0.5-2 seconds (depends on difficulty)
- **Hint generation**: 0.5-1 second
- **Position analysis**: 1-3 seconds

### PythonAnywhere Free Tier
- CPU limited (tasks may be throttled)
- Typical delay: 1-3 seconds per move
- Adequate for learning/playing

## Browser Compatibility

Works on:
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## Limitations

### Free PythonAnywhere Tier
- No concurrent users (single instance)
- CPU throttling (slower analysis)
- 100MB storage limit
- Connection must be refreshed daily

### Current Implementation
- No user accounts/save games
- No multiplayer
- No game history database
- Single game per session

## Future Enhancements

Possible additions:
- User authentication & accounts
- Save/load games
- Game history database
- Multiplayer support
- ELO rating system
- Opening book integration
- Endgame tablebases

## Deployment Checklist

- [ ] Create PythonAnywhere account
- [ ] Upload all files
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Create/configure WSGI file
- [ ] Add static files mapping
- [ ] Reload web app
- [ ] Test game creation
- [ ] Test moves
- [ ] Test hints (5 per game)
- [ ] Test analysis
- [ ] Share link!

## Troubleshooting

### Game won't start
- Check browser console (F12) for errors
- Verify Flask app is running
- Check `/api/new-game` endpoint

### Moves not working
- Verify move format (e.g., "e2e4")
- Check if position is legal
- Ensure game is not over

### Stockfish errors
- Check if Stockfish binary is in correct location
- Verify file permissions
- Try downloading latest Stockfish version

### PythonAnywhere issues
- Check error log in Web tab
- Verify virtual environment path
- Ensure all dependencies installed
- Check Python version compatibility

## Support

For issues:
1. Check error logs
2. Verify all files uploaded correctly
3. Ensure dependencies installed
4. Check PythonAnywhere documentation

## License

This is free to use and modify.

## Credits

- **Stockfish** - https://stockfishchess.org/
- **python-chess** - https://python-chess.readthedocs.io/
- **Flask** - https://flask.palletsprojects.com/
- **PythonAnywhere** - https://www.pythonanywhere.com/

---

**Play Chess Online for Free! ♞**

Questions? Check the deployment guide or PythonAnywhere documentation.
