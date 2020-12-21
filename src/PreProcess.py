# import module
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm

def Read_Process_Save(file):
    CSV_FILE_PATH = './Data/{}.csv'.format(file)
    df = pd.read_csv(CSV_FILE_PATH, delimiter=";", header=1)
    ColumnName = []
    ColumnName.append('Timestamp')
    for i in range (0,5):
        ColumnName.append('Logging:Logging.AxisData[{}].ErrorNumber'.format(i))
        ColumnName.append('Logging:Logging.AxisData[{}].ActualTorque'.format(i))
        ColumnName.append('Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i))
        
        df['Logging:Logging.AxisData[{}].ActualTorque'.format(i)] = \
            df['Logging:Logging.AxisData[{}].ActualTorque'.format(i)].str.replace(',','.')
        df['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i)] = \
            df['Logging:Logging.AxisData[{}].ActualAxisVelocity'.format(i)].str.replace(',','.')
    target_df = df[ColumnName].copy(deep=True)
    
    

    split_index = [] # to save the index that splits the dataframe(save the last index of each pieces)
    split_index.append(0)

    for index in range(0,target_df.shape[0]-1):
        # Save Last Interval
        if index == target_df.shape[0]-2:
            target_df[split_index[-1]:].to_csv('./Data_Process/{}/'.format(file)+'{}.csv'.format(len(split_index)))

        # Traverse Timestamp
        if (datetime.datetime.strptime( target_df['Timestamp'][index+1],'%Y %m %d %H:%M:%S:%f') - datetime.datetime.strptime( target_df['Timestamp'][index],'%Y %m %d %H:%M:%S:%f')).seconds < 5:
            continue 

        # Save Intervals to CSV
        target_df[split_index[-1]:index+1] \
            .loc[target_df['Logging:Logging.AxisData[0].ErrorNumber']==0] \
            .loc[target_df['Logging:Logging.AxisData[1].ErrorNumber']==0] \
            .loc[target_df['Logging:Logging.AxisData[2].ErrorNumber']==0] \
            .loc[target_df['Logging:Logging.AxisData[3].ErrorNumber']==0] \
            .loc[target_df['Logging:Logging.AxisData[4].ErrorNumber']==0] \
                .to_csv('./Data_Process/{}/'.format(file)+'{}.csv'.format(len(split_index)),sep=',') # save
        split_index.append(index+1)
    return target_df


csv_list = ['Datalog_2019_12_10_14_20_33','Datalog_2019_12_10_14_59_07','Datalog_2019_12_10_15_07_25','Datalog_2019_12_10_15_12_00',
           'Datalog_2019_12_10_15_17_33','Datalog_2019_12_10_15_22_40','Datalog_2019_12_10_15_45_19','Datalog_2019_12_10_16_07_01',
           'Datalog_2019_12_10_16_39_44']

if os.path.exists('./Data_Process'):
    os.remove('./Data_Process')
os.mkdir('./Data_Process')
print("Start Pre-Process!!")
for file in tqdm(csv_list):
    os.mkdir('./Data_Process/{}'.format(file))
    Read_Process_Save(file)