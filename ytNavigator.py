from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def setup_driver():
    """Initialize the Chrome WebDriver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    #chrome_options.add_argument("--mute-audio")  # Mute audio
    try:
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        driver.get("https://www.youtube.com/")
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

def accept_cookies(driver):
    """Handle YouTube's cookie banner if it appears."""
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'I agree')]"))
        )
        accept_button.click()
        print("Accepted cookies.")
    except TimeoutException:
        print("No cookie banner found.")

def search_and_play_video(driver, search_query = "Rick Roll"):
    """Search for a video on YouTube and play it."""
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_box.send_keys(search_query)
        search_box.send_keys("\n")
        print(f"Searched for {search_query}.")
        
        # Wait until video results load and click the first video
        first_video = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "video-title"))
        )
        first_video.click()
        print("Playing the first video.")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error finding or playing video: {e}")

def is_ad_playing(driver):
    """Check if an ad overlay is present on the video."""
    try:
        ad_overlay = driver.find_element(By.CLASS_NAME, "video-ads")
        return ad_overlay.is_displayed()
    except NoSuchElementException:
        return False

def skip_ads(driver):
    """Attempt to skip ads by clicking the 'Skip Ad' button if available."""
    try:
        skip_button = WebDriverWait(driver, 6).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button"))
        )
        skip_button.click()
        print("Skipped ad.")
    except TimeoutException:
        print("No skippable ads detected.")

def get_video_playback_time(driver):
    """Retrieve the current playback time of the video."""
    try:
        time_text = driver.find_element(By.CLASS_NAME, "ytp-time-current").text
        minutes, seconds = map(int, time_text.split(":"))
        return minutes * 60 + seconds
    except (NoSuchElementException, ValueError):
        return 0  # If time can't be found, return 0

def play_video_for_two_minutes(driver):
    """Ensure the video plays for two full minutes of playback time."""
    elapsed_play_time = 0  # Track actual playback time in seconds

    while elapsed_play_time < 120:  # Target 2 minutes of actual play time
        try:
            # Check if an ad is playing
            if is_ad_playing(driver):
                print("Ad is playing; waiting for skip button...")
                skip_ads(driver)
            else:
                # Retrieve playback time and update the play counter
                current_play_time = get_video_playback_time(driver)
                if current_play_time > elapsed_play_time:
                    elapsed_play_time = current_play_time
                    print(f"Elapsed play time: {elapsed_play_time} seconds.")
                
            time.sleep(1)  # Check every second

        except Exception as e:
            print(f"Unexpected error: {e}")
            break

    print("Two minutes of video playback completed.")

def main():
    driver = setup_driver()
    if not driver:
        print("Failed to initialize the WebDriver. Exiting script.")
        return

    try:
        # Handle any potential cookie popups
        accept_cookies(driver)
        
        # Search for and play the video
        search_and_play_video(driver)
        
        # Ensure two minutes of actual playback time
        play_video_for_two_minutes(driver)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()
        print("Closed the browser.")

if __name__ == "__main__":
    main()

