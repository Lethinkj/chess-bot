# Deploy Chess Arena to PythonAnywhere

Follow these steps to host Chess Arena on PythonAnywhere for free.

## Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Sign up for a **free account** (Beginner plan)
3. Log in to your account

## Step 2: Upload Your Code

### Option A: Using Git (Recommended)

1. In PythonAnywhere, open **Bash console**
2. Clone your repository:
   ```bash
   cd
   git clone https://github.com/YOUR-USERNAME/chess-arena.git
   cd chess-arena
   ```

### Option B: Upload Files Manually

1. Go to **Files** → upload the following:
   - `app.py`
   - `templates/index.html`
   - `requirements-web.txt`
   - `stockfish.exe` (if available - optional)

Or drag and drop into the file manager.

## Step 3: Create Virtual Environment

1. Open **Bash console** in PythonAnywhere
2. Run:
   ```bash
   cd chess-arena
   mkvirtualenv --python=/usr/bin/python3.10 chess-env
   pip install -r requirements-web.txt
   ```

## Step 4: Configure Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **Flask** as framework
4. Select **Python 3.10**
5. When asked for code location, use:
   ```
   /home/your-username/chess-arena
   ```
6. When asked for WSGI file location, create it as:
   ```
   /home/your-username/chess-arena/wsgi.py
   ```

## Step 5: Create WSGI File

1. Open **Files** → create new file `/chess-arena/wsgi.py`
2. Add this code:
   ```python
   import sys
   path = '/home/YOUR-USERNAME/chess-arena'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app as application
   ```
   (Replace `YOUR-USERNAME` with your PythonAnywhere username)

3. Save the file

## Step 6: Configure Virtual Environment

1. Go to **Web** app configuration
2. Under **Virtualenv**, set:
   ```
   /home/your-username/.virtualenvs/chess-env
   ```
3. Save

## Step 7: Reload Your Web App

1. Click the **green "Reload" button** at the top of the **Web** tab
2. Wait 30 seconds for the app to load

## Step 8: Access Your Chess Arena

Your app will be at:
```
https://your-username.pythonanywhere.com
```

Replace `your-username` with your PythonAnywhere username.

## Troubleshooting

### "ModuleNotFoundError" error

**Solution**: In Web tab, check:
- Virtual environment path is correct
- Source code path is correct
- Run: `pip install -r requirements-web.txt` in Bash console

### Stockfish Not Found

**Solution**:
- Upload `stockfish.exe` to the chess-arena folder
- Or install system Stockfish:
  ```bash
  apt-get install stockfish
  ```
  (Note: Not available on free tier)

### Port or Binding Error

**Solution**:
- Reload the web app again
- Check that no other process is using the port

### Static Files Not Loading

**Solution**:
- Create `/static` folder in chess-arena
- In Web tab, add static files mapping:
  - URL: `/static/`
  - Directory: `/home/your-username/chess-arena/static`

## Performance Notes

Free PythonAnywhere accounts have:
- 100MB storage
- CPU throttling (slower Stockfish analysis)
- Some restrictions on background tasks

For better performance, upgrade to a paid plan.

## What Works on Free Tier

✅ Play chess games
✅ Get hints (5 per game)
✅ Adjust difficulty
✅ View move history
✅ Basic analysis

⚠️ Slower Stockfish analysis (CPU limited)
⚠️ Game speeds limited by server performance

## File Structure

Your `/chess-arena` folder should have:
```
chess-arena/
├── app.py                 # Main Flask app
├── wsgi.py               # Web gateway interface
├── requirements-web.txt  # Dependencies
├── templates/
│   └── index.html        # Web interface
├── static/               # CSS/JS (if needed)
└── stockfish.exe         # (optional) Chess engine
```

## Environment Variables

You can set environment variables in `Web` tab:

```python
import os
DIFFICULTY = os.getenv('DIFFICULTY', '20')
```

## Logs

To view error logs:
1. Go to **Web** tab
2. Click **Error log** link
3. Check for any issues

## Next Steps

1. **Share your link**: Your chess app is now live!
2. **Customize**: Modify `index.html` for your own branding
3. **Upgrade**: For better performance, consider a paid plan
4. **Add features**: Expand with user accounts, leaderboards, etc.

---

**Your Chess Arena is now online! 🎉**

Play at: `https://your-username.pythonanywhere.com`
