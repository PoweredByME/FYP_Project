'''
    This script contains the Message object which is the default
    data type for the communication of messages with in the system.
'''

class Message(object):
    def __init__(self, sender, receiver, dispatchTime, reactionToMsgAtTime, data, otherData = None):
        '''
            Inputs:
                sender -> (list of strings)
                receiver -> (list of strings)
                dispatchTime -> (number) [Tell that this message has been sent at T dispatchTime]
                reactionToMsgAtTime -> (number) [Tell that this message is the result of the query sent at T dispatchTime]
                data -> (object)
                otherData -> (object) [All the other important data which has to be communicated in the future. For future extensions]
        '''
        self._sender = sender;
        self._receiver = receiver;
        self._dispatchTime = dispatchTime;
        self._data = data;
        self._reactionToMsgAtTime = reactionToMsgAtTime;
        self._otherData = otherData;

    def __str__(self):
        ret = "";
        ret += "-" * 20;
        ret += "\n1. sender = " + str(self._sender);
        ret += "\n2. receiver = " + str(self._receiver);
        ret += "\n3. dispatchTime = " + str(self._dispatchTime);
        ret += "\n4. reactionToMsgAtTime = " + str(self._reactionToMsgAtTime);
        ret += "\n5. data = " + str(self._data);
        ret += "\n6. otherData = " + str(self._otherData);
        ret += "\n"
        ret += "-" * 20;
        
        
        return ret;

    def unpack(self):
        '''
            Output:
                (
                    sender, receiver, dispatchTime, reactionToMsgAtTime, data, otherData
                )
        '''
        return (self._sender, self._receiver, self._dispatchTime, self._reactionToMsgAtTime, self._data, self._otherData);



class Messenger(object):
    '''
        A parent class for all the peer messengers
    '''
    def __init__(self, threadSocket):
        self._threadSocket = threadSocket;

    def send(self, msg, reactionToMsgAtTime):
        pass;

    def receive(self):
        pass;

    def _sendAdapter(self, msg):
        pass;

    def _receiveAdapter(self, msg):
        pass;

    def getThreadSocket(self):
        return self._threadSocket;
