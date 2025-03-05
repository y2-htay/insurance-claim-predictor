import keras
from keras import layers


def base_model(X_train_tf):
    model = keras.Sequential([
        layers.Dense(128, activation='relu', input_shape=(
            X_train_tf.shape[1],)),  # Input layer
        layers.Dense(64, activation='relu'),  # Hidden layer
        layers.Dense(32, activation='relu'),  # Hidden layer
        layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model
