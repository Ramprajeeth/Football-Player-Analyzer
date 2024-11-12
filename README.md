# Football PLayer Analyzer #

A real-time football player performance analysis tool using MPU 6050 sensors, Arduino Uno, Flask, and MongoDB.

## Project Overview ##

The Football Player Analyzer is a tool designed to track and analyze the physical performance of football players in real-time. By leveraging data from an MPU 6050 sensor, this system captures acceleration and rotational metrics to provide insights into players' speed, agility, jump height, and more. The project is designed to be accessible to players at all levels, offering real-time feedback through a web-based dashboard.
 
## Features ##

Real-Time Data Collection: Uses the MPU 6050 sensor to capture live player metrics such as acceleration, jump height, and impact force.
Data Processing and Visualization: A backend Flask server processes data and displays metrics on a web-based interface.
Performance Tracking: Tracks and logs performance data over time, storing it in a MongoDB database for retrieval and analysis.
User-Friendly Interface: Visualizes metrics through an easy-to-navigate dashboard for real-time monitoring.

## System Architecture ##

- Sensor (MPU 6050): Captures motion data, including acceleration and gyroscope information.
- Arduino Uno: Transmits sensor data to the backend using serial communication.
- Backend (Flask Server): Receives sensor data, processes it, and stores it in MongoDB.
- Database (MongoDB): Stores both raw and processed player data.
- Frontend (HTML & Plotly): Displays real-time data visualizations on a web dashboard.






