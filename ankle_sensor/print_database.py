from pymongo import MongoClient

# MongoDB connection
MONGODB_URI = "mongodb://localhost:27017/football_analytics"
client = MongoClient(MONGODB_URI)
db = client['football_analytics']

# Access collections
raw_data_collection = db['raw_sensor_data']
metrics_collection = db['processed_metrics']

# Retrieve all documents from raw_sensor_data collection
raw_data = raw_data_collection.find()
print("Raw Sensor Data:")
#for document in raw_data:
#   print(document)

# Retrieve all documents from processed_metrics collection
processed_metrics = metrics_collection.find()
print("\nProcessed Metrics:")
for document in processed_metrics:
    print(document)
processed_metrics_count = metrics_collection.count_documents({})
print(f"\nProcessed Metrics Count: {processed_metrics_count}")
