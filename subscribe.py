from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import os

# Callback
def customCallback(client, userdata, message):
        topic = message.topic
        payload = message.payload.decode("utf-8")
        j = json.loads(payload)
        hoogte = str(j['hoogte'])
        print('We moeten naar hoogte: ' + hoogte)
        commando = "python korsakov.py " + hoogte
        print('commando: ' + commando)
        os.system(commando)

# Read in command-line parameters
host = "xxxxxx-ats.iot.eu-central-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "rbx12.cert.pem"
privateKeyPath = "rbx12.private.key"
port = 443
clientId = "rbx12"
topic = "rbx/command"

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

while True:
    None
