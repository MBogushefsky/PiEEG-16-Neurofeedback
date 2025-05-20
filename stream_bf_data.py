from datetime import datetime
import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
import pandas as pd
import os


def main():
    BoardShim.enable_dev_board_logger()
    board_id = BoardIds.SYNTHETIC_BOARD
    params = BrainFlowInputParams()
    params.master_board = board_id
    board_descr = BoardShim.get_board_descr(board_id)
    sampling_rate = int(board_descr['sampling_rate'])
    board = BoardShim(board_id, params)
    eeg_channel_labels = [
        'Fp1', 'Fp2', 'F7', 'F3', 'F4', 'F8', 'T3', 'C3',
        'C4', 'T4', 'T5', 'P3', 'P4', 'T6', 'O1', 'O2'
    ]
    board_descr['eeg_channels'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    board_descr['eeg_names'] = eeg_channel_labels
    board_descr['num_rows'] = 16
    print(board_descr)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    
    eeg_channels = board_descr['eeg_channels']
    date_time_start = datetime.now()
    csv_file_path = f'./recordings/{date_time_start.strftime("%Y_%m_%d__%H_%M_%S")}.csv'
    while True:
        data = board.get_current_board_data(256)
        data_dict = dict()
        data_dict['datetime'] = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        # DataFilter.set_eeg_channels(
        #     BoardIds.PIEEG_BOARD.value,
        #     eeg_channel_labels
        # )
        for idx, eeg_channel_label in enumerate(eeg_channel_labels):
            eeg_channel = eeg_channels[idx]
            # optional detrend
            DataFilter.detrend(data[eeg_channel], DetrendOperations.LINEAR.value)
            psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                        WindowOperations.BLACKMAN_HARRIS.value)

            band_power_delta = DataFilter.get_band_power(psd, 0.5, 4.0)
            band_power_theta = DataFilter.get_band_power(psd, 4.0, 8.0)
            band_power_alpha = DataFilter.get_band_power(psd, 8.0, 12.0)
            band_power_beta = DataFilter.get_band_power(psd, 12.0, 30.0)
            band_power_gamma = DataFilter.get_band_power(psd, 30.0, 100.0)
            data_dict[f'{eeg_channel_label}_delta'] = band_power_delta
            data_dict[f'{eeg_channel_label}_theta'] = band_power_theta
            data_dict[f'{eeg_channel_label}_alpha'] = band_power_alpha
            data_dict[f'{eeg_channel_label}_beta'] = band_power_beta
            data_dict[f'{eeg_channel_label}_gamma'] = band_power_gamma
            
            # print("alpha/beta:%f", band_power_alpha / band_power_beta)
        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, True)
        for band in bands:
            mindfulness_params = BrainFlowModelParams(BrainFlowMetrics.MINDFULNESS.value,
                                              BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
            mindfulness = MLModel(mindfulness_params)
            mindfulness.prepare()
            data_dict[f'mindful'] = mindfulness.predict(band)[0]
            mindfulness.release()

            restfulness_params = BrainFlowModelParams(BrainFlowMetrics.RESTFULNESS.value,
                                                    BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
            restfulness = MLModel(restfulness_params)
            restfulness.prepare()
            data_dict[f'restful'] = restfulness.predict(band)[0]
            restfulness.release()
        df = pd.DataFrame([data_dict])
        df.to_csv(csv_file_path, mode='a', index=False, header=not os.path.exists(csv_file_path))
    # board.stop_stream()
    # board.release_session()

if __name__ == "__main__":
    main()