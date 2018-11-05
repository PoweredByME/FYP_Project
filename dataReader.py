'''
    This is a peer/worker which deal with the reading of the
    data from the an online or offline source.

    The DataReader class is a child of Worker class. It has is own
    thread.
'''

from worker import Worker;
from message import Messenger, Message;

class DataReader(Worker):
    def __init__(self, threadSocket, waitForInput = False, name = "DataReader"):
        super(DataReader, self).__init__(threadSocket, waitForInput, name);
        self._d = [];
        self._counter = 0;
        self._messenger = DataReaderMessenger(self._threadSocket);

    def _run(self, msg):
        self._counter += 1;
        if self._counter < 10:
            self._d.append(self._counter);

        if msg is None:
            return;
        
        (sender, reciever, sendersDispatchTime, reactionToMsgAtTime, data, otherData) = msg.unpack();
        if data == -2:
            self._messenger.send(self._d, sendersDispatchTime);
            self._d = [];
            self._counter = 0;




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