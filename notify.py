"""Email a digest of deadlines within 3 days (needs SMTP secrets; skips if unset)."""
import datetime as dt, json, os, pathlib, smtplib
from email.message import EmailMessage

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "docs/data/opportunities.json"
SEEN = ROOT / "data/notified.json"


def main():
    user, pw, to = (os.environ.get(k) for k in ("SMTP_USER", "SMTP_PASS", "ALERT_TO"))
    if not (user and pw and to):
        print("Email secrets not set; skipping alerts.")
        return
    now = dt.datetime.now()
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    due = []
    for it in json.loads(DATA.read_text(encoding="utf-8"))["items"]:
        try:
            d = dt.datetime.fromisoformat(it["deadline"])
        except (KeyError, ValueError):
            continue
        if now <= d <= now + dt.timedelta(days=3) and it["id"] not in seen \
                and it.get("first_year_eligible") != "No":
            due.append(it)
    if not due:
        print("Nothing new to alert.")
        return
    body = "\n\n".join(f"{i['name']} ({i['category']})\nDeadline: {i['deadline']}\n{i['link']}"
                       for i in due)
    msg = EmailMessage()
    msg["Subject"] = f"{len(due)} opportunity deadline(s) in the next 3 days"
    msg["From"], msg["To"] = user, to
    msg.set_content(body)
    with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST", "smtp.gmail.com"), 465) as s:
        s.login(user, pw)
        s.send_message(msg)
    SEEN.write_text(json.dumps(sorted(seen | {i["id"] for i in due})))
    print(f"Alert sent for {len(due)} items")


if __name__ == "__main__":
    main()
