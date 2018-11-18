from worker import Worker;
from message import Message,Messenger;
from Utils import Utils;
from Globals import Globals;
import time;
import numpy as np;

class Analyser(Worker):
    def __init__(self, threadSocket, waitForInput = True, name = "Analyser"):
        super(Analyser, self).__init__(threadSocket, waitForInput, name);
        self._messenger = AnalyserMessenger(self._threadSocket);
        #self._counter = 0; used it for debugging the multithreaded system;

    def _askServerForData(self):
        self._messenger.send("send_data", None);

    def _run(self, msg):
        msg = Utils.msg2dict(msg);
        if msg is None: return;
        DATA = [];
        for i in range(0,4):
            fAx, fftData = Utils.computeFFT(msg["data"][:,i], Globals.DATA_SAMPLING_FREQ);
            fAx = fAx[0:fftData.shape[0]];
            DATA.append(
                {
                    "channel" : i+1,
                    "fAx" : fAx,
                    "fftData" : fftData
                }
            );
        target_freq = np.asarray(msg["data"][:, 4]);
        target_ssvep = sum(target_freq) / (len(target_freq) * max(target_freq)) * 100;
        DATA = {
            "type" : "fft",
            "data" : DATA,
            "target_ssvep" : target_ssvep
        }
        #Utils.Print(str(self._counter));
        #self._counter += 1;
        self._messenger.send(DATA, msg["reactionToMsgAtTime"]);
        self._askServerForData();
        


    
class AnalyserMessenger(Messenger):
    def __init__(self, ThreadSocket):
        super(AnalyserMessenger, self).__init__(ThreadSocket);

    def send(self, data, reactionToMsgAtTime):
        import time;
        msg = Message(
            sender = ["Analyser"],
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
