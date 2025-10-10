#!/usr/bin/env python3
import os, json, datetime
def p(s): print(f"[AWA] {s}")
if __name__ == "__main__":
    p("Booting AGI Wealth Autopilot (mock mode)")
    report = {"ok": True, "when": datetime.datetime.utcnow().isoformat()+"Z", "mode": "mock"}
    os.makedirs("../reports", exist_ok=True)
    with open("../reports/boot_report.json", "w") as f:
        json.dump(report, f, indent=2)
    p("Report written to reports/boot_report.json")
