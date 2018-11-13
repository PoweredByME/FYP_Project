'''
    This script is a trial for the loading of the data from the MAMEM DataSet
    33028 -> 4 -> 07.50 Hz
    33026 -> 2 -> 10.00 Hz
    33027 -> 3 -> 08.57 Hz
    33029 -> 5 -> 06.66 Hz
    33025 -> 1 -> 12.00 Hz

    file.mat = {
        info : ... ,
        eeg : ... (15 x samples) ,
        events : ... (events x 4) ,
    }

    ==> events : [
        second column contains the event codes,
        third column contains the sample number at the start of the event.
    ]

    ==> eeg : [
        1 to 14 -> eeg channels,
        15 -> event channel
    ]

    => eeg-channel -> electrode 
        [
            1 : {'AF3'},
            2 : {'F7'},    
            3 : {'F3'},    
            4 : {'FC5'},    
            5 : {'T7'},    
            6 : {'P7'},    
            7 : {'O1'},    
            8 : {'O2'},    
            9 : {'P8'},
            10 : {'T8'},    
            11 : {'FC6'},    
            12 : {'F4'},   
            13 : {'F8'},   
            14 : {'AF4'},    
            15 : {'Status'}
        ]
        
'''
import glob;
from scipy.io import loadmat;
import numpy as np;

def loadData():
    samplesPerSecond = 128;
    src = "EEG-SSVEP-Experiment3/";
    filePart_1 = "U00";
    filePart_2 = range(1, 12);
    filePart_3 = ["a", "b", "c", "d", "e"];
    filePart_4 = ["i", "ii"];
    fileExtension = ".mat";

    eeg_events = {
        33028 : 07.50, # Hz
        33026 : 10.00, # Hz
        33027 : 08.57, # Hz
        33029 : 06.66, # Hz
        33025 : 12.00, # Hz
        32779 : 1, # trial start
        32780 : 0, # trial end
    };

    files = glob.glob(src + "*" + fileExtension);
    data = [];
    

    for _i0 in filePart_2:
        for _i1 in filePart_3:
            for _i2 in filePart_4:
                if _i0 >= 10:
                    filename = src + "U0" + str(_i0) + _i1 + _i2 + fileExtension;
                else:
                    filename = src + filePart_1 + str(_i0) + _i1 + _i2 + fileExtension;
                _data = loadmat(filename);
                events = _data["events"];
                eeg = _data["eeg"];
                
                current_freq = -1;
                for __i in range(1,events.shape[0] - 1):
                    event0 = eeg_events[events[__i, 1]];
                    sample0 = events[__i, 2]; 
                    event1 = eeg_events[events[__i + 1, 1]];
                    sample1 = events[__i + 1, 2]; 

                    eegChunk = eeg[:, sample0 : sample1];
                    if event0 == 1:
                        # trail start
                        for __c in range(int((sample1 - sample0) / samplesPerSecond)):
                            __eegChunk = eegChunk[:, __c * samplesPerSecond : (__c + 1) * samplesPerSecond];
                            data.append({
                                "X" : __eegChunk,
                                "Y" : current_freq
                            });
                    elif event0 == 0:
                        # trail end
                        for __c in range(int((sample1 - sample0) / samplesPerSecond)):
                            __eegChunk = eegChunk[:, __c * samplesPerSecond : (__c + 1) * samplesPerSecond];
                            data.append({
                                "X" : __eegChunk,
                                "Y" : 0.0
                            });
                    else:
                        # cue
                        current_freq = event0;
                        data.append({
                            "X" : eegChunk,
                            "Y" : 0.0
                        })

    return data;

'''
print("loading data... START");
data = loadData();
print("loading data... DONE");

dataToStore = {
    "data" : data,
    "channelToElectrode" : {
            1 : 'AF3',
            2 : 'F7',    
            3 : 'F3',    
            4 : 'FC5',    
            5 : 'T7',    
            6 : 'P7',    
            7 : 'O1',    
            8 : 'O2',    
            9 : 'P8',
            10 : 'T8',    
            11 : 'FC6',    
            12 : 'F4',   
            13 : 'F8',   
            14 : 'AF4',    
            15 : 'Status'
    }
}

import pickle;

print("saving data... START");
pickle.dump( dataToStore, open( "data.pickle", "wb" ) );
print("saving data... DONE");
'''

import pickle;

print("loading data via pickle... START");
data = pickle.load( open( "data.pickle", "rb" ) );
print("loading data via pickle... DONE");

print(data);
