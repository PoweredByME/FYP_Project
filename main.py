'''
    This is the main entry point of the entire code.
'''

from queue import Queue;
from worker import Worker;
from message import Message, Messenger;
from threadSocket import threadSocket;
from dataReader import DataReader;
from analyser import Analyser;
import time;
from Utils import Utils;
from matplotlib import pyplot as plt;
from analysisVisualizer import analysisVisualizer;
from stimulusController import StimulusController;

def SERVER_WORKER_INIT(_threadSocketName, _Messenger, _Worker, threadPool):
    _thread_socket = threadSocket(_threadSocketName);
    _messenger = _Messenger(_thread_socket);
    _worker = _Worker(_thread_socket);
    threadPool.append(_worker);
    return (_thread_socket, _messenger, _worker);

'''def main():
    
    threadPool = [];

    visualizer = analysisVisualizer();
    #setting up data reader thread
    (dataReaderThreadSocket, dataReaderMessenger, dataReaderWorker) = SERVER_WORKER_INIT("server2dataReader", ServerMessenger, DataReader, threadPool);
    (analyserThreadSocket, analyserMessenger, analyserWorker) = SERVER_WORKER_INIT("server2analyser", ServerMessenger, Analyser, threadPool);
    (stimulusControllerThreadSocket, stimulusControllerMessenger, stimulusControllerWorker) = SERVER_WORKER_INIT("server2stimulusController", ServerMessenger, StimulusController, threadPool);

    try:
        # make a thread pool which contains all the thread which are to be executed.
        # start all threads in the pool.
        for _thread in threadPool:
            _thread.start();

        analyserHasAskedForData = False;
        dataReaderServerBuffer = [];
        stimulusControllerMSG = stimulusControllerMessenger.receive();
        stimulusControllerMSG = Utils.msg2dict(stimulusControllerMSG);

        if not stimulusControllerMSG == None and stimulusControllerMSG["data"] == "stimuli_ended":
            joinThreads(threadPool);

        while True:
            ''
                This loop recieves messages from all of the
                messengers and 
            ''
            while True:
                # get all the messages received by the data reader messenger. 
                dataReaderMSG = dataReaderMessenger.receive();
                if dataReaderMSG is not None:
                    dataReaderMSG = Utils.msg2dict(dataReaderMSG);
                    dataReaderServerBuffer.append(dataReaderMSG);
                else:
                    break;

            
            analyserMSG = analyserMessenger.receive();
            if analyserMSG is not None:
                analyserMSG = Utils.msg2dict(analyserMSG);
                if isinstance(analyserMSG["data"], str) and analyserMSG["data"] == "send_data":
                    analyserHasAskedForData = True;
                else:
                    DATA = analyserMSG["data"];
                    if DATA["type"] == "fft":
                        target_ssvep = DATA["target_ssvep"];
                        DATA = DATA["data"];
                        freq_13 = [];
                        freq_15 = [];
                        for _item in DATA:
                            freq_13.append(_item["fftData"][13][0]);
                            freq_15.append(_item["fftData"][15][0]);

                        for _item in DATA:
                            freq_13.append(_item["fftData"][26][0]);
                            freq_15.append(_item["fftData"][30][0]);
                        Utils.Print("=" * 20);
                        Utils.Print("Target Frequency : " + str(target_ssvep));
                        Utils.Print("freq_13 -> " + str(freq_13));
                        Utils.Print("freq_15 -> " + str(freq_15));
                        Utils.Print("=" * 20);
                        #visualizer.SET_DATA__fft_plot_for_4_channel_data(DATA);
            
            if analyserHasAskedForData:
                if len(dataReaderServerBuffer) == 0:
                    dataReaderMSG = None;
                else:
                    dataReaderMSG = dataReaderServerBuffer.pop(0);
            else:
                dataReaderMSG = None;
                
            if dataReaderMSG is not None:
                if isinstance(dataReaderMSG["data"], str) and dataReaderMSG["data"] == "data_ended":
                    Utils.Print("Joining all threads");
                    joinThreads(threadPool);
                    return;
                if analyserHasAskedForData:
                    analyserMessenger.send(dataReaderMSG["data"], ["Analyser"]);
                    analyserHasAskedForData = False;
                
                
                
            


    finally:
        # execute the clean up code.
        Utils.Print("Joining all threads");
        joinThreads(threadPool);

def joinThreads(threadList):
    for _thread in threadList:
        _thread.join();
'''

