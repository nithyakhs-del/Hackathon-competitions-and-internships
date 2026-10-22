"""Codeforces collector (official public API, no key needed)."""
import datetime as dt
import requests

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
URL = "https://codeforces.com/api/contest.list"


def fetch():
    r = requests.get(URL, timeout=30, headers={"User-Agent": "opportunities-hub/1.0"})
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "OK":
        raise RuntimeError("Codeforces API error")
    out = []
    for c in data["result"]:
        if c.get("phase") != "BEFORE":  # upcoming only
            continue
        start = dt.datetime.fromtimestamp(c["startTimeSeconds"], IST)
        out.append({
            "id": f"cf-{c['id']}",
            "name": c["name"],
            "category": "Competition",
            "organizer": "Codeforces",
            "domain": "Competitive Programming",
            "first_year_eligible": "Yes",  # open to all registered users
            "mode": "Online",
            "location": "Online",
            "deadline": start.strftime("%Y-%m-%dT%H:%M"),
            "start_date": start.strftime("%Y-%m-%dT%H:%M"),
            "reward": "Rating / rank",
            "cost": "Free",
            "link": f"https://codeforces.com/contests/{c['id']}",
            "verification": "Verified (official API)",
            "source": "codeforces",
        })
    return out
