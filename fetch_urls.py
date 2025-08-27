import requests
from bs4 import BeautifulSoup, Comment
from requests.exceptions import SSLError, HTTPError

urls = [
    # Add your list of FundedNext URLs here
    "https://help.fundednext.com/en/collections/13565526-general-faq",
    "https://help.fundednext.com/en/collections/13567126-eligibility-verification",
    "https://help.fundednext.com/en/collections/13567149-withdrawal-procedure",
    "https://help.fundednext.com/en/collections/13567602-about-fundednext-stellar-instant-model",
    "https://help.fundednext.com/en/articles/11641077-what-is-stellar-instant",
    "https://help.fundednext.com/en/articles/11641098-how-does-stellar-instant-differ-from-challenge-based-models",
    "https://help.fundednext.com/en/articles/11641117-what-are-the-available-account-sizes-for-the-stellar-instant-model",
    "https://help.fundednext.com/en/articles/11641140-which-trading-platforms-are-you-offering-for-stellar-instant",
    "https://help.fundednext.com/en/articles/11641161-how-much-does-each-stellar-instant-account-cost",
    "https://help.fundednext.com/en/articles/11641381-what-will-be-my-performance-reward-from-the-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641163-what-are-the-daily-loss-limit-and-the-maximum-loss-limit-for-the-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641219-are-there-any-minimum-trading-days",
    "https://help.fundednext.com/en/articles/11641226-can-i-reset-my-stellar-instant-account",
    "https://help.fundednext.com/en/articles/11641232-are-there-restrictions-for-overnight-or-weekend-trading-in-stellar-instant",
    "https://help.fundednext.com/en/articles/11641300-what-are-the-commission-fees-for-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641328-are-there-any-consistency-rules-for-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641338-can-i-use-ea-in-stellar-instant",
    "https://help.fundednext.com/en/articles/11641369-what-is-the-leverage-provided-in-the-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641400-what-is-the-maximum-allocation-for-the-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641410-is-news-trading-allowed-in-the-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641507-is-there-any-passing-reward-for-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641516-is-there-a-scale-up-plan-for-stellar-instant-accounts",
    "https://help.fundednext.com/en/articles/11641571-what-does-10x-scale-up-mean",
    "https://help.fundednext.com/en/articles/11641614-what-rules-do-i-need-to-follow-in-the-stellar-instant-account",
    "https://help.fundednext.com/en/articles/11672342-is-copy-trading-allowed-in-stellar-instant",
    "https://help.fundednext.com/en/articles/11641674-is-kyc-required",
    "https://help.fundednext.com/en/articles/11641680-is-there-an-agreement-in-stellar-instant-account",
    "https://help.fundednext.com/en/articles/11641693-what-is-the-eligibility-criteria-for-my-performance-reward",
    "https://help.fundednext.com/en/articles/11641804-how-can-i-withdraw-my-performance-reward",
    "https://help.fundednext.com/en/articles/11821889-what-crypto-wallet-address-should-i-send-during-withdrawal-of-performance-rewards",
    "https://help.fundednext.com/en/articles/11641898-why-choose-fundednext-stellar-instant",
    "https://help.fundednext.com/en/articles/11642166-when-is-the-best-time-to-reach-out-to-fundednext-stellar-instant-support"
]

keywords = ["coupon", "promo", "discount", "%off", "% off", "code", "voucher", "offer"]

# Common headers to mimic a real browser
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/116.0.0.0 Safari/537.36"),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://google.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    # If possible add a cookie header with session cookies obtained manually.
}

def search_hidden_codes(urls):
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)  # SSL verify enabled by default
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
        except HTTPError as http_err:
            print(f"❌ HTTP error fetching {url}: {http_err}")
        except SSLError as ssl_err:
            print(f"⚠️ SSL verification error fetching {url}: {ssl_err}")
        except Exception as e:
            print(f"⚠️ Other error fetching {url}: {e}")

if __name__ == "__main__":
    search_hidden_codes(urls) 