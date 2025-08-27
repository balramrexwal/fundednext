import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import SSLError

urls = [
    # Add your list of FundedNext URLs here
    "https://help.fundednext.com/en/collections/13565526-general-faq",
    "https://help.fundednext.com/en/collections/13567126-eligibility-verification",
    # ...
]

keywords = ["coupon", "promo", "discount", "%off", "% off", "code", "voucher", "offer"]

def search_hidden_codes(urls):
    for url in urls:
        try:
            r = requests.get(url, timeout=10)  # SSL verify is enabled by default
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")

            visible_text = soup.get_text(" ", strip=True).lower()
            comments = " ".join([c for c in soup.find_all(string=lambda t: isinstance(t, Comment))]).lower()
            meta_tags = " ".join([m.get("content", "") for m in soup.find_all("meta") if m.get("content")]).lower()
            scripts = " ".join([s.get_text() for s in soup.find_all("script")]).lower()

            combined = visible_text + " " + comments + " " + meta_tags + " " + scripts

            matches = [word for word in keywords if word in combined]
            if matches:
                print(f"🔎 Potential promo mention in: {url}")
                print(f"   ➝ Found keywords: {set(matches)}")
                print("--------------------------------------------------")
        except SSLError as ssl_err:
            print(f"⚠️ SSL verification error fetching {url}: {ssl_err}")
        except requests.RequestException as e:
            print(f"⚠️ Error fetching {url}: {e}")

if __name__ == "__main__":
    search_hidden_codes(urls)
