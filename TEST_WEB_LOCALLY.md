# Test Chess Arena Web Locally

Before deploying to PythonAnywhere, test it locally!

## Prerequisites

✅ Already installed from earlier:
- Python 3.9+
- Flask
- python-chess
- stockfish

## Quick Test (2 minutes)

### 1. Start the Server

Open terminal in the chess folder and run:

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 2. Open in Browser

Click or paste in browser:
```
http://localhost:5000
```

Or go to:
- http://127.0.0.1:5000
- http://localhost:5000

### 3. Test Features

#### ✅ Test 1: Start a Game
- Click **"New Game"** button
- Should see empty chess board
- Status shows "White's Turn"

#### ✅ Test 2: Make Moves
- Click a white pawn (e.g., the e2 pawn)
- Valid moves highlight in green
- Click valid destination to move
- Engine automatically plays Black

#### ✅ Test 3: Get Hint
- Click **"Get Hint"** button
- Shows best move (e.g., "Best move: e7e5")
- Counter shows "Hints Used: 1/5"
- Try getting all 5 hints

#### ✅ Test 4: Difficulty
- Move difficulty slider to 0 (left)
- New Game - engine makes weaker moves
- Move to 20 (right) - engine plays much stronger

#### ✅ Test 5: Time Control
- Click **"10 min"** time button
- New Game
- Timer should show active (not ∞)

#### ✅ Test 6: Analysis
- Make a few moves
- Click **"Analyze"** button
- Shows top moves for current position

#### ✅ Test 7: Check Status
- Move counter increases with each move
- Board highlights correctly
- Game status updates

---

## Browser Console (For Debugging)

Press **F12** in browser to open Developer Tools

### Check for errors:
1. Click **"Console"** tab
2. Look for red text (errors)
3. Common errors:
   - `404 /api/new-game` → Flask app not running
   - `Favicon error` → Ignore, not critical
   - `CORS error` → Shouldn't happen, check Flask

### Network tab:
1. Click **"Network"** tab
2. Make a move
3. Should see requests to `/api/move`
4. Status should be `200 OK`

---

## API Testing (Advanced)

Test API directly without browser:

### Test Game Creation
```bash
curl -X POST http://localhost:5000/api/new-game \
  -H "Content-Type: application/json" \
  -d '{"difficulty": 20, "time_limit": null}'
```

Should return:
```json
{
  "success": true,
  "game_id": 1,
  "game": {
    "game_id": 1,
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    ...
  }
}
```

### Test Move
```bash
curl -X POST http://localhost:5000/api/move/1 \
  -H "Content-Type: application/json" \
  -d '{"move": "e2e4"}'
```

### Test Hint
```bash
curl http://localhost:5000/api/hint/1
```

### Health Check
```bash
curl http://localhost:5000/health
```

Should return:
```json
{"status": "ok", "message": "Chess Arena API is running"}
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
# Then kill the process

# Linux/Mac:
lsof -ti:5000 | xargs kill -9
```

### Module Not Found
```bash
# Make sure virtual environment is active
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate
```

### Stockfish Not Found
- Stockfish still works from API perspective
- Some API calls (hints, analysis) will be slower
- Download stockfish.exe and place in chess folder

### Moves Not Working
- Check browser console (F12)
- Verify `/api/move` response status
- Make sure move is in `legal_moves` list

### Board Not Displaying
- Try refreshing browser (Ctrl+R or Cmd+R)
- Clear browser cache (Ctrl+Shift+Delete)
- Try different browser

---

## Performance Expectations

### Local Testing
- Game start: < 0.5 seconds
- Move response: < 1 second
- Hints: < 1 second
- Analysis: 1-3 seconds
- Should be smooth and responsive

### On PythonAnywhere
- Game start: < 1 second
- Move response: 1-2 seconds
- Hints: 1-2 seconds
- Analysis: 2-5 seconds
- Still playable but slightly slower due to shared server

---

## File Verification

Make sure these files exist:
```
chess-arena/
├── app.py ........................ Main Flask app
├── wsgi.py ....................... PythonAnywhere config
├── requirements-web.txt .......... Dependencies
├── templates/
│   └── index.html ................ Web interface
├── static/ ....................... (Optional)
└── stockfish.exe ................. (Optional)
```

### Check files:
```bash
ls -la app.py wsgi.py requirements-web.txt
ls -la templates/index.html
```

---

## When Ready to Deploy

Once you've tested locally and everything works:

1. ✅ Game creation works
2. ✅ Moves work
3. ✅ Hints work (5 limit)
4. ✅ Difficulty slider works
5. ✅ Time control works
6. ✅ Analysis works
7. ✅ No errors in console

**Then:** Follow `PYTHONANYWHERE_QUICK_SETUP.md` to deploy!

---

## Still Having Issues?

1. Check console (F12) for error messages
2. Check Flask terminal output (where you ran `python app.py`)
3. Verify all files are present
4. Try restarting Flask
5. Check requirements-web.txt has all dependencies

---

**Ready to test? Run: `python app.py` ♞**

Questions? Check the full guides:
- `README_WEB.md` - Full web version documentation
- `PYTHONANYWHERE_DEPLOYMENT.md` - Detailed deployment steps
