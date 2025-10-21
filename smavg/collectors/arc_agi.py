import requests
import json
import time
from datetime import datetime

def fetch_with_retries(url, headers=None, timeout=15, max_retries=3):
    """Helper function with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"   ⚠️ Attempt {attempt + 1} failed, retrying in 5s...")
            time.sleep(5)
    return None

def fetch_arc_agi():
    """Fetch REAL ARC-AGI leaderboard data with retries"""
    try:
        print("🔄 Fetching LIVE ARC-AGI data...")
        response = fetch_with_retries("https://leaderboard.arcprize.org/api/leaderboard", timeout=15)
        
        if not response:
            raise ValueError("All retry attempts failed")
            
        data = response.json()
        
        if not data.get("entries"):
            raise ValueError("No entries in ARC-AGI leaderboard")
            
        top_score = max(entry["score"] for entry in data["entries"]) / 100.0
        print(f"✅ ARC-AGI live score: {top_score}")
        
        return {
            "domain": "R", 
            "name": "ARC-AGI", 
            "score": top_score, 
            "trust": "measured", 
            "source": f"arc-prize-live-{datetime.now().strftime('%Y%m%d')}"
        }
    except Exception as e:
        print(f"❌ ARC-AGI collector FAILED: {e}")
        return None
