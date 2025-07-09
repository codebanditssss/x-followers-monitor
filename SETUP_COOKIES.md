# Setting Up X Cookies as GitHub Secret

## Steps to Configure

1. **Get your cookies from X (Twitter)**:

   - Log into X/Twitter in your browser
   - Open Developer Tools (F12)
   - Go to Application/Storage → Cookies
   - Export all cookies for `x.com` domain

2. **Format cookies as JSON array**:

   ```json
   [
     {
       "name": "cookie_name",
       "value": "cookie_value",
       "domain": ".x.com",
       "path": "/",
       "secure": true,
       "httpOnly": true,
       "sameSite": "None"
     }
     // ... more cookies
   ]
   ```

3. **Add to GitHub Secrets**:

   - Go to your repository on GitHub
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `X_COOKIES`
   - Value: Paste your JSON array (minified, all on one line)
   - Click "Add secret"

4. **Test the workflow**:
   - Go to Actions tab
   - Select "Monitor X Followers"
   - Click "Run workflow"
   - Check the logs to ensure it's working

## Security Notes

- Never commit cookies to your repository
- Rotate cookies periodically
- GitHub Secrets are encrypted and only exposed to workflows
- The workflow now loads cookies from the `X_COOKIES` secret

## Local Development

For local testing, you can still use `cookies.json` file. The script will:

1. First check for `cookies.json` file
2. If not found, check for `X_COOKIES` environment variable
3. Raise an error if neither is found
