from datetime import datetime
import spidev
import time
#from RPi import GPIO
#GPIO.setwarnings(False) 
#GPIO.setmode(GPIO.BOARD)
#from gpiozero import LED,Button
from matplotlib import pyplot as plt
#sw1 = Button(26,pull_up=True)#  37
#from gpiozero import LED,Button
#from scipy.ndimage import gaussian_filter1d
#from scipy import signal
import gpiod
#from time import sleep
import pandas as pd
import numpy as np
from scipy.signal import welch
from scipy.integrate import simps
from pylsl import StreamInfo, StreamOutlet
import os
import pyttsx3
from musicpy import note, play
import matplotlib.pyplot as plt

eeg_channel_labels = [
    'F7', 'Fp1', 'Fp2', 'F8', 'F3', 'F4', 'T3', 'C3',
    'C4', 'T4', 'P3', 'P4', 'T5', 'O1', 'O2', 'T6'
]

voice_eng = pyttsx3.init()

stream_info = StreamInfo(
    name='RaspberryPiEEG16Stream',
    type='EEG',
    channel_count=16,
    nominal_srate=250,
    channel_format='float32',
    source_id='raspberry_pi_5'
)
stream_info.desc().append_child_value("manufacturer", "RaspberryPiEEG")
channels = stream_info.desc().append_child("channels")
for label in eeg_channel_labels:
    ch = channels.append_child("channel")
    ch.append_child_value("label", label)
    ch.append_child_value("unit", "microvolts")

outlet = StreamOutlet(stream_info)

button_pin_1 =  26 #13
button_pin_2 =  13
chip = gpiod.Chip("gpiochip4")
# chip = gpiod.chip("0")
cs_line = chip.get_line(19)  # GPIO19
cs_line.request(consumer="SPI_CS", type=gpiod.LINE_REQ_DIR_OUT)
cs_line.set_value(1)  # Set CS high initially

button_line_1 = chip.get_line(button_pin_1)
button_line_1.request(consumer = "Button", type = gpiod.LINE_REQ_DIR_IN)


button_line_2 = chip.get_line(button_pin_2)
button_line_2.request(consumer = "Button", type = gpiod.LINE_REQ_DIR_IN)

spi = spidev.SpiDev()

spi.open(0,0)
spi.max_speed_hz  = 4000000#600000
spi.lsbfirst=False
spi.mode=0b01
spi.bits_per_word = 8

spi_2 = spidev.SpiDev()

spi_2.open(0,1)
spi_2.max_speed_hz=4000000#600000
spi_2.lsbfirst=False
spi_2.mode=0b01
spi_2.bits_per_word = 8

who_i_am=0x00
config1=0x01
config2=0X02
config3=0X03

reset=0x06
stop=0x0A
start=0x08
sdatac=0x11
rdatac=0x10
wakeup=0x02
rdata = 0x12

ch1set=0x05
ch2set=0x06
ch3set=0x07
ch4set=0x08
ch5set=0x09
ch6set=0x0A
ch7set=0x0B
ch8set=0x0C

data_test= 0x7FFFFF
data_check=0xFFFFFF

