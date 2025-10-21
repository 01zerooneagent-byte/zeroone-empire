import sys, os, json, importlib.util
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scoring.model import run_score

def run_collectors():
    """Run ALL collectors and only use successful ones"""
    metrics = []
    cdir = os.path.join(os.path.dirname(__file__), '..', 'collectors')
    
    print("🐲 Smavg AGI Bar — LIVE DATA COLLECTION")
    print("=" * 50)
    
    successful = 0
    failed = 0
    
    for fname in os.listdir(cdir):
        if not fname.endswith(".py") or fname.startswith("__"):
            continue
        mod_name = fname[:-3]
        try:
            spec = importlib.util.spec_from_file_location(mod_name, os.path.join(cdir, fname))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            fn_name = f"fetch_{mod_name}"
            if hasattr(mod, fn_name):
                result = getattr(mod, fn_name)()
                if result:  # Only add successful collections
                    metrics.append(result)
                    successful += 1
                    print(f"✅ {mod_name}: {result['score']:.3f}")
                else:
                    failed += 1
                    print(f"❌ {mod_name}: No data collected")
        except Exception as e:
            failed += 1
            print(f"💥 {mod_name}: {e}")
    
    print(f"📊 Results: {successful} successful, {failed} failed")
    return metrics

if __name__ == "__main__":
    collected = run_collectors()
    
    if not collected:
        print("🚨 CRITICAL: No data collected from any source!")
        print("💡 Check your internet connection and try again")
        sys.exit(1)
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    metrics_json = {
        "as_of": datetime.utcnow().isoformat() + "Z",
        "track": "pure_model",
        "metrics": collected
    }
    
    with open(os.path.join(data_dir, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics_json, f, indent=2)

    state = run_score(
        metrics_path=os.path.join(data_dir,"metrics.json"),
        sources_path=os.path.join(data_dir,"sources.json")
    )
    
    print("\\n🎯 FINAL LIVE SCORES:")
    print(f"   AGI Progress: {state['agi_percent']}%")
    print(f"   Time Bar: {state['time_percent']}%")
    print(f"   Metrics Used: {state['counts']['metrics_counted']}/{state['counts']['metrics_total']}")
    print("✅ Live update complete - ALL DATA IS REAL-TIME!")