'''
class ServerMessenger(Messenger):
    ''
        This messenger only conveys the messages.
        It does not Adapt any message.
    ''
    def __init__(self, ThreadSocket):
        super(ServerMessenger, self).__init__(ThreadSocket);

    def send(self, data, receiversList):
        import time;
        msg = Message(
            sender = ["Server"],
            receiver = receiversList,
            dispatchTime = time.time(),
            reactionToMsgAtTime = None,
            data = data,
            otherData = None
        );
        self._threadSocket.sendInput(msg);

    def receive(self, waitForInput = False, timeOut = 0.05):
        return self._threadSocket.receiveOutput(waitForInput, timeOut);

    
    def __str__(self):
        r = "\nServer Messanger. Using Socket :-";
        r += str(self._threadSocket);
        r += "\n";
        return r;

'''

def makeStimuli():
    '''
        This function creates a list of 
        all the stimuli which are to be presented
        by the stimulator

        RETURN:
            ->  list containing the info about each 
                stimulus. Like, the frequency of the
                box, text of the box, should the text
                flicker or not and the time for which
                stimulus should show up.
    '''

    stimuli = [];
    _sw = True;
    for i in range(20):
        if _sw:
            freq = 13; text = "A";
        else:
            freq = 15; text = "B";
        _sw = not _sw;
        stimuli .append({
            "freq" : 0,
            "text" : None,
            "presistanceTime_sec" : 10,
            });
        stimuli .append({
            "freq" : freq,
            "text" : text,
            "presistanceTime_sec" : 5 ,
            });
    stimuli .append({
            "freq" : 0,
            "text" : None,
            "presistanceTime_sec" : 10,
            });
    return stimuli;

def main():
    stimuli = makeStimuli();
    stimCtrl = StimulusController();
    
    last_stimulus_timestamp = 0;
    request_time_interval = (0,0);

    _stim_counter = 1;
    for stimulus in stimuli:
        Utils.Print("Showing stimulus -> " + str(_stim_counter) + "/" + str(len(stimuli)) + ". " + str(stimulus));
        _stim_counter += 1;
        freq = stimulus["freq"];
        text = stimulus["text"];
        presistanceTime_sec = stimulus["presistanceTime_sec"];
        box = [stimCtrl.makeBox(freq,text)];
        opts = stimCtrl.makeOptions();
        if freq == 0:
            box = [];
        stimCtrl.sendData(box, opts);
        _counter = 0;
        _counter_limit = 400
        Utils.Print("Waiting for stimulators response");
        while True:
            timestamp = stimCtrl.getCurrentStimTimeStamp();
            if not timestamp == None:
                break;
            if _counter > _counter_limit:
                _counter = 0;
                Utils.Print("No response for the timestamp of the inittiation of the stimulus. Something is wrong :(");
                return;
            _counter += 1;
            time.sleep(0.1);

        
        if last_stimulus_timestamp == 0:
        request_time_interval = (last_stimulus_timestamp, timestamp);
        last_stimulus_timestamp = timestamp;
        Utils.Print(request_time_interval);    
        _current_time_0 = time.time();
        # request the data chunk. Somehow... :| 
        # ...... code here
        # process the data chunk. Somehow... :(
        # ...... code here
        time.sleep(1.5);
        # end of the processing of the data chunk... :)
        _current_time_1 = time.time();
        # get how much time remains before showing the
        # next stimulus and pause the thread for the
        # remaining time.
        pauseTime = presistanceTime_sec - (_current_time_1 - _current_time_0);
        Utils.Print("Pausing the thread for " + str(pauseTime) + " seconds");
        time.sleep(pauseTime);


# Call main function if this script is the main script.
if __name__ == "__main__":
    main();