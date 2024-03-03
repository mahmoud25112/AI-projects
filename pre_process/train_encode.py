import numpy as np
import pandas as pd
import cv2
from keras import layers, Input, Model
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from autoEncoder import autoencoder
import tensorflow as tf
from keras.models import load_model

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(f"{len(gpus)} Physical GPUs, {len(logical_gpus)} Logical GPU")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

def resize_images(images, size=(128, 128)):
    resized = np.array([cv2.resize(img, size, interpolation=cv2.INTER_AREA) for img in images])
    return resized

# Load preprocessed and normalized data
preprocessed_objects = np.load('preprocessed_objectsHot.npy')

# Resize the images to 128x128
preprocessed_objects = resize_images(preprocessed_objects)

# Modify the optimizer and recompile the model
# Ensure your autoencoder is defined for 128x128 input shape
autoencoder = load_model('my_model.keras')

autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy')

# Implement early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10)

# Train the autoencoder
autoencoder.fit(preprocessed_objects, preprocessed_objects,
                epochs=50,
                batch_size=40,
                shuffle=True,
                validation_split=0.2,
                callbacks=[early_stopping])

# Extract embeddings
encoder = Model(inputs=autoencoder.input, outputs=autoencoder.get_layer('max_pooling2d_2').output)
vector_embeddings = encoder.predict(preprocessed_objects)

# Flatten and convert embeddings to DataFrame
flat_embeddings = vector_embeddings.reshape(vector_embeddings.shape[0], -1)
embeddings_df = pd.DataFrame(flat_embeddings)
embeddings_df.to_csv('vector_embeddingsHot.csv', index=False)

# Save the model
autoencoder.save('my_model.keras')
