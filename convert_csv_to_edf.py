import pandas as pd
import mne
import numpy as np
import os

# Load CSV (assumes columns: time, delta, theta, alpha, beta, gamma)
recording = f"./recordings/{sorted(os.listdir('./recordings'))[-1]}"
print(recording)
df = pd.read_csv(recording)
data = df.drop(columns=['time']).values.T * 1e-6  # Convert to volts (adjust scaling)
ch_names = list(df.columns[1:])  # Channel names
sfreq = 1 / np.mean(np.diff(df['time']))  # Calculate sampling rate

# Create MNE Raw object
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')
raw = mne.io.RawArray(data, info)

# Export to EDF
raw.export('band_powers.edf', fmt='edf', overwrite=True)
