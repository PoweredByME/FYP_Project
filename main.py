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

def SERVER_WORKER_INIT(_threadSocketName, _Messenger, _Worker, threadPool):
    _thread_socket = threadSocket(_threadSocketName);
    _messenger = _Messenger(_thread_socket);
    _worker = _Worker(_thread_socket);
    threadPool.append(_worker);
    return (_thread_socket, _messenger, _worker);

def main():
    
    threadPool = [];

    visualizer = analysisVisualizer();
    #setting up data reader thread
    (dataReaderThreadSocket, dataReaderMessenger, dataReaderWorker) = SERVER_WORKER_INIT("server2dataReader", ServerMessenger, DataReader, threadPool);
    (analyserThreadSocket, analyserMessenger, analyserWorker) = SERVER_WORKER_INIT("server2analyser", ServerMessenger, Analyser, threadPool);

    try:
        # make a thread pool which contains all the thread which are to be executed.
        # start all threads in the pool.
        for _thread in threadPool:
            _thread.start();

        analyserHasAskedForData = False;
        dataReaderServerBuffer = [];
        while True:
            time.sleep(0.5);
            '''
                This loop recieves messages from all of the
                messengers and 
            '''
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
                    print("he");
                    dataReaderMSG = dataReaderServerBuffer.pop(0);
                    print("she");
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


class ServerMessenger(Messenger):
    '''
        This messenger only conveys the messages.
        It does not Adapt any message.
    '''
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

# Call main function if this script is the main script.
if __name__ == "__main__":
    main();