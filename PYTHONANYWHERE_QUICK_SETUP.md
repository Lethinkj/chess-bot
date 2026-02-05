# Chess Arena - PythonAnywhere Deployment (5-Minute Setup)

## You have a free PythonAnywhere account! Here's how to deploy:

### Step 1: Log in to PythonAnywhere
Go to: https://www.pythonanywhere.com and log in with your account

---

### Step 2: Upload Your Files

**Option A: Git Clone (Fastest)**
1. Click **"Consoles"** at top
2. Open **"Bash"** console
3. Run these commands:
   ```bash
   cd
   git clone https://github.com/YOUR-USERNAME/chess-arena.git
   cd chess-arena
   ```

**Option B: Manual Upload**
1. Go to **"Files"** tab
2. Create folder: `chess-arena`
3. Upload these files:
   - `app.py`
   - `wsgi.py`
   - `requirements-web.txt`
   - `templates/index.html`

---

### Step 3: Install Dependencies

1. Click **"Consoles"** → **"Bash"**
2. Run:
   ```bash
   cd chess-arena
   mkvirtualenv --python=/usr/bin/python3.10 chess
   pip install flask python-chess stockfish
   ```
   
   (Wait for it to finish - takes ~1 minute)

---

### Step 4: Create Web App

1. Click the **"Web"** tab (top right)
2. Click **"Add a new web app"**
3. Choose **"Flask"** framework
4. Select **"Python 3.10"**
5. Choose file path: paste this:
   ```
   /home/YOUR-USERNAME/chess-arena/app.py
   ```
   Replace `YOUR-USERNAME` with your PythonAnywhere username!

6. Click **Next**

---

### Step 5: Configure WSGI File

1. PythonAnywhere will open your WSGI file
2. **Delete everything** in the file
3. Paste this:
   ```python
   import sys
   path = '/home/YOUR-USERNAME/chess-arena'
   if path not in sys.path:
       sys.path.insert(0, path)
   from app import app as application
   ```
   Replace `YOUR-USERNAME`!

4. Click **Save**

---

### Step 6: Set Virtual Environment

1. Go to **"Web"** tab
2. Scroll down to **"Virtualenv"**
3. Click the red error text
4. Type: `/home/YOUR-USERNAME/.virtualenvs/chess`
5. Press **Enter**

---

### Step 7: Reload & Done!

1. Click the big **green "Reload"** button (top of Web tab)
2. Wait 20 seconds...
3. Open your app at: **`https://YOUR-USERNAME.pythonanywhere.com`**

---

## 🎉 You're Done!

Your Chess Arena is now live online!

### What You Can Do:
- ♞ Play chess vs AI
- 🎯 Choose difficulty (0-20)
- ⏱️ Set time limits (1-10 minutes)
- 💡 Get 5 hints per game
- 📊 Analyze positions

---

## Troubleshooting

### "404 Not Found"
- Wait 2 minutes and refresh
- Check green button is showing (not red)

### "ImportError: No module named flask"
- Go to Web tab
- Check virtualenv path is: `/home/YOUR-USERNAME/.virtualenvs/chess`
- Click green Reload button

### Stockfish errors
- Stockfish may be slow on free tier - this is normal
- Game still works, just slower analysis

### Need help?
See detailed guide: **`PYTHONANYWHERE_DEPLOYMENT.md`**

---

## Important: Replace YOUR-USERNAME!

Everywhere it says `YOUR-USERNAME`, use your actual PythonAnywhere username!

For example: If your username is `john123`, then:
- Path becomes: `/home/john123/chess-arena`
- URL becomes: `https://john123.pythonanywhere.com`

---

## Your App URL Format
```
https://[YOUR-USERNAME].pythonanywhere.com
```

Example: `https://myuser.pythonanywhere.com`

---

## File Checklist

These files should be in `/chess-arena`:
- ✅ app.py
- ✅ wsgi.py  
- ✅ requirements-web.txt
- ✅ templates/index.html

---

**Chess Arena is now LIVE! Share your link with friends! ♞**
