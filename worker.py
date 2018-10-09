'''
    This is the genric worker class on which all of the threads of the systems are based.

    The worker thread takes two Queues refrences (globle).
    -> Input Queue
    -> Output Queue

    This code is inspired from:
    https://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping
'''
import os, time, threading;
from queue import Queue;
import queue;

class Worker(threading.Thread):
    def __init__(self, input_queue, output_queue, name = ""):
        super(Worker, self).__init__();
        self._input_queue = input_queue;
        self._output_queue = output_queue;
        self._stop_request = threading.Event();
        self._name = name;

    
    def _isStopRequest(self):
        # Return true if the self._stop_request has been set.
        return self._stop_request.isSet();

    def run(self):
        '''
            This function checks if the stop request has been made. If
            this is the case then the function ends. This function also
            waits for the _input_queue to get filled. If it is filled 
            then program wirks on it. Otherwise, it waits for it to get
            filled and prevents CPU cycles from getting wasted.
        '''
        while not self._isStopRequest():
            try:
                task = self._input_queue.get(True, 0.05);
                print(self._name + ":-> Doing work. Task " + str(task));
            except queue.Empty:
                print("No data available");
                continue;

        print(self._name + ":-> Exiting thread");

    def join(self, timeout = None):
        self._stop_request.set();
        super(Worker, self).join(timeout);

    
        


    