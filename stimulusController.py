from Utils.onlineStimulatorController import onlineStimulatorController;
import json;
import time;
from worker import Worker;
from Utils.Utils import Print, msg2dict;
from message import Message,Messenger;

_mqtt_broker_connected = False;
def setupMQTT(client_name, onRcvMsg_function):
    
    mqtt_topic = "ssvep/stimulator";
    def on_log(client, userdata, level, buf):
        return;
        Print("LOG : " + str(buf));

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            Print("connect OK");
            global _mqtt_broker_connected;
            _mqtt_broker_connected = True;
        else:
            Print("Bad connection Returned. Code = " + str(rc));

    def on_message(client, userdata, msg):
        topic = msg.topic;
        m_decode = str(msg.payload.decode());
        onRcvMsg_function(m_decode);


    s = onlineStimulatorController(client_name);
    s.onLog(on_log);
    s.onConnect(on_connect);
    s.start();
    Print("Connecting to MQTT broker");
    _counter = 0;
    _counter_limit = 10;
    import time;
    while not _mqtt_broker_connected:
        time.sleep(1);
        _counter += 1;
        if _counter > _counter_limit:
            Print("Broker connection timeout. Could not connect to the broker");
            return None;
    if _mqtt_broker_connected:
        Print("MQTT broker has been connected");
    s.setTopic(mqtt_topic);
    s.subscribe();
    s.onRecieveMsg(on_message);
    return s;









    










class StimulusController_Worker(Worker):
    def __init__(self, threadSocket, waitForInput = False, name = "StimulusController"):
        super(StimulusController, self).__init__(threadSocket, waitForInput, name);
        self._messenger = StimulusControllerMessenger(self._threadSocket);
        self._mqtt_client = setupMQTT("_ssvep_simulator_controler", self.onRecieveMsg);
        self._mqtt_stimulator_server_connected = False;
        self._stimuli_ended = False;
        for i in range(0,1000):
            if self._mqtt_stimulator_server_connected:
                Print("Server connected")
                break;
            self._mqtt_client.publish(json.dumps({"request" : "controller_broadcasting", "src" : "stimulator_controller"}));
            time.sleep(0.3);
            Print("Stimulus Controller Attempting to connect..." + str(i));

    def isConnected(self):
        return self._mqtt_stimulator_server_connected;

    def onRecieveMsg(self, msg):
        msg = json.loads(msg);
        if msg["src"] == "stimulator_server":
            if msg["request"] == "controller_broadcast_recieved":
                self._mqtt_stimulator_server_connected = True;
            else:
                Print(str(msg));


    def _sendData(self, boxes, options):
        DATA  = {
            "boxes" : boxes,
            "opts" : options,
            "src" : "stimulator_controller",
            "request" : "update"
        };

        DATA = json.dumps(DATA); 
        Print("Sending Data...")
        self._mqtt_client.publish(DATA);
        time.sleep(1);

    def makeBox(self, freq, text, textFlicker = False):
        true = True;
        false = False;
        return {
            "f" : str(freq),
            "text" : text,
            "opts" : {
                "fBackLoop" : true,
                "flickerText" : textFlicker,
                "showEdit" : false,
                "showInfo" : true,
                "infos" : {
                    "avgF" : true,
                    "curDuty" : false,
                    "curF" : false,
                    "curPer" : false,
                    "rangeF" : false
                },
            },
        };

    def makeOptions(self):
        return {
            "cols" : 2,
            "fontS" : 1,
            "fontB" : True,
        };


    def _run(self, msg):
        if self._stimuli_ended:
            self._messenger.send("stimuli_ended", None)
        msg = msg2dict(msg);
        Print("Starting the stimulus feed");
        
        def addStim(list, freq, text):
            list.append((0, text));
            list.append((0, text));
            list.append((freq, text));

        presentationTimeOfStimulus_sec = 1;
        stimuli = [];
        _sw = True;
        for i in range(10):
            if _sw:
                addStim(stimuli, 13, "A");
            else:
                addStim(stimuli, 15, "B");
            _sw = not _sw;

        for stim in stimuli:
            (freq, text) = stim;
            opts = self.makeOptions();
            if freq == 0:
                box = [];
            else:
                box = [self.makeBox(freq, text)];
            Print(str(box));
            self._sendData(box, opts);
            time.sleep(presentationTimeOfStimulus_sec);
    
        self._stimuli_ended = True;
        

class StimulusControllerMessenger(Messenger):
    def __init__(self, ThreadSocket):
        super(StimulusControllerMessenger, self).__init__(ThreadSocket);

    def send(self, data, reactionToMsgAtTime):
        import time;
        msg = Message(
            sender = ["StimulusController"],
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




class StimulusController(object):
    def __init__(self):
        self._mqtt_client = setupMQTT("_ssvep_simulator_controler", self.onRecieveMsg);
        self._mqtt_stimulator_server_connected = False;
        for i in range(0,1000):
            if self._mqtt_stimulator_server_connected:
                Print("Server connected")
                break;
            self._mqtt_client.publish(json.dumps({"request" : "controller_broadcasting", "src" : "stimulator_controller"}));
            time.sleep(0.3);
            Print("Stimulus Controller Attempting to connect..." + str(i));
        self._currentStimStart = None;

    def isConnected(self):
        return self._mqtt_stimulator_server_connected;

    def onRecieveMsg(self, msg):
        msg = json.loads(msg);
        if msg["src"] == "stimulator_server":
            if msg["request"] == "controller_broadcast_recieved":
                self._mqtt_stimulator_server_connected = True;
            elif msg["request"] == "timestamp":
                self._currentStimStart = msg["timestamp"];
            else:
                Print(str(msg));

    def getCurrentStimTimeStamp(self):
        return self._currentStimStart;

    def sendData(self, boxes, options):
        DATA  = {
            "boxes" : boxes,
            "opts" : options,
            "src" : "stimulator_controller",
            "request" : "update"
        };

        DATA = json.dumps(DATA); 
        Print("Sending Data...")
        self._mqtt_client.publish(DATA);
        self._currentStimStart = None;
        time.sleep(0.3);


    def makeBox(self, freq, text, textFlicker = False):
        true = True;
        false = False;
        return {
            "f" : str(freq),
            "text" : text,
            "opts" : {
                "fBackLoop" : true,
                "flickerText" : textFlicker,
                "showEdit" : false,
                "showInfo" : true,
                "infos" : {
                    "avgF" : true,
                    "curDuty" : false,
                    "curF" : false,
                    "curPer" : false,
                    "rangeF" : false
                },
            },
        };

    def makeOptions(self):
        return {
            "cols" : 2,
            "fontS" : 1,
            "fontB" : True,
        };
