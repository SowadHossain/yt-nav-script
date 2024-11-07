from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    """Initialize the Chrome WebDriver with options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Start Chrome maximized
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--mute-audio")  # Mute audio during playback
    try:
        driver = webdriver.Chrome(service=Service(), options=chrome_options)
        driver.get("https://www.youtube.com/")
        return driver
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        return None

def accept_cookies(driver):
    """Handle YouTube's cookie banner if it appears."""
    try:
        # Wait until the accept cookies button is clickable, then click it
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'I agree')]"))
        )
        accept_button.click()
        print("Accepted cookies.")
    except TimeoutException:
        print("No cookie banner found.")

def search_and_play_video(driver, search_query="Selenium tutorial"):
    """Search for a video on YouTube and play it."""
    try:
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        print(f"Searched for {search_query}.")
        
        # Wait until video results load and click the first video
        first_video = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="video-title"]'))
        )
        first_video.click()
        print("Playing the first video.")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error finding or playing video: {e}")

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
        
        # Allow video to play for a short while
        time.sleep(10)  # Play for 10 seconds (can be adjusted)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()
        print("Closed the browser.")

if __name__ == "__main__":
    main()

