# Engineering Opportunities Hub

Auto-updating tracker of hackathons, competitions and internships for first-year CSE (AI/ML) students in India.

- `collectors/` – one file per automated source (Codeforces included).
- `data/manual.csv` – add Unstop / Devfolio / Internshala / AICTE etc. listings by hand (these sites restrict scraping). Dates: `YYYY-MM-DD`.
- `collect.py` – merges sources, dedupes, flags expired -> `docs/data/opportunities.json`.
- `notify.py` – emails deadlines within 3 days.
- `docs/index.html` – the dashboard (GitHub Pages).
- `.github/workflows/collect.yml` – runs every 6 hours, free.

## Setup (10 minutes)
1. Create a GitHub repo and upload all these files (keep folder structure).
2. Settings -> Pages -> Source: *Deploy from a branch*, branch `main`, folder `/docs`.
3. Actions tab -> "Collect opportunities" -> Run workflow. Your site: `https://<username>.github.io/<repo>/`.
4. Optional alerts: Settings -> Secrets -> Actions, add `SMTP_USER` (Gmail), `SMTP_PASS` (Gmail *App Password*), `ALERT_TO`.

## Add a new automated source
Write `collectors/yoursource.py` with `fetch()` returning dicts like those in `codeforces.py`, then register it in `COLLECTORS` in `collect.py`. Check each site's terms/API first. Kaggle has an official API.

## Rules
Mark `first_year_eligible` as Yes only if the official page says so. Keep `verification` honest, and check the link before applying.
