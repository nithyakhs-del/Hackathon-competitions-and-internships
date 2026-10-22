"""Collect opportunities -> docs/data/opportunities.json"""
import csv, datetime as dt, hashlib, json, pathlib
from collectors import codeforces

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs/data/opportunities.json"
COLLECTORS = {"codeforces": codeforces.fetch}  # add new sources here
KEEP_EXPIRED_DAYS = 30


def load_manual():
    p = ROOT / "data/manual.csv"
    rows = []
    if not p.exists():
        return rows
    with p.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = {k: (v or "").strip() for k, v in r.items() if k}
            if not r.get("name"):
                continue
            key = (r["name"] + r.get("deadline", "")).lower().encode()
            r["id"] = "m-" + hashlib.md5(key).hexdigest()[:10]
            r["source"] = "manual"
            r.setdefault("first_year_eligible", "Unclear")
            rows.append(r)
    return rows


def parse(s):
    try:
        return dt.datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def main():
    now = dt.datetime.now()
    prev = []
    if OUT.exists():
        prev = json.loads(OUT.read_text(encoding="utf-8")).get("items", [])
    items = load_manual()
    for name, fn in COLLECTORS.items():
        try:
            items += fn()
            print(f"[ok] {name}")
        except Exception as e:  # keep old data if a source fails
            print(f"[fail] {name}: {e}")
            items += [p for p in prev if p.get("source") == name]
    seen, final = set(), []
    for it in items:
        if it["id"] in seen:
            continue
        seen.add(it["id"])
        d = parse(it.get("deadline", ""))
        it["expired"] = bool(d and d < now)
        if d and (now - d).days > KEEP_EXPIRED_DAYS:
            continue
        it["last_verified"] = it.get("last_verified") or now.strftime("%Y-%m-%d")
        final.append(it)
    final.sort(key=lambda x: (x["expired"], x.get("deadline") or "9999"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"updated": now.strftime("%Y-%m-%d %H:%M"),
                               "items": final}, indent=1), encoding="utf-8")
    print(f"{len(final)} items written")


if __name__ == "__main__":
    main()
