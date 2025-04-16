from flask import Flask, render_template, Response, redirect, url_for, jsonify
import cv2
import numpy as np
import pygame
import threading
import os
import time
import sys

# Add the detector directory to the path so we can import from it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from detector.detector import DrowsinessDetector

app = Flask(__name__)
detector = None
detection_active = False
camera = None

# Funny messages to display when drowsiness is detected
bot_messages = [
    "Wake up, you idiot!",
    "Hey sleepyhead, eyes on the road!",
    "Stop dreaming and start driving!",
    "Coffee break needed!",
    "Wakey wakey, eggs and bakey!",
    "Snap out of it!",
    "No snoozing allowed!",
    "Are you sleeping on the job?",
    "Alert! Human malfunction detected!",
    "WAKE UP! Life is happening!"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect')
def detect():
    return render_template('detect.html')

def get_frame():
    global detector, detection_active
    
    detection_active = True
    detector = DrowsinessDetector()
    
    while detection_active:
        frame, status = detector.process_frame()
        if frame is not None:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break
    
    detector.release()

@app.route('/video_feed')
def video_feed():
    return Response(get_frame(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_detection')
def stop_detection():
    global detection_active
    detection_active = False
    time.sleep(1)  # Give time for the video feed to stop
    return redirect(url_for('index'))

@app.route('/get_status')
def get_status():
    global detector
    if detector:
        return jsonify({'status': detector.get_status(), 'message': detector.get_message()})
    return jsonify({'status': 'none', 'message': ''})

if __name__ == '__main__':
    app.run(debug=True)