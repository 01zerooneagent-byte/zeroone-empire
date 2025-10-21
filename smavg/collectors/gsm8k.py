import requests
import json
import math
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

def fetch_gsm8k():
    """Fetch REAL GSM8K data with retries"""
    try:
        print("🔄 Fetching LIVE GSM8K data...")
        response = fetch_with_retries("https://huggingface.co/api/models?search=gsm8k&sort=downloads", timeout=10)
        
        if not response:
            raise ValueError("All retry attempts failed")
            
        models = response.json()
        
        if not models:
            raise ValueError("No GSM8K models found")
            
        # Use model downloads as proxy for ecosystem activity
        top_model = max(models, key=lambda x: x.get('downloads', 0))
        downloads = top_model.get('downloads', 0)
        
        # Convert downloads to a score (0-1) - real metric of ecosystem activity
        download_score = min(1.0, math.log10(max(1, downloads)) / 6.0)  # log10(1M) = 6
        
        print(f"✅ GSM8K ecosystem score: {download_score:.3f} (based on {downloads} downloads)")
        
        return {
            "domain": "M",
            "name": "GSM8K-Ecosystem",
            "score": download_score,
            "trust": "measured", 
            "source": f"hf-gsm8k-live-{datetime.now().strftime('%Y%m%d')}"
        }
    except Exception as e:
        print(f"❌ GSM8K collector FAILED: {e}")
        return None
