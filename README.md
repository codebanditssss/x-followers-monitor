# X Followers Monitor

A Python tool to monitor your X (formerly Twitter) followers, track who unfollows you, and maintain a history of follower changes.

## Features

- Track followers and their changes over time
- Store follower history with timestamps
- Detect new followers and unfollowers
- Export data in JSON format
- Headless browser automation using Playwright

## Prerequisites

- Python 3.7 or higher
- Git
- A valid X (Twitter) account

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/x-followers-monitor.git
   cd x-followers-monitor
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install playwright
   playwright install chromium
   ```

## Setup

1. Log into X (Twitter) using Chrome
2. Open Developer Tools (F12 or Ctrl+Shift+I)
3. Go to the "Application" tab
4. Under "Storage" > "Cookies", click on "https://twitter.com" or "https://x.com"
5. Export all cookies to a file named `cookies.json` in the project root directory

## Configuration

Edit `main.py` and update the `USERNAME` variable with your X username:

```python
USERNAME = "your_username_here"
```

## Usage

Run the script:

```bash
python main.py
```

The script will:

1. Load your cookies for authentication
2. Navigate to your followers page
3. Scroll through and collect all follower data
4. Save the results in the following files:
   - `followers_data.json`: Current followers
   - `followers_history/latest.json`: Most recent snapshot
   - `followers_history/followers_TIMESTAMP.json`: Historical snapshots

## Output Files

- `followers_data.json`: Contains current follower data
- `followers_history/`: Directory containing historical snapshots
  - `latest.json`: Most recent follower data
  - `followers_YYYYMMDD_HHMMSS.json`: Timestamped snapshots

## Notes

- The script uses a headless browser, so you won't see the browser window
- Make sure your cookies are valid and up-to-date
- The script may take several minutes to run depending on your follower count
- Rate limiting or temporary blocks may occur if used too frequently

## Security

- Never commit your `cookies.json` file to version control
- Keep your cookies secure as they provide access to your X account
- Regularly update your cookies if authentication fails

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is open source and available under the MIT License.
