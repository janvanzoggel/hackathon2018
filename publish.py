from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bureau", action="store", required=True, dest="bureau", help="ID van het bureau")
parser.add_argument("-s", "--stand", action="store", required=True, dest="stand", help="Stand van het bureau")
parser.add_argument("-p", "--persoon", action="store", required=True, dest="persoon", help="Persoon aan het bureau")

args = parser.parse_args()

host = "xxxxxxxxx-ats.iot.eu-central-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "rbx12.cert.pem"
privateKeyPath = "rbx12.private.key"
port = 443
useWebsocket = False
clientId = "rbx12"
topic = "rbx/event"

bureau = args.bureau
stand = args.stand
persoon = args.persoon

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
time.sleep(2)

# Publish to the same topic in a loop forever
message = {}
message['bureau'] = bureau
message['stand'] = stand
message['persoon'] = persoon
message['timestamp'] = time.time()
messageJson = json.dumps(message)
myAWSIoTMQTTClient.publish(topic, messageJson, 1)
print('Published topic %s: %s\n' % (topic, messageJson))
