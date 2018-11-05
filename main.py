'''
    This is the main entry point of the entire code.
'''

from queue import Queue;
from worker import Worker;
from message import Message, Messenger;
from threadSocket import threadSocket;
from dataReader import DataReader;
import time;

def SERVER_WORKER_INIT(_threadSocketName, _Messenger, _Worker, threadPool):
    _thread_socket = threadSocket(_threadSocketName);
    _messenger = _Messenger(_thread_socket);
    _worker = _Worker(_thread_socket);
    threadPool.append(_worker);

    return (_thread_socket, _messenger, _worker);

def main():
    
    threadPool = [];

    #setting up data reader thread
    (dataReaderThreadSocket, dataReaderMessenger, dataReaderWorker) = SERVER_WORKER_INIT("server2dataReader", ServerMessenger, DataReader, threadPool);


    try:
        # make a thread pool which contains all the thread which are to be executed.
        # start all threads in the pool.
        for _thread in threadPool:
            _thread.start();

        for i in range(5):
            time.sleep(0.0001)
            dataReaderMessenger.send(-2, ["dataReader"]);
            time.sleep(0.001)
            msg = dataReaderMessenger.receive();
            print(msg);
            #time.sleep(0.000001);

    finally:
        # execute the clean up code.
        for _thread in threadPool:
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