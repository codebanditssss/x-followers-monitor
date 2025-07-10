# X Followers Monitor

A Python tool to monitor your X (formerly Twitter) followers, track who unfollows you, and maintain a history of follower changes. Can be run locally or automated using GitHub Actions.

---

## 🚀 Quickstart Tutorial

### 1. Clone the Repository

```bash
git clone https://github.com/prathamdby/x-followers-monitor.git
cd x-followers-monitor
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
playwright install-deps chromium
```

### 4. Obtain X (Twitter) Cookies

- Install the [Cookie-Editor](https://cookie-editor.cgagnier.ca/) browser extension.
- Log into X (Twitter) in your browser.
- Use Cookie-Editor to export cookies as JSON.
- Save them as `cookies.json` in the project root **OR** set as an environment variable (see below).

### 5. Set Environment Variables

- **Required:**
  - `X_USERNAME`: Your X (Twitter) username (without @)
  - `X_COOKIES`: Paste your cookies JSON as a string (must be exported as JSON from Cookie-Editor)
- **Optional:**
  - `DISCORD_WEBHOOK_URL`: Your Discord webhook URL to receive follower updates

**Example (Windows):**

```bash
set X_USERNAME=your_username
set X_COOKIES={...your_cookies_json...}
set DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
```

**Example (macOS/Linux):**

```bash
export X_USERNAME=your_username
export X_COOKIES='{...your_cookies_json...}'
export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_url
```

### 6. Run the Script

```bash
python main.py
```

---

## 🔔 Discord Webhook Integration

- If you set the `DISCORD_WEBHOOK_URL` environment variable, the script will post follower changes to your Discord channel after each run.
- The webhook message includes new followers, unfollowers, and net change.
- You can create a webhook in your Discord server settings (Server Settings > Integrations > Webhooks > New Webhook).

---

## 🛠️ Advanced: GitHub Actions Setup

1. Go to your repository's **Settings > Secrets and Variables > Actions**.
2. Add the following secrets (all required except webhook):
   - `X_COOKIES`: Your cookies JSON string (required)
   - `X_USERNAME`: Your X username (required)
   - `DISCORD_WEBHOOK_URL` (optional): Your Discord webhook URL
3. The workflow will run automatically every 6 hours or can be triggered manually from the Actions tab.

---

## 📦 Output Files

- `followers_data.json`: Current snapshot of your followers
- `followers_history/`: Directory containing historical data
  - `latest.json`: Most recent follower data
  - `followers_YYYYMMDD_HHMMSS.json`: Timestamped snapshots

---

## 📝 Notes

- Never commit your `cookies.json` file or secrets to version control.
- If you see login errors, refresh your cookies.
- If selectors break, X (Twitter) may have changed their frontend; update selectors in `main.py`.

---

## License

MIT
