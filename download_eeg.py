import pandas as pd
import webbrowser

data = pd.read_csv('./data-2025-04-27T17_42_44.194Z.csv')
print(data.head())
pscid = data['PSCID']
print(pscid)
for id in pscid:
    webbrowser.open(f'https://chbmp-open.loris.ca/mri/jiv/get_file.php?file=bids_imports/Dataset_containing_Cuban_Brain_Mapping_database_BIDSVersion_1.2.1/sub-{id}/ses-V01/eeg/sub-{id}_ses-V01_task-protmap_eeg.tgz')