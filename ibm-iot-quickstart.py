##*****************************************************************************
## Copyright (c) 2014 IBM Corporation and other Contributors.
##
## All rights reserved. This program and the accompanying materials
## are made available under the terms of the Eclipse Public License v1.0
## which accompanies this distribution, and is available at
## http://www.eclipse.org/legal/epl-v10.html
##
## Contributors:
## IBM - Initial Contribution
##*****************************************************************************
## IoT Foundation QuickStart Driver
## A sample IBM Internet of Things Foundation Service client for Intel Internet of Things Gateway Solutions

import time
import client as mqtt
import json
import uuid


#Class for retrieving CPU % utilisation
class CPUutil(object):
		def __init__(self):
				self.prev_idle = 0
				self.prev_total = 0
				self.new_idle = 0
				self.new_total = 0
		def get(self):
				self.read()
				delta_idle = self.new_idle - self.prev_idle
				delta_total = self.new_total - self.prev_total
				cpuut = 0.0
				if (self.prev_total != 0) and (delta_total != 0):
						cpuut = ((delta_total - delta_idle) * 100.0 / delta_total)
				return cpuut
		def read(self):
				self.prev_idle = self.new_idle
				self.prev_total = self.new_total
				self.new_idle = 0;
				self.new_total = 0;
				with open('/proc/stat') as f:
						line = f.readline()
				parts = line.split()
				if len(parts) >= 5:
						self.new_idle = int(parts[4])
						for part in parts[1:]:
								self.new_total += int(part)


#Initialise class to retrieve CPU Usage
cpuutil = CPUutil()

macAddress = hex(uuid.getnode())[2:-1]
macAddress = format(long(macAddress, 16),'012x')
#remind the user of the mac address further down in code (post 'connecitng to QS')

#Set the variables for connecting to the Quickstart service
organization = "quickstart"
deviceType = "iotsample-gateway"
broker = ""
topic = "iot-2/evt/status/fmt/json"
username = ""
password = ""


error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)

try:

		file_object = open("./device.cfg")
		
		for line in file_object:
				
				readType, readValue = line.split("=")
			
				if readType == "org":	
						organization = readValue.strip()
				elif readType == "type": 
						deviceType = readValue.strip()
				elif readType == "id": 
						macAddress = readValue.strip()
				elif readType == "auth-method": 
						username = "use-token-auth"
				elif readType == "auth-token": 
						password = readValue.strip()
				else:
						print("please check the format of your config file") #will want to repeat this error further down if their connection fails?
		
		file_object.close()
										
		print("Configuration file found - connecting to the registered service")
		
except error_to_catch:
		print("No config file found, connecting to the Quickstart service")
		print("MAC address: " + macAddress)


#Creating the client connection
#Set clientID and broker
clientID = "d:" + organization + ":" + deviceType + ":" + macAddress
broker = organization + ".messaging.internetofthings.ibmcloud.com"

mqttc = mqtt.Client(clientID)

#Set authentication values, if connecting to registered service
if username is not "":
		mqttc.username_pw_set(username, password=password)

mqttc.connect(host=broker, port=1883, keepalive=60)


#Publishing to IBM Internet of Things Foundation
mqttc.loop_start() 

while mqttc.loop() == 0:
	
		cpuutilvalue = cpuutil.get()
		print cpuutilvalue

		msg = json.JSONEncoder().encode({"d":{"cpuutil":cpuutilvalue}})
		
		mqttc.publish(topic, payload=msg, qos=0, retain=False)
		print "message published"

		time.sleep(5)
		pass



