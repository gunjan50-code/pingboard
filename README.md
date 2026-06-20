# ⬡ Pingboard - Web page Monitor 
A lightweight service monitoring tool built to track uptime and response times across a large portfolio of web pages — originally developed during part-time work at [The Scaling Point] managing 180+ location pages and 6 service lines for company.

---

## The Problem

Managing a site with 180+ location pages across 6 service categories means hundreds of individual URLs that can silently go down. Checking them manually was time-consuming and unreliable. InfraWatch automates this entirely.

---

## What It Does

- Pings a configurable list of URLs every 60 seconds
- Logs response time, HTTP status code, and up/down status to a local SQLite database
- Displays a live dashboard showing current status of all monitored services
- Calculates uptime % per service based on historical checks
- Generates and downloads a full HTML report with one click
- "Run Checks Now" button for on-demand monitoring

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, Vanilla JS |
| Monitoring | Python `requests` + threading |

---

## Project Structure

```
pingboard/
├── app.py              # Flask app + monitoring logic
├── config.json         # List of URLs to monitor
├── monitor.db          # SQLite database (auto-created)
├── requirements.txt
├── templates/
│   ├── dashboard.html  # Live status dashboard
│   └── report.html     # Downloadable report template
└── static/
    └── css/
        └── style.css
```

---

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/gunjan50-code/pingboard.git
cd pingboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your URLs to config.json
# 4. Run the app
python app.py

# 5. Open in browser
# http://localhost:5000
```

---

## Configuring URLs

Edit `config.json` to add any URLs you want to monitor:

```json
{
  "targets": [
    { "name": "Homepage", "url": "https://yoursite.com" },
    { "name": "Service Page", "url": "https://yoursite.com/services/example.html" }
  ]
}
```

---

## Dashboard Preview

- **Green badge** = Service UP, response time shown in ms
- **Red badge** = Service DOWN, no response received
- **Uptime bar** = % of successful checks out of total checks run
- **Download Report** = Exports a clean HTML report with full status summary

---

## Why I Built This

At The Scaling Point, we manage Buildaway's web presence — 6 service categories across ~180 London/Kent/Essex locations, plus a blog. That's hundreds of individual URLs. When any page goes down (broken HTML, server error, DNS issue), it hurts SEO and user experience. 

InfraWatch was built so I could stop checking pages manually and get a clear picture of site health at a glance.

---

## Author

**Gunjan Gupta** — AI & Data Science Student, D.Y. Patil College of Engineering, Pune   
[LinkedIn](https://linkedin.com) | [GitHub](https://github.com/gunjan50-code)
