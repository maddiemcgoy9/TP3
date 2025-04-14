# import necessary libraries

import pandas as pd
import re
import time 
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split

from tensorflow.keras.callbacks import EarlyStopping

start_time = time.time()
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print(tf.__version__)
# Load the CSV file
df = pd.read_csv('ASAP2_train_sourcetexts.csv')


# Function to remove punctuation and count words
def count_words(text):
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Split by whitespace and count words
    words = text.split()
    return len(words)
# Function to remove stop words
def remove_stop_words(text):
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in ENGLISH_STOP_WORDS]
    return ' '.join(filtered_words)


early_stop = EarlyStopping(
    monitor='val_mae',         # Watch validation MAE
    patience=6,                # Stop after 3 stagnant epochs
    min_delta=0.0005,           # Needs to improve by at least this much
    restore_best_weights=True # Roll back to the best-performing epoch
)
# Parameters

epochs = 12
batch = 64
drop = .2

# Apply the function to the 'full_text' column and find the maximum & minimum word count
max_word_count = df['full_text'].apply(count_words).max()
min_word_count = df['full_text'].apply(count_words).min()
print("max words in essay", max_word_count)
print("min words in essay", min_word_count)


# Apply the function to the 'full_text' column and create a new column 'abbridged_text'
df['abbridged_text'] = df['full_text'].apply(remove_stop_words)

max_word_count_abridged = df['abbridged_text'].apply(count_words).max()
min_word_count_abridged = df['abbridged_text'].apply(count_words).min()
print("max words in abridged essay", max_word_count_abridged)
print("min words in abridged essay", min_word_count_abridged)

#Original Text 

print(f"Parameters: epochs:{epochs}, batch size: {batch}, dropout: {drop}")
texts = df["full_text"].astype(str).tolist()
scores = df["score"].values
scaler = MinMaxScaler()
scores = scaler.fit_transform(scores.reshape(-1, 1))

tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

max_length = max_word_count
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding="post", truncating="post")

model = models.Sequential([
    layers.Embedding(input_dim=10000, output_dim=64, input_length=max_length),
    layers.Dropout(drop),
    layers.Bidirectional(layers.LSTM(64)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)  # Single output for regression
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

model.summary()



X_train, X_val, y_train, y_val = train_test_split(padded_sequences, scores, test_size=0.2, random_state=42)

# Train original model
history = model.fit(
    X_train, y_train,
    epochs=epochs,
    validation_data=(X_val, y_val),
    batch_size=batch,
    callbacks=[early_stop],
    verbose=1
)

#loss, mae = model.evaluate(X_val, y_val)
#print("Validation MAE:", mae)

# Predict
#predictions = model.predict(X_val)
predictions = model.predict(padded_sequences)
original_scores = scaler.inverse_transform(predictions)
# Abbridged Texts

abbtexts = df["abbridged_text"].astype(str).tolist()



tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(abbtexts)
abbsequences = tokenizer.texts_to_sequences(abbtexts)

abbmax_length = max_word_count_abridged
abbpadded_sequences = pad_sequences(abbsequences, maxlen=abbmax_length, padding="post", truncating="post")

abbmodel = models.Sequential([
    layers.Embedding(input_dim=10000, output_dim=64, input_length=abbmax_length),
    layers.Dropout(drop), 
    layers.Bidirectional(layers.LSTM(64)),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)  # Single output for regression
])

abbmodel.compile(optimizer='adam', loss='mse', metrics=['mae'])

abbmodel.summary()

abbX_train, abbX_val, abby_train, abby_val = train_test_split(abbpadded_sequences, scores, test_size=0.2, random_state=42)

# Train abridged model
abbhistory = abbmodel.fit(
    abbX_train, abby_train,
    epochs=epochs,
    validation_data=(abbX_val, abby_val),
    batch_size=batch,
    callbacks=[early_stop],
    verbose=1
)

#loss, mae = abbmodel.evaluate(X_val, y_val)
#print("Validation MAE:", mae)

# Predict
#predictions = abbmodel.predict(X_val)
abbpredictions = abbmodel.predict(abbpadded_sequences)
abboriginal_scores = scaler.inverse_transform(abbpredictions)
end_time = time.time()

run_time = end_time-start_time
print(f"Model run duration: {run_time/ 60:.2f} minutes")

import pickle

# Save original model's history
with open('history.pkl', 'wb') as f:
    pickle.dump(history.history, f)

# Save abridged model's history
with open('abbhistory.pkl', 'wb') as f:
    pickle.dump(abbhistory.history, f)
    


import matplotlib.pyplot as plt

def inverse_mae(scaled_mae_list, scaler):
    """Inverse transform MAE values from scaled to original range"""
    # We'll inverse transform dummy 2D arrays since MinMaxScaler works that way
    return [scaler.inverse_transform([[mae]])[0][0] for mae in scaled_mae_list]

# Inverse-transform MAE values for original and abridged models
orig_mae = inverse_mae(history.history['mae'], scaler)
orig_val_mae = inverse_mae(history.history['val_mae'], scaler)

abb_mae = inverse_mae(abbhistory.history['mae'], scaler)
abb_val_mae = inverse_mae(abbhistory.history['val_mae'], scaler)

# Plotting
plt.figure(figsize=(12, 6))

# Original model
plt.plot(orig_mae, label='Original Train MAE', color='blue')
plt.plot(orig_val_mae, label='Original Val MAE', color='blue', linestyle='--')

# Abridged model
plt.plot(abb_mae, label='Abridged Train MAE', color='green')
plt.plot(abb_val_mae, label='Abridged Val MAE', color='green', linestyle='--')

# Force integer x-axis ticks
epochs = len(orig_mae)
plt.xticks(range(epochs))

plt.title('Training and Validation MAE over Epochs (Original Score Scale)')
plt.xlabel('Epoch')
plt.ylabel('Mean Absolute Error (MAE)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


actual_scores = scaler.inverse_transform(scores)
error_original = actual_scores.flatten() - original_scores.flatten()
error_abridged = actual_scores.flatten() - abboriginal_scores.flatten()
plt.figure(figsize=(14, 6))

# Original Model Error Histogram
plt.subplot(1, 2, 1)
plt.hist(error_original, bins=50, color='blue', alpha=0.7, edgecolor='black')
plt.title('Prediction Error Distribution\nOriginal Model')
plt.xlabel('Error (Actual - Predicted)')
plt.ylabel('Frequency')
plt.grid(True)

# Abridged Model Error Histogram
plt.subplot(1, 2, 2)
plt.hist(error_abridged, bins=50, color='green', alpha=0.7, edgecolor='black')
plt.title('Prediction Error Distribution\nAbridged Model')
plt.xlabel('Error (Actual - Predicted)')
plt.ylabel('Frequency')
plt.grid(True)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

# Overlayed Error Histograms
plt.hist(error_original, bins=50, color='blue', alpha=0.5, edgecolor='black', label='Original Model')
plt.hist(error_abridged, bins=50, color='green', alpha=0.5, edgecolor='black', label='Abridged Model')

plt.title('Overlayed Prediction Error Distribution')
plt.xlabel('Error (Actual - Predicted)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()