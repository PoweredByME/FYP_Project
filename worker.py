'''
    This is the genric worker class on which all of the threads of the systems are based.

    The worker thread takes two Queues refrences (globle).
    -> Input Queue
    -> Output Queue

    This code is inspired from:
    https://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping
'''
import os, time, threading;
from threadSocket import threadSocket;
from message import Messenger;
from Utils.Utils import Print;

class Worker(threading.Thread):
    def __init__(self, threadSocket, waitForInput = True, name = ""):
        super(Worker, self).__init__();
        self._threadSocket = threadSocket;
        self._messenger = WorkerMessenger(self._threadSocket);
        self._stop_request = threading.Event();
        self._name = name;
        self._waitForInput = waitForInput;
        self._init_askForData_sent = False;
    
    def _askServerForData(self):
        pass;

    def _isStopRequest(self):
        # Return true if the self._stop_request has been set.
        return self._stop_request.isSet();

    def run(self):
        '''
            This function checks if the stop request has been made. If
            this is the case then the function ends. This function also
            waits for the _input_queue to get filled. If it is filled 
            then program works on it. Otherwise, it waits for it to get
            filled and prevents CPU cycles from getting wasted.
        '''
        if not self._init_askForData_sent:
            self._askServerForData();
            self._init_askForData_sent = True;
        while not self._isStopRequest():
            msg = self._messenger.receive(waitForInput = self._waitForInput);
            if msg == -1:
                # No data is recieved
                continue;
            self._run(msg);

        Print("Thread Name = " + self._name + " [Exiting thread]");

    def _run(self, msg):
        '''
            This is the function which is to be polymorphed for different
            child classes.

            This funciton always gets a Message(Object).

            The msg can be None or Message(object).
        '''
        if msg is None:
            Print("message -> None");
            return;
        (sender, receiver, dispatchTime, reactionOfMsgAtTime, data, otherData) = msg.unpack();
        Print(self._name + ":-> Doing work. Task " + str(data));
        #Print("\n" + str(msg) + "\n");
            

    def join(self, timeout = None):
        self._stop_request.set();
        super(Worker, self).join(timeout);

    
        

class WorkerMessenger(Messenger):
    '''
        Parent class for the messenger of all the 
        workers / peers
    '''
    def __init__(self, ThreadSocket):
        super(WorkerMessenger, self).__init__(ThreadSocket);

    def send(self, data):
        import time;
        msg = Message(
            sender = ["Worker"],
            receiver = ["None"],
            dispatchTime = time.time(),
            reactionToMsgAtTime = reactionToMsgAtTime,
            data = data,
            otherData = None
        );
        self._threadSocket.sendOutput(msg);

    def receive(self, waitForInput = True, timeOut = 0.05):
        return self._threadSocket.receiveInput(waitForInput, timeOut);

