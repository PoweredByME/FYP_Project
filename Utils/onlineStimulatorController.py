'''
    First run the python_server.py
    Then run the python_controller.py
    to connect the system.
'''

import paho.mqtt.client as mqtt;
import time;
import json;

class onlineStimulatorController(object):
    '''
        This class is used to control the things which are
        shown on the stimulator.

        This controller uses mqtt protocol to convey the 
        prefrence messages to the python_server.py of the 
        stimulator
    '''
    def __init__(self, clientName):
        #self._mqtt_broker = "broker.hivemq.com";
        #self._mqtt_broker = "test.mosquitto.org";
        self._mqtt_broker = "iot.eclipse.org";
        self._mqtt_client_name = clientName;
        self._mqtt_client = mqtt.Client(self._mqtt_client_name);
        print("Connecting to broker " +  self._mqtt_broker);
        
    def publish(self, STRING):
        self._mqtt_client.publish(self._mqtt_topic, STRING);
    
    def subscribe(self, TOPIC = None):
        if TOPIC is None:
            self._mqtt_client.subscribe(self._mqtt_topic);
            return;
        self._mqtt_topic = TOPIC;
        self._mqtt_client.subscribe(TOPIC);

    def onRecieveMsg(self, onRecieveMsgFunction):
        self._mqtt_client.on_message = onRecieveMsgFunction;

    def setTopic(self, topicName):
        self._mqtt_topic = topicName;

    def onLog(self, onLogFunction):
        self._mqtt_client.on_log = onLogFunction;

    def onConnect(self, onConnectFunction):
        self._mqtt_client.on_connect = onConnectFunction;

    def start(self):
        self._mqtt_client.connect(self._mqtt_broker);
        self._mqtt_client.loop_start();

    def end(self):
        self._mqtt_client.loop_stop();
        self._mqtt_client.disconnect();
###############################################################