def read_byte(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 read_reg=spi.xfer(data)
 print ("data", read_reg)
 
def send_command(command):
 send_data = [command]
 com_reg=spi.xfer(send_data)
 
def write_byte(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)
 spi.xfer(data)

def read_byte_2(register):
 write=0x20
 register_write=write|register
 data = [register_write,0x00,register]
 cs_line.set_value(0)
 read_reg=spi.xfer(data)
 cs_line.set_value(1)
 print ("data", read_reg)
 
def send_command_2(command):
 send_data = [command]
 cs_line.set_value(0)
 spi_2.xfer(send_data)
 cs_line.set_value(1)
 
def write_byte_2(register,data):
 write=0x40
 register_write=write|register
 data = [register_write,0x00,data]
 print (data)

 cs_line.set_value(0)
 spi_2.xfer(data)
 cs_line.set_value(1)
 

send_command (wakeup)
send_command (stop)
send_command (reset)
send_command (sdatac)

write_byte (0x14, 0x80) #GPIO 80
write_byte (config1, 0x96)
write_byte (config2, 0xD4)
write_byte (config3, 0xFF)
write_byte (0x04, 0x00)
write_byte (0x0D, 0x00)
write_byte (0x0E, 0x00)
write_byte (0x0F, 0x00)
write_byte (0x10, 0x00)
write_byte (0x11, 0x00)
write_byte (0x15, 0x20)
#
write_byte (0x17, 0x00)
write_byte (ch1set, 0x00)
write_byte (ch2set, 0x00)
write_byte (ch3set, 0x00)
write_byte (ch4set, 0x00)
write_byte (ch5set, 0x00)
write_byte (ch6set, 0x00)
write_byte (ch7set, 0x00)
write_byte (ch8set, 0x00)

send_command (rdatac)
send_command (start)


send_command_2 (wakeup)
send_command_2 (stop)
send_command_2 (reset)
send_command_2 (sdatac)

write_byte_2 (0x14, 0x80) #GPIO 80
write_byte_2 (config1, 0x96)
write_byte_2 (config2, 0xD4)
write_byte_2 (config3, 0xFF)
write_byte_2 (0x04, 0x00)
write_byte_2 (0x0D, 0x00)
write_byte_2 (0x0E, 0x00)
write_byte_2 (0x0F, 0x00)
write_byte_2 (0x10, 0x00)
write_byte_2 (0x11, 0x00)
write_byte_2 (0x15, 0x20)
#
write_byte_2 (0x17, 0x00)
write_byte_2 (ch1set, 0x00)
write_byte_2 (ch2set, 0x00)
write_byte_2 (ch3set, 0x00)
write_byte_2 (ch4set, 0x00)
write_byte_2 (ch5set, 0x00)
write_byte_2 (ch6set, 0x00)
write_byte_2 (ch7set, 0x00)
write_byte_2 (ch8set, 0x00)

send_command_2 (rdatac)
send_command_2 (start)

DRDY=1

result=[0]*27
result_2=[0]*27


data_1ch = []
data_2ch = []
data_3ch = []
data_4ch = []
data_5ch = []
data_6ch = []
data_7ch = []
data_8ch = []

data_9ch = []
data_10ch = []
data_11ch = []
data_12ch = []
data_13ch = []
data_14ch = []
data_15ch = []
data_16ch = []

axis_x=0
y_minus_graph=100
y_plus_graph=100
x_minux_graph=5000
x_plus_graph=250
sample_len = 250

fig, axis = plt.subplots(4, 4, figsize=(5, 5))
plt.subplots_adjust(hspace=1)
ch_name = 0
ch_name_title = [1,5,2,6,3,7,4,8]
axi = [(i, j) for i in range(4) for j in range(2)]
for ax_row, ax_col in axi:
    axis[ax_row, ax_col].set_xlabel('Time')
    axis[ax_row, ax_col].set_ylabel('Amplitude')
    axis[ax_row, ax_col].set_title('Data after pass filter Ch-' + str(ch_name_title[ch_name]))
    ch_name = ch_name + 1    
    
test_DRDY = 5 
test_DRDY_2 = 5
#1.2 Band-pass filter
data_before = []
data_after =  []
just_one_time = 0
data_lenght_for_Filter = 2     # how much we read data for filter, all lenght  [_____] + [_____] + [_____]
read_data_lenght_one_time = 1   # for one time how much read  [_____]
sample_len = 250
sample_lens = 250
fps = 250
highcut = 1
lowcut = 10
data_before_1 = data_before_2 = data_before_3 = data_before_4 = data_before_5 = data_before_6 = data_before_7 = data_before_8 = [0]*250
data_before_9 = data_before_10 = data_before_11 = data_before_12 = data_before_13 = data_before_14 = data_before_15 = data_before_16 = [0]*250

print (data_lenght_for_Filter*read_data_lenght_one_time-read_data_lenght_one_time)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y
def butter_highpass(cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def bandpower(data, sf, band, window_sec=None, relative=False):
    # data: 1D array of EEG signal
    # sf: Sampling frequency (Hz)
    # band: [low, high] frequency range (Hz)
    # window_sec: Window length in seconds for Welch method
    # relative: if True, returns relative power
    band = np.array(band)
    freqs, psd = welch(data, sf, nperseg=window_sec*sf if window_sec else None, scaling='density')
    idx_band = np.logical_and(freqs >= band[0], freqs <= band[1])
    bp = simps(psd[idx_band], freqs[idx_band]) # Absolute power
    if relative:
        bp /= simps(psd, freqs) # Relative power
    return bp

def all_bandpowers(data):
   return {
      'delta': bandpower(data, 250, [0.5, 4], 10, True),
      'theta': bandpower(data, 250, [4, 8], 10, True),
      'alpha': bandpower(data, 250, [8, 13], 10, True),
      'beta': bandpower(data, 250, [13, 30], 10, True),
      'gamma': bandpower(data, 250, [30, 100], 10, True)     
   }

def fill_focus(eeg_data):
    fp1_focus = eeg_data['Fp1_beta'] / (eeg_data['Fp1_alpha'] + eeg_data['Fp1_theta'])
    fp2_focus = eeg_data['Fp2_beta'] / (eeg_data['Fp2_alpha'] + eeg_data['Fp2_theta'])
    f3_focus = eeg_data['F3_beta'] / (eeg_data['F3_alpha'] + eeg_data['F3_theta'])
    f4_focus = eeg_data['F4_beta'] / (eeg_data['F4_alpha'] + eeg_data['F4_theta'])
    f7_focus = eeg_data['F7_beta'] / (eeg_data['F7_alpha'] + eeg_data['F7_theta'])
    f8_focus = eeg_data['F8_beta'] / (eeg_data['F8_alpha'] + eeg_data['F8_theta'])
    c3_focus = eeg_data['C3_beta'] / (eeg_data['C3_alpha'] + eeg_data['C3_theta'])
    c4_focus = eeg_data['C4_beta'] / (eeg_data['C4_alpha'] + eeg_data['C4_theta'])
    eeg_data['focus_value'] = (fp1_focus + fp2_focus + f3_focus + f4_focus + f7_focus + f8_focus + c3_focus + c4_focus) / 8
    if eeg_data['focus_value'] < 0.3:
       eeg_data['focus_level'] = 'Low Focus/Relaxation'
    elif 0.3 <= eeg_data['focus_value'] < 0.5:
       eeg_data['focus_level'] = 'Medium Focus/Alertness'
    elif 0.5 <= eeg_data['focus_value'] < 1.0:
       eeg_data['focus_level'] = 'High Focus/Stress'
    elif 1.0 <= eeg_data['focus_value']:
       eeg_data['focus_level'] = 'Very High Focus/Stress'

def fill_asymmetry(eeg_data):
   fp1_fp2_asym = ((eeg_data['Fp1_alpha'] - eeg_data['Fp2_alpha']) / (eeg_data['Fp1_alpha'] + eeg_data['Fp2_alpha'])) * 100
   f3_f4_asym = ((eeg_data['F3_alpha'] - eeg_data['F4_alpha']) / (eeg_data['F3_alpha'] + eeg_data['F4_alpha'])) * 100
   f7_f8_asym = ((eeg_data['F7_alpha'] - eeg_data['F8_alpha']) / (eeg_data['F7_alpha'] + eeg_data['F8_alpha'])) * 100
   c3_c4_asym = ((eeg_data['C3_alpha'] - eeg_data['C4_alpha']) / (eeg_data['C3_alpha'] + eeg_data['C4_alpha'])) * 100
   p3_p4_asym = ((eeg_data['P3_alpha'] - eeg_data['P4_alpha']) / (eeg_data['P3_alpha'] + eeg_data['P4_alpha'])) * 100
   t3_t4_asym = ((eeg_data['T3_alpha'] - eeg_data['T4_alpha']) / (eeg_data['T3_alpha'] + eeg_data['T4_alpha'])) * 100
   t5_t6_asym = ((eeg_data['T5_alpha'] - eeg_data['T6_alpha']) / (eeg_data['T5_alpha'] + eeg_data['T6_alpha'])) * 100
   o1_o2_asym = ((eeg_data['O1_alpha'] - eeg_data['O2_alpha']) / (eeg_data['O1_alpha'] + eeg_data['O2_alpha'])) * 100
   eeg_data['Fp1_Fp2_asymmetry'] = fp1_fp2_asym
   eeg_data['F3_F4_asymmetry'] = f3_f4_asym
   eeg_data['F7_F8_asymmetry'] = f7_f8_asym
   eeg_data['C3_C4_asymmetry'] = c3_c4_asym
   eeg_data['P3_P4_asymmetry'] = p3_p4_asym
   eeg_data['T3_T4_asymmetry'] = t3_t4_asym
   eeg_data['T5_T6_asymmetry'] = t5_t6_asym
   eeg_data['O1_O2_asymmetry'] = o1_o2_asym
   eeg_data['avg_asymmetry'] = (fp1_fp2_asym + f3_f4_asym + f7_f8_asym + c3_c4_asym + p3_p4_asym + t3_t4_asym + t5_t6_asym + o1_o2_asym) / 8

def fill_avg_delta(eeg_data):
    total = 0
    for eeg_channel_label in eeg_channel_labels:
      total += eeg_data[f'{eeg_channel_label}_delta']
    eeg_data['avg_delta'] = total / len(eeg_channel_labels)

def fill_avg_theta(eeg_data):
    total = 0
    for eeg_channel_label in eeg_channel_labels:
      total += eeg_data[f'{eeg_channel_label}_theta']
    eeg_data['avg_theta'] = total / len(eeg_channel_labels)

def fill_avg_alpha(eeg_data):
    total = 0
    for eeg_channel_label in eeg_channel_labels:
      total += eeg_data[f'{eeg_channel_label}_alpha']
    eeg_data['avg_alpha'] = total / len(eeg_channel_labels)

def fill_avg_beta(eeg_data):
    total = 0
    for eeg_channel_label in eeg_channel_labels:
      total += eeg_data[f'{eeg_channel_label}_beta']
    eeg_data['avg_beta'] = total / len(eeg_channel_labels)

def fill_avg_gamma(eeg_data):
    total = 0
    for eeg_channel_label in eeg_channel_labels:
      total += eeg_data[f'{eeg_channel_label}_gamma']
    eeg_data['avg_gamma'] = total / len(eeg_channel_labels)

def determine_level(band, value):
    if band == 'delta':
        if value < 0.2:
            return 1
        elif 0.2 <= value < 0.3:
            return 2
        elif 0.3 <= value < 0.4:
            return 3
        elif 0.4 <= value:
            return 4
    elif band == 'theta':
        if value < 0.1:
            return 1
        elif 0.1 <= value < 0.15:
            return 2
        elif 0.15 <= value < 0.2:
            return 3
        elif 0.2 <= value:
            return 4
    elif band == 'alpha':
        if value < 0.15:
            return 1
        elif 0.15 <= value < 0.225:
            return 2
        elif 0.225 <= value < 0.3:
            return 3
        elif 0.3 <= value:
            return 4
    elif band == 'beta':
        if value < 0.1:
            return 1
        elif 0.1 <= value < 0.15:
            return 2
        elif 0.15 <= value < 0.2:
            return 3
        elif 0.2 <= value:
            return 4
    elif band == 'gamma':
        if value < 0.01:
            return 1
        elif 0.01 <= value < 0.02:
            return 2
        elif 0.02 <= value < 0.04:
            return 3
        elif 0.05 <= value:
            return 4

def fill_mental_performance(eeg_data):
    fill_avg_delta(eeg_data)
    fill_avg_theta(eeg_data)
    fill_avg_alpha(eeg_data)
    fill_avg_beta(eeg_data)
    fill_avg_gamma(eeg_data)
    'F7', 'Fp1', 'Fp2', 'F8', 'F3', 'F4'
    frontal_theta = (eeg_data['F7_theta'] + eeg_data['Fp1_theta'] + eeg_data['Fp2_theta'] + eeg_data['F8_theta'] + eeg_data['F3_theta'] + eeg_data['F4_theta']) / 6
    eeg_data['frontal_theta'] = frontal_theta
    # eeg_data['frontal_theta_mp_level'] = determine_level('theta', frontal_theta)
    parietal_alpha = (eeg_data['P3_alpha'] + eeg_data['P4_alpha'] + eeg_data['T5_alpha'] + eeg_data['T6_alpha']) / 4
    eeg_data['parietal_alpha'] = parietal_alpha
    # eeg_data['parietal_alpha_mp_level'] = determine_level('alpha', parietal_alpha)
    # eeg_data['beta_mp_level'] = determine_level('beta', eeg_data['avg_beta'])
    # eeg_data['gamma_mp_level'] = determine_level('gamma', eeg_data['avg_gamma'])
    eeg_data['theta_alpha'] = eeg_data['avg_theta'] / eeg_data['avg_alpha']
    eeg_data['beta_alpha_theta'] = eeg_data['avg_beta'] / (eeg_data['avg_alpha'] + eeg_data['avg_theta'])   
    eeg_data['mental_performance'] = (eeg_data['frontal_theta'] + eeg_data['parietal_alpha'] + eeg_data['avg_beta'] + eeg_data['avg_gamma'] + eeg_data['theta_alpha'] + eeg_data['beta_alpha_theta']) / 6
    print(eeg_data['mental_performance'])

date_time_start = datetime.now()
csv_file_path = f'./recordings/{date_time_start.strftime("%Y_%m_%d__%H_%M_%S")}.csv'
eeg_data_set = []
while 1:
    
    
    #print ("1", button_state)
    #print("2", button_state_2)

        #print ("ok3")
        button_state = button_line_1.get_value()
        #print (button_state)
        if button_state == 1:
            test_DRDY = 10
        if test_DRDY == 10 and button_state == 0:
            test_DRDY = 0 

            output=spi.readbytes(27)
            
            cs_line.set_value(0)
            output_2=spi_2.readbytes(27)
            cs_line.set_value(1)

#            print (output[0],output[1],output[2])
            if output_2[0]==192 and output_2[1] == 0 and output_2[2] == 8:
                eeg_data = dict()
                eeg_data['datetime'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                #print ("ok4")
                for a in range (3,25,3):
                    voltage_1=(output[a]<<8)| output[a+1]
                    voltage_1=(voltage_1<<8)| output[a+2]
                    convert_voktage=voltage_1|data_test
                    if convert_voktage==data_check:
                        voltage_1_after_convert=(voltage_1-16777214)
                    else:
                       voltage_1_after_convert=voltage_1
                    channel_num =  (a/3)

                    result[int (channel_num)]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)

                data_1ch.append(result[1])
                data_2ch.append(result[2])
                data_3ch.append(result[3])
                data_4ch.append(result[4])
                data_5ch.append(result[5])
                data_6ch.append(result[6])
                data_7ch.append(result[7])
                data_8ch.append(result[8])

                for a in range (3,25,3):
                    voltage_1=(output_2[a]<<8)| output_2[a+1]
                    voltage_1=(voltage_1<<8)| output_2[a+2]
                    convert_voktage=voltage_1|data_test
                    if convert_voktage==data_check:
                        voltage_1_after_convert=(voltage_1-16777214)
                    else:
                       voltage_1_after_convert=voltage_1
                    channel_num =  (a/3)

                    result[int (channel_num) + 8]=round(1000000*4.5*(voltage_1_after_convert/16777215),2)

                data_9ch.append(result[9])
                data_10ch.append(result[10])
                data_11ch.append(result[11])
                data_12ch.append(result[12])
                data_13ch.append(result[13])
                data_14ch.append(result[14])
                data_15ch.append(result[15])
                data_16ch.append(result[16])

            outlet.push_sample([
                result[1], 
                result[2],
                result[3],
                result[4],
                result[5],
                result[6],
                result[7],
                result[8],
                result[9],
                result[10],
                result[11],
                result[12],
                result[13],
                result[14],
                result[15],
                result[16]
            ])

            # if len(data_9ch_test) == 250:  # set  lenght 250 it is 1 sec, 20000  = 80 sec   
            #     data = [
            #        data_1ch_test,
            #        data_2ch_test,
            #        data_3ch_test,
            #        data_4ch_test,
            #        data_5ch_test,
            #        data_6ch_test,
            #        data_7ch_test,
            #        data_8ch_test,
            #        data_9ch_test,
            #        data_10ch_test,
            #        data_11ch_test,
            #        data_12ch_test,
            #        data_13ch_test,
            #        data_14ch_test,
            #        data_15ch_test,
            #        data_16ch_test
            #     ]

            #     for idx, eeg_channel_label in enumerate(eeg_channel_labels):
            #         band_powers = all_bandpowers(data[idx])
            #         eeg_data[f'{eeg_channel_label}_delta'] = band_powers['delta']
            #         eeg_data[f'{eeg_channel_label}_theta'] = band_powers['theta']
            #         eeg_data[f'{eeg_channel_label}_alpha'] = band_powers['alpha']
            #         eeg_data[f'{eeg_channel_label}_beta'] = band_powers['beta']
            #         eeg_data[f'{eeg_channel_label}_gamma'] = band_powers['gamma']
                
                # fill_focus(eeg_data)
                # fill_asymmetry(eeg_data)
                # fill_mental_performance(eeg_data)

                # mp = eeg_data['mental_performance']
                # if mp > 1.0:
                    # play(note('C', 5))
                # voice_eng.say(eeg_data['focus_level'])
                # voice_eng.runAndWait()

                # eeg_data_set.append(eeg_data)
                # df = pd.DataFrame([eeg_data])
                # df.to_csv(csv_file_path, mode='a', index=False, header=not os.path.exists(csv_file_path))
                
                # data_1ch_test = []
                # data_2ch_test = []
                # data_3ch_test = []
                # data_4ch_test = []
                # data_5ch_test = []
                # data_6ch_test = []
                # data_7ch_test = []
                # data_8ch_test = []
                # data_9ch_test = []
                # data_10ch_test = []
                # data_11ch_test = []
                # data_12ch_test = []
                # data_13ch_test = []
                # data_14ch_test = []
                # data_15ch_test = []
                # data_16ch_test = []
                
                # df = pd.DataFrame(data_dict)
                # df.to_csv("output3.csv", index=True)
                # print (df)
                # print(bandpower(data_1ch_test, 250, [0.5, 4], None, True))



spi.close()
