# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 13:40:36 2023

@author: ljr1e21
"""

import numpy as np
import fnmatch as fnm
import pandas as pd


def hh(timestamp):
    return int(timestamp.split()[3][0:2])

def mm(timestamp):
    return int(timestamp.split()[3][3:5])

def ss(timestamp):
    return int(timestamp.split()[3][6:8])

def time(timestamp,unit='s'):
    # takes a timestamp in the form Fri Aug 26 16:45:04 2022 and converts to seconds unit='s', minutes unit='m', or hours unit='h'
    if unit=='s':
        return int((hh(timestamp)*60 + mm(timestamp))*60 + ss(timestamp))
    elif unit=='m':
        return float( hh(timestamp)*60 + mm(timestamp) + ss(timestamp)/60 )
    elif unit=='h':
        return float( hh(timestamp) + (mm(timestamp) + ss(timestamp)/60)/60 )
    else:
        return 1


def timestamp_to_time(timestamp):
    # takes a list of timestamps in the form of Fri Aug 26 16:45:04 2022 and converts to seconds from the nearist past hour
    t0 = time(timestamp[0])
    s_from_hour = ss(timestamp[0]) + mm(timestamp[0])*60
    frate = frame_rate(timestamp)
    t = []
    t_from_h = []
    tn = time(timestamp[-1],unit='s') - t0
    for i, tstamp in enumerate(timestamp):
        tx = round(i/frate,3)
        t.append(tx)
        t_from_h.append(tx+s_from_hour)
    
    if round(t[-1]) == tn:
        print('Successfully re-evaluated frame rates!')
        return t, t_from_h
    else:
        print('Frame rate calculation failed, please investigate!')
        return 1
    
def frame_rate(timestamp):
    # Calculates frame rate based on the total time in seconds and the total number of frames
    return len(timestamp)/(time(timestamp[-1],unit='s') - time(timestamp[0],unit='s'))
    

def PressureExport_to_DF(file,numSensors=4):
    """
    Takes .txt file export from Tactilus of format:

    FRAME      1(mmHg)
    Fri Aug 26 16:45:04 2022
       23     0     0     0
       28     0     0     0
       10     0     0     0
       12     0     0     0
        6     0     0     0
       34     0     0     0
        0     0     0     0
        0     0     0     0

    to a pandas dataframe of the format:

    DATA = [[1,tstring,t1,t2,23,28,10,12,6,34],
            [2,tstring,t1,t2,23,28,10,12,6,34],
            [...],...]

    if a frame rate is specified then column one of the output will be in seconds rather than in frames
    """
    cols = ['FRAME','Timestamp','Time From Hour [s]','Time From Start [s]']
    
    with open(file, 'r') as file:# Open file in read mode
        file_list = file.readlines() # Create a list with each line of the data as an item in the list

    # Find all the lines with FRAME at the beginning
    Instance = fnm.filter( file_list, 'FRAME*' )

    # From the last item in Instance find the value of the last frame and store it in frames
    frames = int( Instance[-1].split()[1][:-6] )
    
    ind = range(frames)
    
    for i in range(numSensors):
        n = i + 1
        string = 'Sensor ' + str(n)
        cols.append(string)

    # Create an empty dataframe (may need to specify double not float)
    DATA = np.zeros((frames,9), dtype=np.double )
    df = pd.DataFrame(data=None,columns=cols,index=ind)
    Timestamp = []
    
    per = 0
    
    count = 0
    
    t = file_list[1].split(' ')[3]

    # Populate the np array with the data from the file_list
    for i in range(frames): # Replace 5 with frames
        percent = round(i*100/frames,1)
        if percent != per:
            #print(f"{percent} %")
            per = percent
        DATA[i,0] = float( Instance[i].split()[1][:-6] ) # Frame number
        Timestamp.append(file_list[i*11+1].strip())
        time = file_list[i*11+1].split()[3]
        if time == t:
            count += 1
        else:
            count = 0
            t = time
        for j in range(numSensors):
            DATA[i,j+1] = float( file_list[i*11+2+j].split()[0] ) # Each of the six data channels

    df['FRAME'] = DATA[:,0]
    df['Timestamp'] = Timestamp
    [ t, t_h ] = timestamp_to_time(Timestamp)
    df['Time From Hour [s]'] = t_h
    df['Time From Start [s]'] = t
    for j in range(numSensors):
        sname = 'Sensor ' + str(j+1)
        df[sname] = DATA[:,j+1]
    return df

if __name__ == '__main__':

    input_filename='Tactilus_Pressure.txt' # Change the contents of the '' to the file name of the txt file or change the name of the txt file to Tactilus_Pressure.txt
    output_filename='Tactilus_Pressure.csv' # Change the contents of the '' to the desired output file name or rename it after

    df = PressureExport_to_DF(file=input_filename,numSensors=6)
    df.to_csv(output_filename,index=None)