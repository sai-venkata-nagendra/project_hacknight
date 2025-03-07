import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization, Dropout
from tensorflow.keras.optimizers import Adam

# Load preprocessed data
X_train = np.load("preprocessed/X_train.npy")
y_train = np.load("preprocessed/y_train.npy")

# Expand dimensions for CNN input
X_train = np.expand_dims(X_train, axis=-1)
y_train = np.expand_dims(y_train, axis=-1)

# Define a deeper CNN model for depth estimation
model = Sequential([
    Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(256, 256, 1)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Conv2D(256, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    UpSampling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    UpSampling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(1, (3, 3), activation='sigmoid', padding='same')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# Train the model
model.fit(X_train, y_train, epochs=30, batch_size=8, validation_split=0.1)

# Save the trained model
os.makedirs("output", exist_ok=True)
model.save("output/depth_model.h5")

print("✅ Model trained and saved successfully!")