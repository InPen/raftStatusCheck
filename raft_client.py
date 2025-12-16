# raft_client.py
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

CASESEARCH_URL = "https://applyhousinghelp.mass.gov/s/casesearch?LanguageCode=en_US&language=en_US"


def fetch_raft_status(case_number: str, last_name: str, headless: bool = True) -> dict:
    """
    Open the public RAFT Case Search page, submit case number + last name,
    and scrape the basic status info.

    Returns a dict like:
    {
        "client_name": "...",
        "raft_case_number": "...",
        "status": "...",
        "scraped_at": "2025-12-16T...",
    }
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        try:
            page.goto(CASESEARCH_URL, wait_until="networkidle", timeout=30000)

            # 1) Fill the "Case Number" input
            # The page text (from public descriptions) says:
            #   * Enter Case Number or ETO Case Number:
            # so we try to use the accessible label.
            page.get_by_label("Enter Case Number or ETO Case Number", exact=False).fill(case_number)

            # 2) Fill the "Last Name" input
            page.get_by_label("Enter Last Name or Legal Business Name", exact=False).fill(last_name)

            # 3) Click the search/check-status button
            # We don't know the exact text, so we try a few common names.
            try:
                page.get_by_role("button", name="Search").click()
            except Exception:
                page.get_by_role("button", name="Check Status").click()

            # 4) Wait for results to load
            page.wait_for_load_state("networkidle", timeout=15000)

            # 5) Scrape result fields.
            # We don't know the exact DOM yet, so we'll try some generic patterns.
            def safe_text(selector: str):
                try:
                    return page.locator(selector).first.inner_text().strip()
                except Exception:
                    return None

            # These will be adjusted once you inspect the actual HTML.
            # For now, these are "best guess" selectors:
            client_name = safe_text("text=/Applicant Name/i >> xpath=..//div[2]") or safe_text(
                "text=/Applicant Name/i"
            )
            raft_case_number = safe_text("text=/Case Number/i >> xpath=..//div[2]") or case_number
            status = safe_text("text=/Status/i >> xpath=..//div[2]") or safe_text("text=/Status/i")

            result = {
                "client_name": client_name,
                "raft_case_number": raft_case_number,
                "status": status,
                "scraped_at": datetime.utcnow().isoformat() + "Z",
            }

        except PWTimeout as e:
            result = {"error": "timeout", "message": str(e)}
        except Exception as e:
            result = {"error": "scrape_failed", "message": str(e)}
        finally:
            browser.close()

        return result


if __name__ == "__main__":
    # Manual test helper
    case_num = input("Enter RAFT Case Number: ").strip()
    last = input("Enter Last Name: ").strip()
    data = fetch_raft_status(case_num, last, headless=False)  # show browser while testing
    print("\n=== RESULT ===")
    print(data)
