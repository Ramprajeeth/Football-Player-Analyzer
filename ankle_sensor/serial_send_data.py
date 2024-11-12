import serial
import requests
import time
import json

# Configure the serial port to match the Arduino's settings
#/dev/tty.HC-05
#/dev/tty.usbmodem101
serial_port = '/dev/tty.HC-05'  # Change this to your correct port, e.g., COM3 on Windows
baud_rate = 9600
arduino = serial.Serial(serial_port, baud_rate)

# URL of your Flask server's POST endpoint
url = "http://127.0.0.1:5001/api/data"

def parse_sensor_data(line):
    """Parse the Arduino sensor data line into a dictionary."""
    try:
        # Attempt to parse the line as JSON
        data = json.loads(line.strip())
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to parse data: {line} - Error: {e}")
        return None

def send_data_to_server(data):
    """Send parsed sensor data to the server."""
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Data sent successfully:", data)
        else:
            print("Failed to send data:", response.status_code, response.text)
    except Exception as e:
        print("Error sending data:", e)

# Read from Serial and send data to server
while True:
    try:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8')
            print("Received from Arduino:", line.strip())
            sensor_data = parse_sensor_data(line)
            if sensor_data:
                send_data_to_server(sensor_data)
            time.sleep(1)  # Wait a bit before reading next data
    except KeyboardInterrupt:
        print("Stopping the program.")
        break
    except Exception as e:
        print("Error:", e)
