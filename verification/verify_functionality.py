import time
import sys
from playwright.sync_api import sync_playwright

def verify_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Capture console logs
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

        print("1. Navigating to Home Page...")
        page.goto("http://localhost:5173")

        # Inject CSS
        page.add_style_tag(content="""
            *, *::before, *::after {
                animation-duration: 0s !important;
                transition-duration: 0s !important;
            }
            div.absolute { pointer-events: none !important; }
            button, input, div.relative.z-30, span.cursor-pointer { pointer-events: auto !important; }
        """)

        print("2. Handling Intro...")
        try:
            ignite_btn = page.locator("button:has-text('IGNITE')")
            if ignite_btn.is_visible(timeout=3000):
                print("   Intro visible. Clicking Ignite...")
                ignite_btn.click()
                time.sleep(1)
            else:
                print("   Intro not visible.")
        except Exception as e:
            print(f"   Intro check failed: {e}")

        print("3. Selecting a Category / Checking Input...")
        try:
            page.wait_for_selector("input[type='text']", state="visible", timeout=5000)
            print("   Input is visible.")
        except:
            print("   Input hidden...")

        print("4. Entering Research Query...")
        page.fill("input[type='text']", "Future of AI in 2025")

        print("5. Starting Research...")
        try:
            search_btn = page.locator("label button:has(span.material-symbols-outlined:has-text('arrow_forward'))")
            search_btn.click(force=True)
            print("   Clicked search button.")
        except Exception as e:
            print(f"   Button click failed ({e}), trying Enter key...")
            page.keyboard.press("Enter")

        print("6. Waiting for Research Results (redirect to editor)...")
        try:
            page.wait_for_url(r"**/editor/research/*", timeout=10000)
            print(f"   Redirected to: {page.url}")
        except Exception as e:
            print("   Wait for URL failed. Taking screenshot.")
            page.screenshot(path="verification/failure_screenshot.png")
            raise e

        print("7. Polling for Completion...")
        try:
            page.wait_for_selector("text=Mock Draft Content", timeout=30000)
            print("   Research completed and content loaded.")
        except Exception as e:
            print(f"   Timed out waiting for content: {e}")
            page.screenshot(path="verification/timeout_debug.png")
            raise e

        print("8. Saving Draft...")
        try:
            # The save button is a span in the header with text "Save"
            save_btn = page.locator("header span:has-text('Save')")
            if save_btn.count() > 0:
                save_btn.click(force=True)
                print("   Clicked Save.")
                # Wait for navigation to /editor/draft/...
                page.wait_for_url(r"**/editor/draft/*", timeout=5000)
                print(f"   Saved and redirected to draft: {page.url}")
            else:
                print("   Save button not found.")
                print(page.locator("header").inner_html())
        except Exception as e:
             print(f"   Save click failed: {e}")

        time.sleep(2)

        print("9. Navigating to Library...")
        page.goto("http://localhost:5173/library")

        print("10. Verifying Draft in Library...")
        try:
            # Look for the title of the research which becomes the draft title
            # In PrismEditorPage, it sets title to `result.query.original` which is "Future of AI in 2025"
            page.wait_for_selector("text=Future of AI in 2025", timeout=5000)
            print("   Draft found in library.")
        except:
             print("   Draft NOT found in library.")
             page.screenshot(path="verification/library_fail.png")

        print("11. Opening Draft...")
        try:
            page.click("text=Future of AI in 2025")
            page.wait_for_url(r"**/editor/draft/*")
            print(f"   Opened draft at: {page.url}")
            page.wait_for_selector("text=Mock Draft Content")
            print("   Draft content verified.")
        except Exception as e:
            print(f"   Failed to open draft: {e}")

        print("\nSUCCESS: Full flow verified!")
        page.screenshot(path="verification/success.png")
        browser.close()

if __name__ == "__main__":
    verify_flow()
