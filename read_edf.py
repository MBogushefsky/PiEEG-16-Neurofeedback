import json
import os

import mne
import matplotlib.pyplot as plt
from scipy.stats import zscore
import numpy as np

# montage = mne.channels.make_standard_montage('standard_1020')
# montage.plot(show_names=True)
eeg_subs = os.listdir('./eeg_data')
# raw = mne.io.read_raw_edf(f'./eeg_data/{eeg_subs[0]}/{eeg_subs[0]}.edf', preload=True)
# raw.compute_psd().plot()
# plt.show()
# eeg_sub_data = []
# for eeg_sub in eeg_subs:
# #     # print(eeg_sub)
# #     with open(f'./eeg_data/{eeg_sub}/{eeg_sub[:-4]}_events.tsv', 'r') as f:
#     raw = mne.io.read_raw_edf(f'./eeg_data/{eeg_sub}/{eeg_sub}.edf', preload=True)
#     raw_delta = raw.copy().filter(l_freq=0.5, h_freq=4.)
#     raw_theta = raw.copy().filter(l_freq=4., h_freq=8.)
#     raw_alpha = raw.copy().filter(l_freq=8., h_freq=12.)
#     raw_beta = raw.copy().filter(l_freq=12., h_freq=30.)
#     raw_gamma = raw.copy().filter(l_freq=30., h_freq=50.)
#     # raw.info['bads'] = ['Cz']
#     # raw.interpolate_bads()
#     # raw.set_montage('GSN-HydroCel-128', on_missing='warn')
#     # raw.plot_sensors(show_names=True)
#     # plt.show()
#     # data, times = raw[:]
#     # print(times)
#     # channel_names = ['Fp1-REF', 'Fp2-REF']
#     # channel_data = raw.get_data(picks=channel_names).flatten()
#     # print(channel_data)
#     # mean = np.mean(channel_data)
#     # std = np.std(channel_data)
#     # z_scores = (channel_data - mean) / std
#     # print(z_scores)
#     # z_channel = zscore(channel_data)
#     # print(z_channel)
#     channel_names = ['Fp1', 'Fp2', 'F7', 'F3', 'F4', 'F8', 'T7', 'C3', 'C4', 'T8', 'P7', 'P3', 'P4', 'P4', 'P8', 'O1', 'O2']
#     channel_mapping = []
#     for ch_name in channel_names:
#         for ch in raw.info['chs']:
#             label = ch['ch_name']
#             if label.startswith(ch_name):
#                 channel_mapping.append(label)
#     for ch in channel_mapping:
#         print(ch)
#         ch_data_delta = raw_delta.get_data(picks=ch).flatten()
#         ch_data_theta = raw_theta.get_data(picks=ch).flatten()
#         ch_data_alpha = raw_alpha.get_data(picks=ch).flatten()
#         ch_data_beta = raw_beta.get_data(picks=ch).flatten()
#         ch_data_gamma = raw_gamma.get_data(picks=ch).flatten()
#         eeg_sub_data.append({
#             'delta': np.average(ch_data_delta),
#             'theta': np.average(ch_data_theta),
#             'alpha': np.average(ch_data_alpha),
#             'beta': np.average(ch_data_beta),
#             'gamma': np.average(ch_data_gamma)
#         })
#         print(np.average(ch_data_delta))
# with open('./eeg_data.json', 'w+') as f:
#     f.write(json.dumps(eeg_sub_data))

# with open('./eeg_data.json', 'r') as f:
#     eeg_data = json.loads(f.read())
#     alphas = []
#     for data in eeg_data:
#         alphas.append(data['alpha'])
#     eeg_data_alpha_avg = np.average(alphas)
#     print(eeg_data_alpha_avg)