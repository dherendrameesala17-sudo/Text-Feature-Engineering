import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

reviews = []
print("Starting scraper...")

for page in range(1, 11):
    url = f"https://www.amazon.in/product-reviews/B0CHX3QBCH/ref=cm_cr_dp_d_show_all_btm?pageNumber={page}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        found = soup.select("[data-hook='review-body']")

        for tag in found:
            reviews.append({"review_text": tag.get_text(strip=True)})

        print(f"Page {page}: got {len(found)} reviews | Total so far: {len(reviews)}")
        time.sleep(random.uniform(2, 4))

    except Exception as e:
        print(f"Page {page} failed: {e}")

df = pd.DataFrame(reviews)

if len(df) >= 100:
    print(f"\nSuccess! Scraped {len(df)} reviews")
    df.to_csv("reviews.csv", index=False)
    print("Saved to reviews.csv")
else:
    print(f"\nOnly got {len(df)} reviews — Amazon blocked us.")
    print("Switching to backup dataset...")

    backup_url = "https://raw.githubusercontent.com/pycaret/pycaret/master/datasets/amazon.csv"
    df = pd.read_csv(backup_url)
    df = df.rename(columns={"reviewText": "review_text", "Positive": "label"})
    df = df[['review_text', 'label']].dropna().head(200)
    df.to_csv("reviews.csv", index=False)
    print(f"Backup dataset saved! {len(df)} reviews ready.")