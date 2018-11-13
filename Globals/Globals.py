"""
    This script contains all the globals variables
    which are used in the code.

    Most of the variables are settings upon which the
    code works.
"""

DATA_SOURCE = "offline";            # can be either "offline" or "online".
DATA_SAMPLING_FREQ = 256.0;         # the sampling rate of the recorded EEG.
DATA_MAX_BUFFER_TIME_SEC = 2;     # The time in seconds for which the data is stored in the buffer.

SHOW_DATA_WHEN_FILE_OPENED = False  # print the data file when it is opened. Use this for debugging.
DATA_FRAME_APPENDAGE = 3;           # the number of columns which are extra i.e. other than the EEG data itself.

OFFLINE_DATA_PATH = "Dataset/SRC/";
OFFLINE_DATASET_FILE_TYPE = ".mat";

DEBUG = True;