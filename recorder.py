import cv2
import numpy as np
import pyaudio
import wave
import threading
import time
from PIL import ImageGrab  # Use PIL for screen capture

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

# Set up OpenCV VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(video_output, fourcc, 20.0, (screen_width, screen_height))

# Define audio recording function
def record_audio():
    stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    for _ in range(0, int(rate / chunk * 120)):  # 120 chunks for 2 minutes
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()

# Define screen capture function
def record_screen():
    end_time = time.time() + 120  # 2 minutes
    while time.time() < end_time:
        # Capture the screen
        img = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        out.write(frame)
        cv2.waitKey(10)

# Timer function to show remaining time in seconds
def countdown_timer(duration):
    for remaining in range(duration, 0, -1):
        print(f"Time remaining: {remaining} seconds", end='\r')
        time.sleep(1)
    print("Recording completed!               ")

# Run audio, video recording, and timer threads
audio_thread = threading.Thread(target=record_audio)
screen_thread = threading.Thread(target=record_screen)
timer_thread = threading.Thread(target=countdown_timer, args=(120,))  # 2 minutes countdown

audio_thread.start()
screen_thread.start()
timer_thread.start()

audio_thread.join()
screen_thread.join()
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

