# GitHub Issue Radar 🚀

An automated GitHub issue monitoring bot that detects newly opened issues in a GitHub repository and sends notifications to Telegram.

Built with Python, the GitHub REST API, Telegram Bot API, and GitHub Actions.

## 📌 Overview

Keeping track of new issues in GitHub repositories can be time-consuming, especially when monitoring projects with active development.

GitHub Issue Radar automates this process by periodically checking a repository for newly opened issues, identifying issues that haven't been seen before, and sending Telegram notifications.

The bot runs automatically using GitHub Actions, so it doesn't require a local machine to remain running.

## ✨ Features

- **Automated Issue Monitoring:** Periodically checks GitHub repositories for newly opened issues.
- **New Issue Detection:** Identifies issues that haven't been recorded in the issue history.
- **Telegram Notifications:** Sends alerts when new issues are detected.
- **Duplicate Prevention:** Maintains issue history to avoid repeatedly notifying about the same issue.
- **Scheduled Execution:** Runs automatically every 30 minutes using GitHub Actions.
- **Secure Configuration:** Uses GitHub Secrets to store sensitive credentials.
- **Manual Execution:** Supports manually triggering the monitoring workflow.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| GitHub REST API | Retrieves repository issues |
| Telegram Bot API | Sends notifications |
| GitHub Actions | Automates scheduled execution |
| JSON | Stores issue history |

## ⚙️ How It Works

1. GitHub Actions triggers the monitoring script every 30 minutes.
2. The Python script connects to the GitHub REST API.
3. It retrieves open issues from the configured repository.
4. Pull requests are excluded from the issue list.
5. The script compares the retrieved issues against the saved issue history.
6. Newly detected issues are sent to Telegram.
7. The updated issue history is saved to prevent duplicate notifications.

### Workflow

```text
GitHub Actions
      |
      v
Run Python Script
      |
      v
Fetch GitHub Issues
      |
      v
Filter Pull Requests
      |
      v
Compare with Issue History
      |
      v
New Issues Detected?
      |
      +---- Yes ----> Send Telegram Alert
      |                     |
      |                     v
      |              Update Issue History
      |
      +---- No -----> No Notification
                            |
                            v
                    Save Issue History
```

## 📂 Project Structure

```text
github-issue-radar/
│
├── .github/
│   └── workflows/
│       └── monitor.yml
│
├── monitor.py
├── issues_seen.json
├── .gitignore
└── README.md
```

| File | Description |
|---|---|
| `monitor.py` | Main Python script that monitors issues and sends Telegram alerts |
| `issues_seen.json` | Stores previously detected issue IDs |
| `monitor.yml` | GitHub Actions workflow for automated execution |
| `.gitignore` | Specifies files Git should ignore |
| `README.md` | Project documentation |

## 🚀 Setup and Usage

### 1. Clone the repository

```bash
git clone https://github.com/Deekshitha-089/github-issue-radar.git
```

Navigate into the project:

```bash
cd github-issue-radar
```

### 2. Configure Telegram

Create a Telegram bot using [BotFather](https://t.me/BotFather).

Obtain:
- Telegram bot token
- Telegram chat ID

### 3. Configure environment variables

Set the following environment variables:

```text
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

Never expose your bot token publicly or commit it to the repository.

### 4. Run the monitoring script

```bash
python monitor.py
```

The script checks for new issues and sends a Telegram notification when a new issue is detected.

## 🔐 GitHub Actions Configuration

To enable automated monitoring, configure the following repository secrets:

| Secret | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot authentication token |
| `TELEGRAM_CHAT_ID` | Telegram chat ID that receives notifications |

Navigate to:

**GitHub Repository → Settings → Secrets and variables → Actions → New repository secret**

Add both secrets.

The workflow runs automatically every 30 minutes and can also be triggered manually from the Actions tab.

## 📩 Example Notification

When a new issue is detected, the bot sends a Telegram notification containing issue information, including:

- Issue title
- Repository
- Issue number
- Issue URL

## 🎯 Project Goals

This project was built to explore and practice:

- Working with REST APIs
- Automating repetitive tasks using Python
- Detecting changes in external data
- Sending notifications using a messaging API
- Scheduling scripts using GitHub Actions
- Managing credentials securely using GitHub Secrets

## 🔮 Future Improvements

- Monitor multiple repositories simultaneously.
- Add issue labels and author information to notifications.
- Support filtering issues by labels or keywords.
- Add a daily issue summary.
- Add configurable monitoring intervals.
- Improve error handling and logging.

## 👩‍💻 Author

**Deekshitha**

GitHub: [Deekshitha-089](https://github.com/Deekshitha-089)

---
