# Drowsiness Detector Flask App

This is a simple Flask web application that uses OpenCV and Haarcascades for face and eye detection to monitor drowsiness levels. If the user blinks multiple times in a short period, an alarm sounds as a wake-up warning. It includes a front-end interface and runs in a web browser.

## Features
- **Real-time Drowsiness Detection**: Tracks face and eye movements to detect if the user is falling asleep.
- **Wake-up Alarm**: Plays an alarm sound if the user is detected as drowsy.
- **Simple Interface**: A clean, interactive front-end with a button to start and end detection.
- **Flask Backend**: Utilizes Flask to serve the web pages and manage detection sessions.

## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Flask
- **Detection**: OpenCV, Haarcascades for face and eye detection
- **Sound**: Pygame for alarm sound

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask app: `python app.py`
4. Access the app on `http://127.0.0.1:5000/`

## Contributions
Feel free to fork this repo, make changes, and submit pull requests. All suggestions are welcome!
