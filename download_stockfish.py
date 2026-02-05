"""
Stockfish Download Script
Downloads and sets up Stockfish chess engine for Windows.
"""

import os
import sys
import urllib.request
import zipfile
import shutil

STOCKFISH_URL = "https://github.com/official-stockfish/Stockfish/releases/download/sf_17/stockfish-windows-x86-64-avx2.zip"
STOCKFISH_FALLBACK_URL = "https://github.com/official-stockfish/Stockfish/releases/download/sf_17/stockfish-windows-x86-64.zip"

def download_stockfish():
    """Download and extract Stockfish."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    stockfish_exe = os.path.join(script_dir, "stockfish.exe")
    
    if os.path.exists(stockfish_exe):
        print(f"Stockfish already exists at {stockfish_exe}")
        return stockfish_exe
    
    zip_path = os.path.join(script_dir, "stockfish.zip")
    extract_dir = os.path.join(script_dir, "stockfish_temp")
    
    print("Downloading Stockfish (this may take a moment)...")
    
    try:
        # Try AVX2 version first (faster on modern CPUs)
        urllib.request.urlretrieve(STOCKFISH_URL, zip_path)
    except Exception as e:
        print(f"AVX2 version failed: {e}")
        print("Trying fallback version...")
        try:
            urllib.request.urlretrieve(STOCKFISH_FALLBACK_URL, zip_path)
        except Exception as e2:
            print(f"Download failed: {e2}")
            print("\nPlease download Stockfish manually from:")
            print("https://stockfishchess.org/download/")
            print(f"\nPlace stockfish.exe in: {script_dir}")
            return None
    
    print("Extracting Stockfish...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find stockfish.exe in extracted files
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.lower() == "stockfish.exe" or file.lower().startswith("stockfish"):
                    if file.endswith(".exe"):
                        src = os.path.join(root, file)
                        shutil.copy2(src, stockfish_exe)
                        print(f"Stockfish installed to {stockfish_exe}")
                        break
        
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree(extract_dir, ignore_errors=True)
        
        if os.path.exists(stockfish_exe):
            return stockfish_exe
        else:
            print("Could not find stockfish.exe in downloaded archive")
            return None
            
    except Exception as e:
        print(f"Error extracting: {e}")
        return None


if __name__ == "__main__":
    result = download_stockfish()
    if result:
        print(f"\nSuccess! Stockfish is ready at: {result}")
        print("\nYou can now run: python chess_engine.py")
    else:
        print("\nFailed to download Stockfish automatically.")
        print("Please download from https://stockfishchess.org/download/")
