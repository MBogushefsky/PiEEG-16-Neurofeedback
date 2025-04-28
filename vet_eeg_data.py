import os
import shutil

eeg_subs = os.listdir('./eeg_data')
for eeg_sub in eeg_subs:
    # print(eeg_sub)
    with open(f'./eeg_data/{eeg_sub}/{eeg_sub[:-4]}_events.tsv', 'r') as f:
        # print(f.read())
        contents = f.read()
        if 'photic stimulation' in contents:
            print(eeg_sub)
            shutil.rmtree(f'./eeg_data/{eeg_sub}')
