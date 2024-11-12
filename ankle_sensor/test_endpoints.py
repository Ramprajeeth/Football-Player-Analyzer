import requests
import json

# Define the base URL for your Flask server
BASE_URL = 'http://localhost:5001'

# Sample sensor data to send in POST request
sensor_data = {
    "accX": 0.3,
    "accY": 2.0,
    "accZ": 1.0,
    "gyroX": 0.06,
    "gyroY": 0.03,
    "gyroZ": 0.01
}

# Function to test the POST request to /api/data
def test_post_data():
    try:
        # Send a POST request
        response = requests.post(f"{BASE_URL}/api/data", json=sensor_data)

        # Print the response
        print("POST /api/data Response:")
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
        print("\n")
    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")

# Function to test the GET request to /api/retrieve
def test_get_data():
    try:
        # Send a GET request
        response = requests.get(f"{BASE_URL}/api/retrieve")

        # Print the response
        print("GET /api/retrieve Response:")
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
        print("\n")
    except requests.exceptions.RequestException as e:
        print(f"Error during GET request: {e}")

if __name__ == '__main__':
    # Test the POST request to send data
    test_post_data()

    # Test the GET request to retrieve the data
    test_get_data()
