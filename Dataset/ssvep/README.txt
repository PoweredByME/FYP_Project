This manifest of the data in this data set is as follows.

data = {
    "time_stamps" : [] %Every element of this array contains a timestamp which corresponds to the time the sample is taken%
    , "Fs" : [[256.]] %The sampling frequency of the data%
    , "gender" : ['13'] %The target freq of the SSVEP%
    , "trial_time_stamp" : [,,...,] %The time_stamp of the sample upon which a specific trial started%
    , "add_info" : [];
    , "trial" : [[,...,,..,]] %The index of the sample upon which the trial starts and ends%
    , "Y" : [....,] %The target frequency of a trial%
    , "X" : [,....,] % A list of smaples of 4 channel data of EEG.
}