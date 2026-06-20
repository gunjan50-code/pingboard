from flask import Flask, render_template, jsonify, send_file
import sqlite3
import requests
import time
import threading
import json
from datetime import datetime
import os

app = Flask(__name__)
DB = "monitor.db"

# --- Load targets from config ---
def load_targets():
    with open("config.json") as f:
        return json.load(f)["targets"]

# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            status TEXT,
            response_time REAL,
            status_code INTEGER,
            checked_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Ping a single URL ---
def check_url(target):
    name = target["name"]
    url = target["url"]
    try:
        start = time.time()
        r = requests.get(url, timeout=5)
        elapsed = round((time.time() - start) * 1000, 2)  # ms
        status = "UP" if r.status_code < 400 else "DOWN"
        code = r.status_code
    except Exception:
        elapsed = None
        status = "DOWN"
        code = None

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO checks (name, url, status, response_time, status_code, checked_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, url, status, elapsed, code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# --- Run checks for all targets ---
def run_all_checks():
    targets = load_targets()
    for t in targets:
        check_url(t)

# --- Background monitor thread ---
def monitor_loop():
    while True:
        run_all_checks()
        time.sleep(60)  # check every 60 seconds

# --- Get latest status per target ---
def get_latest_statuses():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    targets = load_targets()
    results = []
    for t in targets:
        c.execute('''
            SELECT status, response_time, status_code, checked_at
            FROM checks WHERE url = ?
            ORDER BY id DESC LIMIT 1
        ''', (t["url"],))
        row = c.fetchone()
        if row:
            results.append({
                "name": t["name"],
                "url": t["url"],
                "status": row[0],
                "response_time": row[1],
                "status_code": row[2],
                "checked_at": row[3]
            })
        else:
            results.append({
                "name": t["name"],
                "url": t["url"],
                "status": "PENDING",
                "response_time": None,
                "status_code": None,
                "checked_at": "Not checked yet"
            })
    conn.close()
    return results

# --- Uptime % per target ---
def get_uptime_stats():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    targets = load_targets()
    stats = []
    for t in targets:
        c.execute("SELECT COUNT(*) FROM checks WHERE url=?", (t["url"],))
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM checks WHERE url=? AND status='UP'", (t["url"],))
        up = c.fetchone()[0]
        uptime = round((up / total) * 100, 1) if total > 0 else 0
        stats.append({"name": t["name"], "uptime": uptime, "total_checks": total})
    conn.close()
    return stats

# --- Routes ---
@app.route("/")
def dashboard():
    statuses = get_latest_statuses()
    stats = get_uptime_stats()
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("dashboard.html", statuses=statuses, stats=stats, last_updated=last_updated)

@app.route("/api/status")
def api_status():
    return jsonify(get_latest_statuses())

@app.route("/check-now")
def check_now():
    run_all_checks()
    return jsonify({"message": "Checks complete", "time": datetime.now().strftime("%H:%M:%S")})

@app.route("/report")
def generate_report():
    statuses = get_latest_statuses()
    stats = get_uptime_stats()
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = render_template("report.html", statuses=statuses, stats=stats, generated_at=generated_at)
    report_path = "report_output.html"
    with open(report_path, "w") as f:
        f.write(html)
    return send_file(report_path, as_attachment=True, download_name=f"infra_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html")

@app.route("/history/<path:url>")
def history(url):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        SELECT status, response_time, status_code, checked_at
        FROM checks WHERE url=?
        ORDER BY id DESC LIMIT 20
    ''', (url,))
    rows = c.fetchall()
    conn.close()
    data = [{"status": r[0], "response_time": r[1], "status_code": r[2], "checked_at": r[3]} for r in rows]
    return jsonify(data)

if __name__ == "__main__":
    init_db()
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()
    app.run(debug=True)
