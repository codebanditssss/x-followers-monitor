import json
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import os
import logging

USERNAME = "prathamdby"

COOKIES_FILE = "cookies.json"
OUTPUT_FILE = "followers_data.json"
HISTORY_DIR = "followers_history"
LATEST_FILE = os.path.join(HISTORY_DIR, "latest.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_cookies():
    """Load cookies from file or environment variable"""
    if os.path.exists(COOKIES_FILE):
        logger.info("Loading cookies from file")
        with open(COOKIES_FILE, "r") as f:
            return json.load(f)
    elif os.environ.get("X_COOKIES"):
        logger.info("Loading cookies from environment variable")
        cookies_data = os.environ.get("X_COOKIES")
        cookies = json.loads(cookies_data)
        # Optionally save to file for debugging (remove in production)
        # with open(COOKIES_FILE, "w") as f:
        #     json.dump(cookies, f, indent=2)
        return cookies
    else:
        raise ValueError(
            "No cookies found. Please provide cookies.json or set X_COOKIES environment variable"
        )


def normalize_same_site(cookie):
    val = cookie.get("sameSite")
    cookie["sameSite"] = {
        "no_restriction": "None",
        "lax": "Lax",
        "strict": "Strict",
    }.get(str(val).lower() if val is not None else None, "None")
    return cookie


def get_follower_data(page):
    try:
        return page.evaluate(
            """() => {
            const cells = document.querySelectorAll('div[data-testid="cellInnerDiv"]');
            const results = [];
            cells.forEach(cell => {
                const nameElement = cell.querySelector('a[role="link"] span.css-1jxf684.r-dnmrzs.r-1udh08x.r-1udbk01.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3 > span');
                const usernameElement = cell.querySelector('div[dir="ltr"].css-146c3p1.r-dnmrzs.r-1udh08x.r-1udbk01.r-3s2u2q.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-18u37iz.r-1wvb978 > span');
                if (nameElement && usernameElement) {
                    const name = nameElement.innerText.trim();
                    const username = usernameElement.innerText.trim().replace('@', '');
                    if (name && username && !name.includes('@')) {
                        results.push({name: name, username: username});
                    }
                }
            });
            return results;
        }"""
        )
    except Exception as e:
        logger.error(f"Error extracting follower data: {e}")
        return []


def load_previous_data():
    if os.path.exists(LATEST_FILE):
        with open(LATEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def compare_followers(previous_data, current_data):
    if not previous_data:
        return None

    prev_usernames = {f["username"] for f in previous_data["followers"]}
    curr_usernames = {f["username"] for f in current_data["followers"]}

    unfollowed = prev_usernames - curr_usernames
    new_followers = curr_usernames - prev_usernames

    unfollowed_data = [
        f for f in previous_data["followers"] if f["username"] in unfollowed
    ]
    new_follower_data = [
        f for f in current_data["followers"] if f["username"] in new_followers
    ]

    return {
        "unfollowed": unfollowed_data,
        "new_followers": new_follower_data,
        "unfollowed_count": len(unfollowed),
        "new_followers_count": len(new_followers),
    }


def save_progress(follower_data, username):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    logger.info(f"Saving progress for {len(follower_data)} followers")

    followers_with_urls = []
    for name, uname in sorted(follower_data):
        followers_with_urls.append(
            {"name": name, "username": uname, "profile_url": f"https://x.com/{uname}"}
        )

    data = {
        "username": username,
        "timestamp": datetime.now().isoformat(),
        "total_followers": len(follower_data),
        "followers": followers_with_urls,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    with open(LATEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(HISTORY_DIR, f"followers_{timestamp}.json")
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Data saved to {OUTPUT_FILE} and {backup_file}")


def smart_scroll(page):
    page.evaluate(
        """() => {
        const currentScroll = window.pageYOffset;
        const viewportHeight = window.innerHeight;
        window.scrollTo(0, currentScroll + viewportHeight * 0.7);
        const timeline = document.querySelector('div[aria-label="Timeline: Followers"]');
        if (timeline) {
            timeline.scrollBy(0, 400);
        }
    }"""
    )
    time.sleep(1.5)


def wait_for_new_content(page, old_count, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if len(page.query_selector_all('div[data-testid="cellInnerDiv"]')) > old_count:
            return True
        time.sleep(0.2)
    return False


def scroll_followers_list(page, username):
    logger.info("Starting follower collection process...")
    try:
        page.wait_for_selector('div[data-testid="cellInnerDiv"]', timeout=15000)
        logger.info("Initial followers loaded")
    except:
        logger.warning("Could not find follower cells, trying alternative approach...")

    follower_data = set()
    no_new_content_count = 0
    scroll_count = 0

    initial_follower_data = get_follower_data(page)
    for item in initial_follower_data:
        follower_data.add((item["name"], item["username"]))

    logger.info(f"Initial collection: {len(follower_data)} unique followers")

    while no_new_content_count < 10 and scroll_count < 500:
        scroll_count += 1
        logger.debug(f"Scroll #{scroll_count}")

        current_cells = len(page.query_selector_all('div[data-testid="cellInnerDiv"]'))
        smart_scroll(page)
        wait_for_new_content(page, current_cells, timeout=5)

        previous_count = len(follower_data)
        for item in get_follower_data(page):
            follower_data.add((item["name"], item["username"]))

        followers_added = len(follower_data) - previous_count
        logger.debug(f"New followers found: {followers_added}")

        if followers_added == 0:
            no_new_content_count += 1
            logger.debug(f"No new followers ({no_new_content_count}/10)")
        else:
            no_new_content_count = 0

        if scroll_count % 15 == 0:
            save_progress(follower_data, username)
            logger.info(
                f"Progress checkpoint: {len(follower_data)} followers collected"
            )

    logger.info(f"Scrolling completed! Total followers collected: {len(follower_data)}")
    save_progress(follower_data, username)
    return follower_data


def extract_username_from_url(url):
    parts = url.split("/")
    for i, part in enumerate(parts):
        if part == "x.com" and i + 1 < len(parts):
            return parts[i + 1]
    return "unknown"


def main():
    logger.info("Starting X followers monitor")

    try:
        cookies = load_cookies()
        cookies = [normalize_same_site(cookie) for cookie in cookies]
    except ValueError as e:
        logger.error(f"Error loading cookies: {e}")
        return

    with sync_playwright() as p:
        logger.info("Launching browser in headless mode")
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-web-security",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
            ],
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 4200},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        context.add_cookies(cookies)
        page = context.new_page()

        url = f"https://x.com/{USERNAME}/followers"
        username = extract_username_from_url(url)
        logger.info(f"Navigating to {username}'s followers page")

        page.goto(url)
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)

        if "log in" in page.content().lower():
            logger.error("Not logged in properly. Check your cookies.")
            browser.close()
            return

        logger.info("Page loaded successfully")
        previous_data = load_previous_data()

        try:
            follower_data = scroll_followers_list(page, username)
            current_data = {
                "username": username,
                "timestamp": datetime.now().isoformat(),
                "total_followers": len(follower_data),
                "followers": [
                    {
                        "name": name,
                        "username": uname,
                        "profile_url": f"https://x.com/{uname}",
                    }
                    for name, uname in sorted(follower_data)
                ],
            }

            if previous_data:
                logger.info(f"Comparing with data from {previous_data['timestamp']}")
                changes = compare_followers(previous_data, current_data)
                if changes:
                    logger.info("=== CHANGES SINCE LAST RUN ===")
                    if changes["unfollowed_count"] > 0:
                        logger.info(
                            f"❌ {changes['unfollowed_count']} people unfollowed"
                        )
                        for user in changes["unfollowed"]:
                            logger.info(f"  - {user['name']} (@{user['username']})")
                    else:
                        logger.info("✅ No one unfollowed")

                    if changes["new_followers_count"] > 0:
                        logger.info(
                            f"🎉 {changes['new_followers_count']} new followers:"
                        )
                        for user in changes["new_followers"]:
                            logger.info(f"  - {user['name']} (@{user['username']})")
                    else:
                        logger.info("📊 No new followers")

                    net_change = (
                        changes["new_followers_count"] - changes["unfollowed_count"]
                    )
                    if net_change > 0:
                        logger.info(f"📈 Net gain: +{net_change} followers")
                    elif net_change < 0:
                        logger.info(f"📉 Net loss: {net_change} followers")
                    else:
                        logger.info("➖ No net change in followers")
            else:
                logger.info("First run - no previous data to compare")

        except Exception as e:
            logger.error(f"Error during follower collection: {e}", exc_info=True)

        logger.info("Closing browser")
        browser.close()


if __name__ == "__main__":
    main()
