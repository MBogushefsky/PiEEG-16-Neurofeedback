import pandas as pd
import numpy as np
import os

recording = f"./recordings/{sorted(os.listdir('./recordings'))[-1]}"
print(recording)
df = pd.read_csv(recording)
print(np.average(df['avg_asymmetry']))
print(np.average(df['Fp1_Fp2_asymmetry']))
print(np.average(df['F3_F4_asymmetry']))
print(np.average(df['F7_F8_asymmetry']))
print(np.average(df['C3_C4_asymmetry']))
print(np.average(df['P3_P4_asymmetry']))
print(np.average(df['T3_T4_asymmetry']))
print(np.average(df['T5_T6_asymmetry']))
print(np.average(df['O1_O2_asymmetry']))