import cv2
import mediapipe as mp
import os
import numpy as np

# Directory to save data
DATA_DIR = "./gesture_data"
GESTURES = {"f": "forward", "b": "backward", "l": "left", "r": "right", "s": "stop"}

# Create directories for each gesture
for gesture in GESTURES.values():
    os.makedirs(os.path.join(DATA_DIR, gesture), exist_ok=True)

# Initialize MediaPipe Hands and OpenCV
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

# Variable to track current gesture and frame count
current_gesture = None
count = 0

def capture_data(gesture, frame, hand_landmarks):
    global count
    landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

    # Save the landmarks to a file
    file_path = os.path.join(DATA_DIR, gesture, f"{gesture}_{count}.npy")
    np.save(file_path, landmarks)
    print(f"Saved {file_path}")
    count += 1

    # Display the gesture on the video feed
    cv2.putText(frame, f"Gesture: {gesture}, Count: {count}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image")
            break

        # Convert frame to RGB and process hand landmarks
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Check for key press to update the current gesture
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Exiting program.")
            break
        elif key in [ord(k) for k in GESTURES.keys()]:
            current_gesture = GESTURES[chr(key)]
            count = 0  # Reset count for new gesture
            print(f"Recording gesture: {current_gesture}")

        # If hand landmarks are detected, record data for the selected gesture
        if results.multi_hand_landmarks and current_gesture:
            hand_landmarks = results.multi_hand_landmarks[0]
            capture_data(current_gesture, frame, hand_landmarks)

        # Display frame with current gesture info
        if current_gesture:
            cv2.putText(frame, f"Recording: {current_gesture}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Show the frame
        cv2.imshow("Gesture Capture", frame)

except KeyboardInterrupt:
    print("Data collection interrupted.")

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
