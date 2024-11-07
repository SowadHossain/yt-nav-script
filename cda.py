from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import threading
import time
import cv2
import numpy as np
import pyaudio
from PIL import ImageGrab
import wave

# Screen capture settings
screen_width = 1920  # Set your screen width
screen_height = 1080  # Set your screen height

# Audio settings
audio_format = pyaudio.paInt16
channels = 2
rate = 44100
chunk = 1024
audio_output = "output.wav"
video_output = "output.avi"

# Initialize PyAudio and OpenCV
p = pyaudio.PyAudio()
frames = []
capture_video = True  # Control variable for recording state

# Set up OpenCV VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_output, fourcc, 20.0, (screen_width, screen_height))

# Set up Selenium for ad detection on YouTube
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and accessible

def setup_youtube(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "video-title")))
    driver.find_element(By.ID, "video-title").click()

def is_ad_playing():
    """Detect if an ad overlay is present on the YouTube video."""
    try:
        ad_overlay = driver.find_element(By.CLASS_NAME, "video-ads")
        return ad_overlay.is_displayed()
    except NoSuchElementException:
        return False

# Define audio recording function
def record_audio():
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    while countdown > 0:
        if capture_video:
            data = stream.read(chunk)
            frames.append(data)
        else:
            stream.read(chunk)  # Read to maintain stream continuity
    stream.stop_stream()
    stream.close()

# Define screen capture function
def record_screen():
    global capture_video
    while countdown > 0:
        if capture_video:
            img = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            out.write(frame)
        time.sleep(0.05)  # Control frame rate

# Ad monitoring function to toggle recording based on ad presence
def monitor_ad_status():
    global capture_video
    while countdown > 0:
        capture_video = not is_ad_playing()
        time.sleep(1)

# Timer and countdown to show remaining time
countdown = 120  # 2 minutes in seconds
def countdown_timer():
    global countdown
    while countdown > 0:
        print(f"Time remaining: {countdown} seconds", end='\r')
        time.sleep(1)
        countdown -= 1
    print("Recording completed!               ")

# Function to start the navigation and recording process
def youtube_navigator():
    # Setup YouTube video
    setup_youtube()

    # Start audio, screen recording, ad monitor, and timer threads
    audio_thread = threading.Thread(target=record_audio)
    screen_thread = threading.Thread(target=record_screen)
    ad_monitor_thread = threading.Thread(target=monitor_ad_status)
    timer_thread = threading.Thread(target=countdown_timer)

    # Start threads
    audio_thread.start()
    screen_thread.start()
    ad_monitor_thread.start()
    timer_thread.start()

    # Wait for all threads to finish
    audio_thread.join()
    screen_thread.join()
    ad_monitor_thread.join()
    timer_thread.join()

    # Save audio file
    with wave.open(audio_output, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    out.release()
    p.terminate()

    print("Recording saved as", video_output, "and", audio_output)

# Run the YouTube navigator
youtube_navigator()

