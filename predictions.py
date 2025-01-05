import pandas as pd
import json
from sklearn.linear_model import LinearRegression
import numpy as np
from prometheus_client import start_http_server, Gauge
import time

# Load the JSON file
with open('cpu_usage.json') as f:
    data = json.load(f)

# Extract timestamps and CPU usage values
timestamps = [point[0] for point in data['data']['result'][0]['values']]
cpu_usage = [float(point[1]) for point in data['data']['result'][0]['values']]

# Create a DataFrame
df = pd.DataFrame({'timestamp': timestamps, 'cpu_usage': cpu_usage})

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Extract time-based features
df['hour'] = df['timestamp'].dt.hour
df['minute'] = df['timestamp'].dt.minute
df['second'] = df['timestamp'].dt.second
df['day_of_week'] = df['timestamp'].dt.dayofweek  # Monday=0, Sunday=6

# Define features (X) and target (y)
X = df[['hour', 'minute', 'second', 'day_of_week']]
y = df['cpu_usage']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Define a Prometheus Gauge metric
predicted_cpu_usage = Gauge('predicted_cpu_usage', 'Predicted CPU usage')

# Start Prometheus metrics server on port 8000
start_http_server(8000)

# Function to predict and update the gauge
def predict_and_update():
    # Predict for a specific timestamp
    future_timestamp = pd.to_datetime('2025-01-05 17:00:00')
    future_hour = future_timestamp.hour
    future_minute = future_timestamp.minute
    future_second = future_timestamp.second
    future_day_of_week = future_timestamp.dayofweek

    # Create a feature vector for prediction
    future_features = np.array([[future_hour, future_minute, future_second, future_day_of_week]])

    # Predict CPU usage
    predicted_value = model.predict(future_features)[0]

    # Set the predicted value as the metric
    predicted_cpu_usage.set(predicted_value)

    # Print the predicted value (optional)
    print("Predicted CPU Usage:", predicted_value)

# Run the prediction and update in a loop
while True:
    predict_and_update()
    time.sleep(60)  # Update every 60 seconds
