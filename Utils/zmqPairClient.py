import zmq
import random
import sys
import time


class zmqPairClient(object):
    def __init__(self, ip, port):
        self._ip = ip;
        self._port = port;
        self._bindingAddress = "tcp://" + str(self._ip) + ":" + str(port);
        Utils.Print("Pair client connecting to server @ : " + self._bindingAddress);

    def getIP(self):
        return self._ip;
    
    def getPort(self):
        return self._port;

    def getBindingAddress(self):
        return self._bindingAddress;

    def connect(self):
        self._context = zmq.Context();
        self._socket = self._context.socket(zmq.PAIR);
        self._socket.connect(self._bindingAddress);

    def listen(self, onRecieveMsg):
        self._onRecieveMsg = onRecieveMsg;
        while True:
            msg = self._socket.recv();
            self._onRecieveMsg(msg);
    
    def send(self,STRING):
        self._socket.send_string(STRING);



import Utils;
client = zmqPairClient(Utils.getComputerIP(), "5556");

def onRecvMsg(msg):
    Utils.Print(str(msg));
    client.send("Hello From Client");

client.connect();
client.send("Init connection");
client.listen(onRecvMsg);