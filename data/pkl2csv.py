import pandas as pd
import os
import pickle as pkl

DIR_PATH = './AIR'
CSV_PATH = '../storage/datasets/air-csv'


def convert(file: str):
    print(f'converting {file}... ')
    abs_path = '/'.join([DIR_PATH, file])
    file_name = file.split('.')[0]
    with open(abs_path, 'rb') as f:
        _data = pkl.load(f)
    data = _data[file_name]
    rul = data['rul']  # do not use. since most situations rul are missing
    dq = data['dq']
    cycles = data['data']
    dict = {
        'dq': [],
    }
    for status in cycles[1]['Status'].value_counts().index.tolist():
        dict[f'{status} mean Current (mA)'] = []
        dict[f'{status} std Current (mA)'] = []
        dict[f'{status} mean Voltage (V)'] = []
        dict[f'{status} std Voltage (V)'] = []
    for cycle, features in cycles.items():
        dict['dq'].append(dq[cycle])
        # print(features['Status'].value_counts().index.tolist())
        for status in features['Status'].value_counts().index.tolist():
            sub_features = features[(features['Status'] == status)]
            dict[f'{status} mean Current (mA)'].append(
                sub_features['Current (mA)'].mean())
            dict[f'{status} std Current (mA)'].append(
                sub_features['Current (mA)'].std())
            dict[f'{status} mean Voltage (V)'].append(
                sub_features['Voltage (V)'].mean())
            dict[f'{status} std Voltage (V)'].append(
                sub_features['Voltage (V)'].std())
        # print(dict)
    df = pd.DataFrame(dict)
    df.to_csv('/'.join([CSV_PATH, f'{file_name}.csv']), index=False)


def main():
    for file in os.listdir(DIR_PATH):
        convert(file)


if __name__ == "__main__":
    main()
