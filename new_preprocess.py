import os
import numpy as np
from sklearn.model_selection import train_test_split

# Define paths
data_dir = r"C:\Users\anshu\OneDrive\Desktop\Labs-Codes\Project\Term-3\CAP-419_Workshop_on_IOT-Labotary\gesture_data"  # Path to your main data folder
gestures = ["forward", "backward", "left", "right", "stop"]  # Define the gesture labels

# List to hold preprocessed data and labels
data = []
labels = []

# Function to normalize landmarks by wrist position
def normalize_landmarks(landmarks):
    wrist = landmarks[0]  # Wrist is the first landmark
    normalized = [(lm[0] - wrist[0], lm[1] - wrist[1], lm[2] - wrist[2]) for lm in landmarks]
    return np.array(normalized).flatten()  # Flatten the landmarks

# Load and preprocess data
for gesture in gestures:
    gesture_dir = os.path.join(data_dir, gesture)  # Get the folder for each gesture
    label = gestures.index(gesture)  # Assign numeric label for each gesture
    
    for filename in os.listdir(gesture_dir):
        if filename.endswith(".npy"):  # Assuming each sample is saved as a .npy file
            filepath = os.path.join(gesture_dir, filename)  # Path to each sample's .npy file
            landmarks = np.load(filepath)  # Load the sample data (landmarks)
            
            # Normalize landmarks and flatten them into a single vector
            normalized_landmarks = normalize_landmarks(landmarks)
            data.append(normalized_landmarks)  # Add to data list
            labels.append(label)  # Add corresponding label

# Convert lists to NumPy arrays
data = np.array(data)
labels = np.array(labels)

# Split into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(data, labels, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Save preprocessed data (optional)
np.save("X_train.npy", X_train)
np.save("y_train.npy", y_train)
np.save("X_val.npy", X_val)
np.save("y_val.npy", y_val)
np.save("X_test.npy", X_test)
np.save("y_test.npy", y_test)

print("Data preprocessing completed successfully.")
