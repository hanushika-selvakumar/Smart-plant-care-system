# Smart-plant-care-system
This repository contains a Raspberry Pi-based Smart Plant Care System that monitors plant health, detects pests/diseases using computer vision, and automates plant care tasks. The system integrates sensor data, machine learning, and IoT capabilities to create a comprehensive plant monitoring solution.

Key Features
1. Plant Health Monitoring
Environmental Sensors:DHT11 for temperature and humidity monitoring
Soil moisture sensor
LDR (Light Dependent Resistor) for light intensity
Gas sensor for air quality
Motion sensor (PIR)

2. Pest/Disease Detection
Uses EfficientNet deep learning model for real-time pest/disease classification
Detects 9 common plant pests:Aphids, Armyworm, Beetle, Bollworm, Grasshopper, Mites, Mosquito, Sawfly, Stem borer
Visual feedback with annotated camera feed

3. Automation
Relay-controlled watering system
Automated plant treatment activation
Remote control via web interface

4. IoT Integration
Flask web server for image hosting
Data transmission to remote server (iotcloud22.in)
Web-based dashboard for monitoring

Technical Stack
Hardware: Raspberry Pi with various sensors and relays
Machine Learning: TensorFlow/Keras with EfficientNet model
Computer Vision: OpenCV
Web Server: Flask
GPIO Control: RPi.GPIO library

Hardware Requirements
Component	Quantity
Raspberry Pi	1
DHT11 Sensor	1
Soil Moisture Sensor	1
LDR Sensor	1
Gas Sensor (MQ-2)	1
PIR Motion Sensor	1
5V Relays	2
Camera Module	1

Setup Instructions
Install required Python packages:
pip install Adafruit_DHT RPi.GPIO opencv-python tensorflow flask requests

Connect sensors to Raspberry Pi GPIO pins as configured. Place EfficientNet model file (efficientnet.h5) in project directory. Run app1.py to start the system

 Installation
Clone the repository
git clone https://github.com/yourusername/smart-plant-care-system.git
cd smart-plant-care-system

Install dependencies
pip install -r requirements.txt

Hardware Setup
Connect sensors to Raspberry Pi GPIO pins as per: python

# GPIO Configuration (app1.py)
DHT_PIN = 14
soil = 15
ldr = 23
Gas = 24
motion = 25
relay_water = 21
relay_plant = 20
Download the ML model
Place efficientnet.h5 in the project root directory.

Acknowledgments
Adafruit for sensor libraries
TensorFlow for ML framework
Flask for web interface
