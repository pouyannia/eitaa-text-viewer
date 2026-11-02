
import requests
from bs4 import BeautifulSoup

CHANNEL = "farsna"
CHANNEL_URL = f"https://eitaa.com/s/{CHANNEL}"


def fetch_channel():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        CHANNEL_URL,
        headers=headers,
        timeout=30
    )

    print("HTTP Status:", response.status_code)
    print("Final URL:", response.url)
    print("Content-Type:", response.headers.get("Content-Type"))

    response.raise_for_status()

    return response.text


def main():

    # 1. دریافت HTML
    html = fetch_channel()

    print("\n========== HTML INFO ==========")
    print("HTML length:", len(html))

    # 2. تجزیه HTML
    soup = BeautifulSoup(html, "html.parser")

    print("\n========== PAGE TITLE ==========")

    if soup.title:
        print(soup.title.get_text(strip=True))
    else:
        print("No title")

    # 3. بررسی تگ‌های Script
    print("\n========== SCRIPT URLS ==========")

    for script in soup.select("script[src]"):
        print(script.get("src"))

    # 4. بررسی تعداد عناصر احتمالی پیام
    print("\n========== MESSAGE ELEMENTS ==========")

    selectors = [
        ".etme_widget_message",
        ".js-message_text",
        ".etme_widget_message_text",
        ".etme_widget_message_wrap",
        "[data-post]"
    ]

    for selector in selectors:
        print(
            selector,
            ":",
            len(soup.select(selector))
        )

    # 5. جستجوی کلمات مهم در HTML
    print("\n========== KEYWORDS ==========")

    keywords = [
        "message",
        "widget",
        "farsna",
        "399071",
        "before",
        "api",
        "ajax",
        "post"
    ]

    html_lower = html.lower()

    for word in keywords:
        print(
            word,
            ":",
            word in html_lower
        )

    # 6. نمایش 2000 کاراکتر ابتدایی
    print("\n========== HTML START ==========")
    print(html[:2000])

    # 7. نمایش 4000 کاراکتر انتهایی
    print("\n========== HTML END ==========")
    print(html[-4000:])


if __name__ == "__main__":
    main()
