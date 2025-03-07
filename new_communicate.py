import tensorflow as tf
import numpy as np
import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
import time

# Load the pre-trained gesture recognition model
model = tf.keras.models.load_model('hand_gesture_model_v3.h5')
print("Model loaded successfully")

# MQTT Broker details
mqtt_server = "192.168.143.176"  # Replace with your MQTT broker IP
mqtt_port = 1883
mqtt_topic = "iot/car"  # Topic where gestures will be published

# Gesture labels for classification
gesture_labels = {0: "Forward", 1: "Backward", 2: "Left", 3: "Right", 4: "Stop"}

# Initialize MediaPipe for hand gesture recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Set up MQTT client for communication with ESP
client = mqtt.Client()
client.connect(mqtt_server, mqtt_port, 60)
client.loop_start()

# Function to publish gesture predictions to MQTT
def publish_gesture(gesture):
    client.publish(mqtt_topic, gesture)
    print(f"Published gesture: {gesture}")

# Start webcam feed
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Variable to store the last published gesture
last_gesture = None

try:
    while True:
        # Capture frame-by-frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Convert frame to RGB for MediaPipe processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to extract hand landmarks
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extract and normalize landmarks relative to the wrist (landmark 0)
                wrist = hand_landmarks.landmark[0]
                normalized_landmarks = [(lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z) for lm in hand_landmarks.landmark]
                
                # Flatten landmarks and reshape for model input
                input_data = np.array(normalized_landmarks).flatten()
                
                # Reshape the input to match the model's expected input shape (1, 1, 63)
                input_data = np.expand_dims(input_data, axis=0)  # shape (1, 63)
                input_data = np.expand_dims(input_data, axis=1)  # shape (1, 1, 63)

                # Perform gesture prediction using the trained model
                prediction = model.predict(input_data)
                gesture_index = np.argmax(prediction)  # Get the index of the highest probability
                gesture = gesture_labels[gesture_index]  # Map the index to the gesture label
                
                # Display the predicted gesture on the frame
                cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                # Publish the gesture to MQTT only if it has changed
                if gesture != last_gesture:
                    publish_gesture(gesture)
                    last_gesture = gesture
        
        # Display the frame with the predicted gesture
        cv2.imshow('Live Feed - Gesture Recognition', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Small delay to control frame rate
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    # Release video capture and close MQTT connection
    cap.release()
    client.loop_stop()
    client.disconnect()
    cv2.destroyAllWindows()
    hands.close()
