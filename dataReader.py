'''
    This is a peer/worker which deal with the reading of the
    data from the an online or offline source.

    The DataReader class is a child of Worker class. It has is own
    thread.
'''

from worker import Worker;
from message import Messenger, Message;
import time;

class DataReader(Worker):
    '''
        This class is the child of the Worker class.
        This class runs as a daemon in the background. 
        When ever the data buffer of the sampler is filled.
        It simply send the data to the server. 

        It does not need the query of the server to send the data back.
    '''
    def __init__(self, threadSocket, waitForInput = False, name = "DataReader"):
        super(DataReader, self).__init__(threadSocket, waitForInput, name);
        self._messenger = DataReaderMessenger(self._threadSocket);
        self._dataRecorder = DataRecoder();
        self._dataEnded = False;       


    def _run(self, msg):
        '''
            This function is called repeatedly like an infinite while loop
        '''
        if self._dataEnded:
            self._messenger.send("data_ended", None);
            self._stop_request.set();
            return;
        if msg is not None:
            # do something if required.
            pass;
        elif msg is None:
            # do something if required.
            pass;

        ret = self._dataRecorder.getSample();
        if ret is None:
            # data stream has ended.
            Utils.Print("The offline data has ended");
            self._dataEnded = True;
        elif ret == False:
            # data buffer is full
            DAT = self._dataRecorder.getData();
            self._messenger.send(DAT, None);
############################################################################################
            


class DataReaderMessenger(Messenger):
    def __init__(self, ThreadSocket):
        super(DataReaderMessenger, self).__init__(ThreadSocket);

    def send(self, data, reactionToMsgAtTime):
        import time;
        msg = Message(
            sender = ["DataReader"],
            receiver = ["Server"],
            dispatchTime = time.time(),
            reactionToMsgAtTime = reactionToMsgAtTime,
            data = data,
            otherData = None
        );
        self._threadSocket.sendOutput(msg);

    def receive(self, waitForInput = False, timeOut = 0.05):
        return self._threadSocket.receiveInput(waitForInput, timeOut);

    def __str__(self):
        r = "\nData Reader Messanger. Using Socket :-";
        r += str(self._threadSocket);
        r += "\n";
        return r;
############################################################################################

from Globals import Globals;
import glob;
from scipy.io import loadmat;
from Utils import Utils;
import numpy as np;
class DataReader_Offline(object):
    """
        This class reads all the dataset files with in the
        set dataset folder.

        Change the code in this class to cater for the different datasets.

        Note: 
            The class must have the function getSample which returns a tuple
            containing index of the sample, samples in form of array of all the channels,
            target frequency and total length of the dataset.
    """
    def __init__(self):
        self._dataPath = Globals.OFFLINE_DATA_PATH;
        self._dataSetFileType = "";
        self._dataSetFilesList = glob.glob(self._dataPath + "*" + Globals.OFFLINE_DATASET_FILE_TYPE);

    def _openFile(self, filePath):
        x = loadmat(filePath);
        if Globals.SHOW_DATA_WHEN_FILE_OPENED:
            Utils. Print(str(x));
        return x;

    def _largest_within_delta(self, X, k, delta):
        rigth_idx = X.searchsorted(k, 'right') - 1;
        if k - X[rigth_idx] <= delta:
            return rigth_idx;
        else:
            return None;
        
    def getSample(self):
        #    This function yields samples of the EEG data.
        for file in self._dataSetFilesList:
            data = self._openFile(file);
            for i in range(len(data["X"])):
                sample = data["X"][i];
                if i < data["trial"][0][0]:
                    targetFreq = 0.0;
                else:
                    idx = self._largest_within_delta(data["trial"][0], i, 100000000);
                    targetFreq = data["Y"][0][idx];
                yield (i,sample, targetFreq, len(data["X"]));
        yield (None,None, None, None);
    
    '''
    def getSample(self):
        #   This function yields samples of the EEG data.
        for file in self._dataSetFilesList:
            data = self._openFile(file);
            print(data);
            for i in range(len(data["Data"][0][0][0])):
                sample = data["Data"][0][0][0][i];
                targetFreq = 0.0;
                yield (i,sample, targetFreq, len(data["Data"][0][0][0]));
        yield (None,None, None, None);
    '''
############################################################################################

class DataRecoder(object):
    def getSample(self):
        '''
            Returns:
                True -> if data buffer is not filled completely and data file has not ended.
                False -> if data buffer is filled but data file has not ended.
                None -> if data file has ended.
        '''
        if self._isDataBufferFull():
            return False;
        (counter, sample, targetFreq, totalSamples) = next(self._sampleGenerator);
        if targetFreq is None and sample is None and counter is None:
            self._dataEnded = True;
            return None;
        self._fillDataBuffer((counter, sample, targetFreq, totalSamples));
        return True;

    def _fillDataBuffer(self, sample):
        self._DATA_BUFFER.append(sample);
    
    def _isDataBufferFull(self):
        if len(self._DATA_BUFFER) >= self._DATA_MAX_SAMPLES - 1:
            return True;
        return False;

    def _emptyBuffer(self):
        self._DATA_BUFFER = [];

    def endOfData(self):
        return self._dataEnded;

    def getData(self):
        if self._isDataBufferFull():
            (count, sample, targetFreq, totalSamples) = self._DATA_BUFFER[0];
            buffer = np.zeros((self._DATA_MAX_SAMPLES - 1, 3 + len(sample)));
            counter = 0;
            for samples in self._DATA_BUFFER:
                (count, sample, targetFreq, totalSamples) = samples;
                for i in range(len(sample)):
                    buffer[counter][i] = sample[i-1];
                offset_index = len(sample);
                ###################################################################################
                ##   UPDATE THE Global.DATA_FRAME_APPENDAGE VARIABLE IF MORE COLUMNS ARE ADDED.  ##
                ###################################################################################
                buffer[counter][offset_index + 0] = targetFreq;
                buffer[counter][offset_index + 1] = count;
                buffer[counter][offset_index + 2] = totalSamples;
                #################################################################################
                counter += 1;
            self._emptyBuffer();
            return np.asmatrix(buffer);
        else:
            return None;


    def __init__(self):
        self._dataReader = None;
        if Globals.DATA_SOURCE == "offline":
            self._dataReader = DataReader_Offline();
        elif Globals.DATA_SOURCE == "online":
            self._dataReader = DataReader_Online();
        else:
            raise Exception("Error! Data source not provided");

        self._DATA_BUFFER = [];
        self._dataEnded = False;
        self._DATA_MAX_BUFFER_TIME_SEC = Globals.DATA_MAX_BUFFER_TIME_SEC;
        self._DATA_SAMPLING_FREQ_HZ = Globals.DATA_SAMPLING_FREQ
        self._DATA_MAX_SAMPLES = int(self._DATA_MAX_BUFFER_TIME_SEC * self._DATA_SAMPLING_FREQ_HZ);
        self._sampleGenerator = self._dataReader.getSample();
############################################################################################
        
