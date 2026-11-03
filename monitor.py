import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode


owner = "openvinotoolkit"
repository = "openvino"

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

history_file = "issues_seen.json"


def get_github_issues():
    """Fetch open issues from the GitHub repository."""

    api_url = (
        f"https://api.github.com/repos/{owner}/{repository}/issues"
        "?state=open&sort=created&direction=desc&per_page=100"
    )

    request = Request(
        api_url,
        headers={
            "User-Agent": "github-issue-radar"
        }
    )

    with urlopen(request, timeout=15) as response:
        issues = json.loads(response.read().decode("utf-8"))

    actual_issues = [
        issue for issue in issues
        if "pull_request" not in issue
    ]

    return actual_issues


def send_telegram_message(message):
    """Send a message to Telegram."""

    if not telegram_bot_token or not telegram_chat_id:
        raise ValueError(
            "Telegram credentials are missing. "
            "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID."
        )

    telegram_url = (
        f"https://api.telegram.org/bot"
        f"{telegram_bot_token}/sendMessage"
    )

    message_data = urlencode({
        "chat_id": telegram_chat_id,
        "text": message
    }).encode("utf-8")

    request = Request(
        telegram_url,
        data=message_data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    with urlopen(request, timeout=15) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("ok"):
        raise RuntimeError("Telegram could not send the message.")


def load_seen_issues():
    """Load issue IDs that were already processed."""

    if not os.path.exists(history_file):
        return None

    with open(history_file, "r") as file:
        return set(json.load(file))


def save_seen_issues(seen_issues):
    """Save processed issue IDs to the history file."""

    with open(history_file, "w") as file:
        json.dump(sorted(seen_issues), file, indent=4)


def main():
    try:
        print("Checking GitHub for issues...")

        issues = get_github_issues()

        print(f"Repository: {owner}/{repository}")
        print(f"Open issues found: {len(issues)}")

        seen_issues = load_seen_issues()

        if seen_issues is None:
            seen_issues = {
                f"{owner}/{repository}#{issue['number']}"
                for issue in issues
            }

            save_seen_issues(seen_issues)

            print("Initial issue history saved.")
            print("New issues will be reported on future runs.")
            return

        new_issues = []

        for issue in issues:
            issue_id = f"{owner}/{repository}#{issue['number']}"

            if issue_id not in seen_issues:
                new_issues.append(issue)

        if not new_issues:
            print("No new issues found.")
            return

        print(f"New issues found: {len(new_issues)}")

        for issue in new_issues:
            issue_number = issue["number"]
            issue_title = issue["title"]
            issue_url = issue["html_url"]

            message = (
                "🚨 New GitHub Issue!\n\n"
                f"Repository: {owner}/{repository}\n"
                f"Issue: #{issue_number}\n"
                f"Title: {issue_title}\n"
                f"Link: {issue_url}"
            )

            send_telegram_message(message)

            seen_issues.add(
                f"{owner}/{repository}#{issue_number}"
            )

            print(f"Telegram alert sent for issue #{issue_number}")

        save_seen_issues(seen_issues)

        print("Issue history updated.")

    except HTTPError as error:
        print(f"HTTP error: {error.code}")

    except URLError as error:
        print(f"Connection error: {error.reason}")

    except Exception as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()
