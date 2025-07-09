# X Followers Monitor

A Python tool to monitor your X (formerly Twitter) followers, track who unfollows you, and maintain a history of follower changes. Can be run locally or automated using GitHub Actions.

## Features

- Track followers and their changes over time
- Store follower history with timestamps
- Detect new followers and unfollowers
- Export data in JSON format
- Headless browser automation using Playwright
- GitHub Actions integration for automated monitoring
- Supports both local and environment-based configuration

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
   playwright install-deps chromium
   ```

## Setup Options

You can run this tool either locally or using GitHub Actions. Choose one of the following setup methods:

### Option 1: Local Setup with cookies.json

1. Install Cookie-Editor extension for your browser:

   - [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   - [Firefox](https://addons.mozilla.org/firefox/addon/cookie-editor/)
   - [Edge](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi)
   - [Safari](https://apps.apple.com/app/cookie-editor/id6446215341)
   - [Opera](https://addons.opera.com/extensions/details/cookie-editor/)

2. Log into X (Twitter) in your browser
3. Click on the Cookie-Editor extension icon in your browser toolbar
4. Click "Export" and select "Export as JSON" (this copies all cookies to clipboard in JSON format)
5. Create a new file named `cookies.json` in the project root directory
6. Paste the copied JSON cookies into `cookies.json`

### Option 2: Environment Variables Setup (Recommended for GitHub Actions)

1. Get your X cookies using Cookie-Editor (follow steps 1-4 from Option 1)
2. In your GitHub repository:
   - Go to Settings > Secrets and Variables > Actions
   - Add the following secrets:
     - `X_COOKIES`: Paste your copied JSON cookies data here (make sure you used "Export as JSON")
     - `X_USERNAME`: Your X username (without @ symbol)

## Usage

### Local Usage

1. Set your X username in one of two ways:

   - Edit `main.py` and update the USERNAME variable:
     ```python
     USERNAME = "your_username_here"
     ```
   - Or set the X_USERNAME environment variable:
     ```bash
     # Windows
     set X_USERNAME=your_username_here
     # Linux/macOS
     export X_USERNAME=your_username_here
     ```

2. Run the script:
   ```bash
   python main.py
   ```

### GitHub Actions Usage

1. The workflow is already configured to run automatically every 6 hours
2. You can also trigger it manually:
   - Go to your repository's Actions tab
   - Select "Monitor X Followers" workflow
   - Click "Run workflow"

## Output Files

The script generates the following files:

- `followers_data.json`: Current snapshot of your followers
- `followers_history/`: Directory containing historical data
  - `latest.json`: Most recent follower data
  - `followers_YYYYMMDD_HHMMSS.json`: Timestamped snapshots

When using GitHub Actions:

- Data is saved as workflow artifacts
- Artifacts are retained for 90 days
- Each run updates the existing artifacts

## Understanding the Output

The script provides detailed information about follower changes:

- Total follower count
- New followers since last run
- Users who unfollowed since last run
- Net change in followers
- Timestamps for tracking

Each follower entry includes:

- Display name
- Username
- Profile URL

## Security Notes

- Never commit your `cookies.json` file to version control
- When using GitHub Actions, always use repository secrets
- Keep your cookies secure as they provide access to your X account
- Regularly update your cookies if authentication fails
- The script uses a headless browser for security

## Troubleshooting

- If you see "Not logged in properly" error:
  - Your cookies might be expired
  - Update your cookies data
  - Make sure all required cookies are included
- If the script stops prematurely:
  - Check your internet connection
  - Verify your X account is not rate limited
  - Try running the script again after a few minutes

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is open source and available under the MIT License.
