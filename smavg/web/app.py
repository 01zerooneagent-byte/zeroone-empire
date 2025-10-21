from flask import Flask, Response
from renderer import render_text
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def root():
    page = render_text()
    headers = {"Content-Type": "text/plain; charset=utf-8", "Refresh": "30"}
    return Response(page, headers=headers)

@app.route("/health")
def health():
    return "Smavg 🐲 LIVE is running!"

@app.route("/raw")
def raw():
    import json
    try:
        with open("data/metrics.json","r",encoding="utf-8") as f:
            return Response(f.read(), headers={"Content-Type":"application/json"})
    except FileNotFoundError:
        return "No live metrics data available", 404

@app.route("/update-now")
def update_now():
    """Trigger a real-time update"""
    try:
        result = subprocess.run([
            os.path.join(os.path.dirname(__file__), '..', '.venv', 'bin', 'python'),
            os.path.join(os.path.dirname(__file__), '..', 'scripts', 'update.py')
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..'))
        
        return f"✅ Live update triggered!\\n{result.stdout}\\n{result.stderr}"
    except Exception as e:
        return f"❌ Update failed: {e}"

if __name__ == "__main__":
    print("🚀 Starting Smavg 🐲 AGI Bar — 100% LIVE MODE")
    print("📊 Dashboard: http://localhost:8080")
    print("🔄 Live update: http://localhost:8080/update-now")
    print("📈 Raw data: http://localhost:8080/raw")
    print("🔴 ALL DATA IS REAL-TIME - NO STATIC FALLBACKS")
    print("⏹️  Press Ctrl+C to stop")
    app.run(host="0.0.0.0", port=8080, debug=False)
