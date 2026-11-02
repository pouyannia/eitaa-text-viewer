
import requests
import json
import re

from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pathlib import Path


CHANNEL = "farsna"
CHANNEL_URL = f"https://eitaa.com/s/{CHANNEL}"

OUTPUT_FILE = Path("messages.json")


def fetch_channel():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        CHANNEL_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def extract_messages(html):

    soup = BeautifulSoup(html, "html.parser")

    messages = []

    elements = soup.select(
        ".etme_widget_message"
    )

    for element in elements:

        message_id = element.get("data-post")

        content = element.select_one(
            ".js-message_text"
        )

        date_element = element.select_one(
            ".etme_widget_message_date time"
        )

        if not message_id or not content:
            continue

        # Remove links and their visible labels
        for link in content.select("a"):
            link.decompose()

        # Extract plain text
        raw_text = content.get_text(
            separator="\n"
        )

        lines = []

        for line in raw_text.splitlines():

            line = re.sub(r"\s+", " ", line).strip()

            if line:
                lines.append(line)

        text = "\n".join(lines)

        if not text:
            continue

        published_at = None

        if date_element:
            published_at = date_element.get("datetime")

        messages.append({
            "id": message_id,
            "text": text,
            "published_at": published_at,
            "channel": CHANNEL
        })

    return messages


def save_messages(messages):

    if not messages:
        raise ValueError(
            "No messages found. Check the source HTML."
        )

    data = {
        "channel": CHANNEL,
        "fetched_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "count": len(messages),
        "messages": messages
    }

    OUTPUT_FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print(f"{len(messages)} messages saved.")


def main():
    html = fetch_channel()

    print("HTML length:", len(html))
    print("HTML preview:")
    print(html[:2000])

    soup = BeautifulSoup(html, "html.parser")

    print("\nPage title:", soup.title.get_text(strip=True) if soup.title else "No title")

    print(
        "Message elements:",
        len(soup.select(".etme_widget_message"))
    )

    print(
        "Message text elements:",
        len(soup.select(".js-message_text"))
    )

    messages = extract_messages(html)

    print("Extracted messages:", len(messages))

    save_messages(messages)


if __name__ == "__main__":
    main()
