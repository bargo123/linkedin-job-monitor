import os
import json
import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=%22flutter%20developer%22%20OR%20%22flutter%20engineer%22%20OR%20%22mobile%20developer%22%20NOT%20%22react%20native%22%20NOT%20%22software%20engineer%22%20NOT%20%22mobile%20engineer%22%20NOT%20%22android%22%20NOT%20%22ios%22&f_WT=2&location=Worldwide&f_TPR=r86400&sortBy=DD"

SEEN_FILE = "seen_jobs.json"


def send_telegram(text):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=10,
    )


def load_seen():
    if os.path.exists(SEEN_FILE):
        return set(json.load(open(SEEN_FILE)))
    return set()


def save_seen(seen):
    json.dump(list(seen), open(SEEN_FILE, "w"))


def fetch_jobs():
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(SEARCH_URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    for a in soup.select("a.base-card__full-link"):
        title = a.text.strip()
        link = a["href"]
        job_id = link.split("/")[-1].split("?")[0]
        jobs.append((job_id, title, link))

    return jobs


def main():
    seen = load_seen()
    new_seen = set(seen)
    send_telegram("Loading...")
    jobs = fetch_jobs()
     
    for job_id, title, link in jobs:
        if job_id not in seen:
            send_telegram(f"🚀 New Flutter Job\n\n{title}\n{link}")
            new_seen.add(job_id)

    save_seen(new_seen)


if __name__ == "__main__":
    main()
