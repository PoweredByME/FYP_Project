import zmq
import random
import sys
import time
import Utils;

class zmqPairServer(object):
    def __init__(self, ip, port):
        self._ip = ip;
        self._port = port;
        self._bindingAddress = "tcp://" + str(self._ip) + ":" + str(port);
        Utils.Print("Pair server's binding address : " + self._bindingAddress);

    def getIP(self):
        return self._ip;
    
    def getPort(self):
        return self._port;

    def getBindingAddress(self):
        return self._bindingAddress;

    def connect(self):
        self._context = zmq.Context();
        self._socket = self._context.socket(zmq.PAIR);
        self._socket.bind(self._bindingAddress);

    def listen(self, onRecieveMsg):
        self._onRecieveMsg = onRecieveMsg;
        while True:
            msg = self._socket.recv();
            self._onRecieveMsg(msg);
    
    def send(self,STRING):
        self._socket.send_string(STRING);





server = zmqPairServer(Utils.getComputerIP(), 5556);
server.connect();

def onRecvMsg(msg):
    Utils.Print(str(msg));
    server.send("Hello from server");

server.listen(onRecvMsg);