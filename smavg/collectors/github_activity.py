import requests
import json
import os
import time
from datetime import datetime

def fetch_with_retries(url, headers=None, timeout=15, max_retries=3):
    """Helper function with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 403:
                print(f"   ⚠️ GitHub API rate limit hit on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    raise Exception("GitHub API rate limit exceeded")
                time.sleep(10)  # Longer delay for rate limits
                continue
            response.raise_for_status()
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"   ⚠️ Attempt {attempt + 1} failed, retrying in 5s...")
            time.sleep(5)
    return None

def fetch_github_activity():
    """Fetch REAL GitHub activity for AGI repos with token support"""
    try:
        print("🔄 Fetching LIVE GitHub activity...")
        
        # Track major AGI repo activity
        repos = [
            "enricoros/big-AGI",
            "Josh-XT/AGiXT", 
            "TransformerOptimus/SuperAGI",
            "fchollet/ARC-AGI"
        ]
        
        # GitHub API headers with token support
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Smavg-AGI-Tracker"
        }
        if os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
            print("   🔑 Using GITHUB_TOKEN for authenticated API calls")
        
        total_stars = 0
        successful_repos = 0
        
        for repo in repos:
            try:
                response = fetch_with_retries(f"https://api.github.com/repos/{repo}", headers=headers, timeout=10)
                
                if response:
                    data = response.json()
                    stars = data.get('stargazers_count', 0)
                    total_stars += stars
                    successful_repos += 1
                    print(f"   📊 {repo}: {stars} stars")
                else:
                    print(f"   ❌ {repo}: Failed to fetch")
            except Exception as e:
                print(f"   ❌ {repo}: {e}")
                continue
                
        if successful_repos == 0:
            raise ValueError("No GitHub repos accessible - check GITHUB_TOKEN or rate limits")
            
        # Normalize: 0-100K stars = 0.0-1.0 score
        star_score = min(1.0, total_stars / 100000.0)
        
        print(f"✅ GitHub ecosystem score: {star_score:.3f} ({total_stars} total stars from {successful_repos} repos)")
        
        return {
            "domain": "WM",  # Working Memory - proxy for code/development activity
            "name": "GitHub-AGI-Activity",
            "score": star_score,
            "trust": "measured",
            "source": f"github-live-{datetime.now().strftime('%Y%m%d')}"
        }
    except Exception as e:
        print(f"❌ GitHub activity collector FAILED: {e}")
        if "rate limit" in str(e).lower():
            print("   💡 Tip: Set GITHUB_TOKEN environment variable to increase rate limits")
        return None
