import mne
import matplotlib.pyplot as plt
from scipy.stats import zscore
import numpy as np

montage = mne.channels.make_standard_montage('standard_1020')
montage.plot(show_names=True)

raw = mne.io.read_raw_eeglab('./SHA256E-s43276600--b9db835744d332a7b2fa9ab55c8d4585342898251a25b98f98649c0735e9a6a6.set', preload=True)
# raw.info['bads'] = ['Cz']
raw.interpolate_bads()
# raw.set_montage('GSN-HydroCel-128', on_missing='warn')
raw.plot_sensors(show_names=True)
plt.show()
# channel_names = ['E8']
# channel_data = raw.get_data(picks=channel_names).flatten()
# print(channel_data)
# mean = np.mean(channel_data)
# std = np.std(channel_data)
# z_scores = (channel_data - mean) / std
# print(z_scores)
# z_channel = zscore(channel_data)
# print(z_channel)
channel_mapping = []
for ch in raw.info['chs']:
    label = ch['ch_name']
    x, y, z = ch['loc'][:3]
    channel_mapping.append({'label': label, 'x': x, 'y': y, 'z': z})
for ch in channel_mapping:
    print(ch)
# raw.compute_psd().plot()
# plt.show()