'''
    This is a socket via which the threads will communicate with eachother.
    Each socket have a send queue and a recieve queue.
'''

class threadSocket(object):
    
    def __init__(self, name = "", debug = False):
        from queue import Queue;
        self._sendQueue = Queue();
        self._receiveQueue = Queue();
        self._sqLen = 0;
        self._rqLen = 0;
        self._name = name
        self._debug = debug;

    def lengths(self):
        _sendQueueLength = self._sqLen
        _receiveQueueLength = self._rqLen;
        return (_sendQueueLength, _receiveQueueLength);

    def getRQL(self):
        '''
            Get recieve queue length
        '''
        return self._rqLen;

    def getSQL(self):
        '''
            Get send queue length
        '''
        return self._sqLen;
        
    def sendOutput(self, msg):
        '''
            SEND DATA INTO THE SEND QUEUE
        '''
        self._sendQueue.put(msg);
        self._sqLen += 1;

    def sendInput(self, msg):
        '''
            SEND DATA INTO THE RECEIVE QUEUE
        '''
        self._receiveQueue.put(msg);
        self._rqLen += 1;

    def receiveInput(self, waitForInput = True, timeOut = 0.05):
        '''
            GET DATA OUT OF THE RECEIVE QUEUE

            waitForInput -> True means that the system will
            wait for the receive queue to get filled. If the
            queue is empty. The it will cause the thread to
            go to sleep for a specific time period.
        '''
        import queue;
        try:
            if waitForInput:
                self._rqLen -=1 ;
                return self._receiveQueue.get(waitForInput, timeOut);
            elif self._receiveQueue.empty():
                return None;
            else:
                self._rqLen -=1;
                return self._receiveQueue.get();
        except queue.Empty:
            if not self._debug:
                return None;
            from Utils.Utils import Print;
            Print("Socket name = " + self._name + " [Receive Queue : No Data Available for more than "+ str(timeOut) + "sec]");
            return None;

    def receiveOutput(self, waitForInput = True, timeOut = 0.05):
        '''
            GET DATA OUT OF THE SEND QUEUE

            waitForInput -> True means that the system will
            wait for the receive queue to get filled. If the
            queue is empty. The it will cause the thread to
            go to sleep for a specific time period.
        '''
        import queue;
        try:
            if waitForInput:
                self._sqLen -= 1;
                return self._sendQueue.get(waitForInput, timeOut);
            elif self._sendQueue.empty():
                return None;
            else:
                self._sqLen -= 1;
                return self._sendQueue.get();
        except queue.Empty:
            if not self._debug:
                return None;
            from Utils.Utils import Print;
            Print("Socket name = " + self._name + " [Send Queue : No Data Available for more than "+ str(timeOut) + "sec]");
            return None;

    

    def __str__(self):
        r = "\n";
        r += "Socket name = " + self._name + "\n";
        r += "Receive queue content = " + str(self._receiveQueue) + "\n";
        r += "Send queue content = " + str(self._sendQueue) + "\n";
        return r;

        


