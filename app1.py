import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import requests
import json
import http.server
import socketserver
import os
import socket
from flask import Flask, send_from_directory
import threading

# Setup GPIO pins
DHT_PIN = 14
soil = 15
ldr = 23
Gas = 24
motion = 25
relay_water = 21
relay_plant = 20

SENSOR_TYPE = Adafruit_DHT.DHT11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN, GPIO.IN)
GPIO.setup(soil, GPIO.IN)
GPIO.setup(ldr, GPIO.IN)
GPIO.setup(Gas, GPIO.IN)
GPIO.setup(motion, GPIO.IN)
GPIO.setup(relay_water, GPIO.OUT)
GPIO.setup(relay_plant, GPIO.OUT)

# Load TensorFlow model
model = load_model('efficientnet.h5')

# Disease classes
disease_classes = {
    0: 'Aphids',
    1: 'Armyworm',
    2: 'Beetle',
    3: 'Bollworm',
    4: 'Grasshopper',
    5: 'Mites',
    6: 'Mosquito',
    7: 'Sawfly',
    8: 'Stem_borer',
}

# Flask server setup
app = Flask(__name__)

# Set the directory where your images are stored
IMAGE_FOLDER = 'images'
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER



# Ensure the image directory exists
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

# Function to send data to the database
def load_json():
    
    response = requests.get('https://iotcloud22.in/3791_smart_plant/light.json')
    if response.status_code == 200:
        data = response.json()
        light = data.get('light')
        if light == "on1":
            GPIO.output(relay_water, GPIO.HIGH)
        elif light == "off1":
            GPIO.output(relay_water, GPIO.LOW)
        elif light == "on2":
            GPIO.output(relay_plant, GPIO.HIGH)
        elif light == "off2":
            GPIO.output(relay_plant, GPIO.LOW)
            
def send_db():
    global text
    hum, temp = Adafruit_DHT.read_retry(SENSOR_TYPE, DHT_PIN)
    Temp = str(temp) + "°C"
    Hum = str(hum) + "%"
    gas = GPIO.input(Gas)
    ldr_value = GPIO.input(ldr)
    soil_value = GPIO.input(soil)
    motion_value = GPIO.input(motion)
    plant = str(text)
    # Get image URL for the stored image
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 80))

    ip_address = s.getsockname()[0]
    print(ip_address)
    image_url = f"http://{ip_address}:5000/image/output.jpg"

    # Prepare data for the server
    data = {
        "value1": Temp,
        "value2": Hum,
        "value3": str(gas),
        "value4": str(ldr_value),
        "value5": str(soil_value),
        "value6": str(plant),
        "value7": image_url,
        "value8": str(motion_value)
    }
    print("Data : ",data)
    
    # Post data to the remote server
    url = 'https://iotcloud22.in/3791_smart_plant/post_value.php'
    response = requests.post(url, data=data)
    print("HTTP Response:", response.status_code)

# Function to process the video feed
def process_video():
    global text
#     load_json()
    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        img = cv2.resize(frame, (300, 300))
        a = tf.keras.preprocessing.image.img_to_array(img)
        a = np.expand_dims(a, axis=0)
        imag = np.vstack([a])
        predict = model.predict(imag)
        classes = np.argmax(predict)
        print(classes)
        if classes == 0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
            GPIO.output(relay_plant, GPIO.HIGH)
            sleep(1)
            GPIO.output(relay_plant, GPIO.LOW)
            sleep(1)
        text = disease_classes[classes]
        print(text)
        # Draw text on the frame
        cv2.putText(frame, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 0), 3)
        cv2.imshow('Smart Plant Care System', frame)

        # Save the output image
        cv2.imwrite(os.path.join(IMAGE_FOLDER, 'output.jpg'), frame)
        
        # Send data to the database
        send_db()

        if cv2.waitKey(1) == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

# Start the Flask server in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Start the Flask server
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Start processing video feed
process_video()
