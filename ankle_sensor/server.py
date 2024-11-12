from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime
from pymongo import MongoClient
import logging
import os
from bson import ObjectId  # Import ObjectId to handle MongoDB object serialization

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection class
class PlayerDataProcessor:
    def __init__(self):
        '''Connect to MongoDB'''
        MONGODB_URI = "mongodb://localhost:27017/football_analytics"  # Local MongoDB URI
        
        # Connect to MongoDB client
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['football_analytics']
        
        # Collections to store raw data and processed metrics
        self.raw_data = self.db['raw_sensor_data']
        self.metrics = self.db['processed_metrics']
        
        logger.info("Connected to local MongoDB successfully")

    def save_data(self, raw_data, processed_metrics):
        """Save both raw data and processed metrics to MongoDB"""
        try:
            timestamp = datetime.now()

            # Save raw sensor data
            raw_document = {
                'timestamp': timestamp,
                'acc_x': raw_data['accX'],
                'acc_y': raw_data['accY'],
                'acc_z': raw_data['accZ'],
                'gyro_x': raw_data.get('gyroX', 0),
                'gyro_y': raw_data.get('gyroY', 0),
                'gyro_z': raw_data.get('gyroZ', 0)
            }
            self.raw_data.insert_one(raw_document)

            # Save processed metrics
            metrics_document = {
                'timestamp': timestamp,
                **processed_metrics
            }
            self.metrics.insert_one(metrics_document)

            logger.info("Data saved successfully to MongoDB")
        except Exception as e:
            logger.error(f"Error saving data to MongoDB: {e}")
            raise

    def process_raw_data(self, raw_data):
        """Process incoming raw sensor data and calculate metrics"""
        try:
            # Extract accelerometer data
            acc_x = raw_data['accX']
            acc_y = raw_data['accY']
            acc_z = raw_data['accZ']
            
            # Extract gyroscope data (if available)
            gyro_x = raw_data.get('gyroX', 0)
            gyro_y = raw_data.get('gyroY', 0)
            gyro_z = raw_data.get('gyroZ', 0)
            
            # 1. Overall acceleration magnitude
            acc_magnitude = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
            
            # 2. Estimate speed (rough estimation)
            speed = float(acc_magnitude * 0.1)
            
            # 3. Kick detection and power estimation
            kick_detected = acc_z > 2.0
            kick_power = float(acc_z * 10) if kick_detected else 0.0
            
            # 4. Step detection (based on acc magnitude threshold)
            step_detected = acc_magnitude > 1.2
            
            # Convert NumPy bool to Python bool
            step_detected = bool(step_detected)
            kick_detected = bool(kick_detected)
            
            # 5. Movement pattern recognition (simple classifier)
            if acc_magnitude < 0.5:
                movement_pattern = 'Standing'
            elif 0.5 <= acc_magnitude < 1.5:
                movement_pattern = 'Walking'
            else:
                movement_pattern = 'Running'
            
            # 6. Jump detection and jump height estimation
            jump_height = 0.0
            if acc_y > 2.0:
                jump_height = float((acc_y * 0.1)**2 / (2 * 9.81))
            
            # 7. Impact force measurement
            impact_force = float(acc_magnitude) if acc_magnitude > 3.0 else 0.0
            
            # 8. Foot orientation tracking (short duration using gyro data)
            rotation_rate = float(np.sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2))
            
            return {
                'speed': speed,
                'kick_detected': kick_detected,
                'kick_power': kick_power,
                'step_detected': step_detected,
                'movement_pattern': movement_pattern,
                'jump_height': jump_height,
                'impact_force': impact_force,
                'rotation_rate': rotation_rate
            }
        except Exception as e:
            logger.error(f"Error processing raw data: {e}")
            raise

    def get_latest_data(self):
        """Retrieve the latest raw data from MongoDB"""
        try:
            latest_data = self.raw_data.find().sort('timestamp', -1).limit(1)
            return list(latest_data)
        except Exception as e:
            logger.error(f"Error retrieving data from MongoDB: {e}")
            return []

# Helper function to convert ObjectId to string for JSON serialization
def convert_objectid_to_string(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, dict):
                convert_objectid_to_string(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], dict):
                convert_objectid_to_string(data[i])
    return data

# Initialize the processor
processor = PlayerDataProcessor()

# API Routes
@app.route('/api/data', methods=['POST'])
def receive_data():
    """Endpoint to receive and store raw sensor data"""
    try:
        raw_data = request.json
        logger.info(f"Received data: {raw_data}")
        
        # Process raw data to calculate metrics
        processed_metrics = processor.process_raw_data(raw_data)
        
        # Store both raw data and processed metrics
        processor.save_data(raw_data, processed_metrics)
        
        # Send response back with success
        return jsonify({'status': 'success', 'received_data': raw_data, 'processed_metrics': processed_metrics}), 200
    except Exception as e:
        logger.error(f"Error in receive_data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/retrieve', methods=['GET'])
def retrieve_data():
    """Endpoint to retrieve the most recent stored data"""
    try:
        latest_data = processor.get_latest_data()
        if latest_data:
            latest_data = convert_objectid_to_string(latest_data)
            return jsonify({'status': 'success', 'latest_data': latest_data[0]}), 200
        else:
            return jsonify({'status': 'error', 'message': 'No data found'}), 404
    except Exception as e:
        logger.error(f"Error in retrieve_data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
