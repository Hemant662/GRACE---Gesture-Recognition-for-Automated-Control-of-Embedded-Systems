import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Load the preprocessed data
X_train = np.load("X_train.npy")
y_train = np.load("y_train.npy")
X_val = np.load("X_val.npy")
y_val = np.load("y_val.npy")
X_test = np.load("X_test.npy")
y_test = np.load("y_test.npy")

print(f"Training Data Shape: {X_train.shape}")
print(f"Training Labels Shape: {y_train.shape}")
print(f"Validation Data Shape: {X_val.shape}")
print(f"Validation Labels Shape: {y_val.shape}")
print(f"Testing Data Shape: {X_test.shape}")
print(f"Testing Labels Shape: {y_test.shape}")

# Reshape the data to be 3D for LSTM input (samples, timesteps, features)
# Assuming that each sequence is one timestep long (you could adjust this if your data has multiple frames per gesture)
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))  # 1 timestep
X_val = X_val.reshape((X_val.shape[0], 1, X_val.shape[1]))  # 1 timestep
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))  # 1 timestep

# Define the model
model = Sequential()

# LSTM layer for temporal pattern recognition
model.add(LSTM(128, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
model.add(Dropout(0.2))  # Dropout layer for regularization

model.add(LSTM(64, return_sequences=False))
model.add(Dropout(0.2))  # Dropout layer for regularization

# Dense layer to output predictions for each gesture
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))  # Dropout layer for regularization
model.add(Dense(5, activation='softmax'))  # 5 output classes for the gestures

# Compile the model
model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Model Summary
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_val, y_val))

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc:.4f}")

# Save the model
model.save('gesture_gesture_model_v3.h5')
print("Model saved to 'gesture_gesture_model_v3.h5'")