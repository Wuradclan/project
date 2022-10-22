from MQTTLib import AWSIoTMQTTClient
from network import WLAN
import time
import utime
import config
import pycom
from mqtt import MQTTClient
import socket
import machine
import micropython
from machine import RTC



import config
import json
from MQTTLib import AWSIoTMQTTShadowClient
from MQTTLib import AWSIoTMQTTClient

from network import LoRa
import ubinascii

from pycoproc_1 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

from network import LoRa
import ubinascii

# Connect to wifi

# RGBLED
# Disable the on-board heartbeat (blue flash every 4 seconds)
# We'll use the LED to respond to messages from Adafruit IO
pycom.heartbeat(False)
time.sleep(0.1) # Workaround for a bug.
                # Above line is not actioned if another
                # process occurs immediately afterwards
pycom.rgbled(0xff0000)  # Status red = not working

# Connect to wifi to get time
wlan = WLAN(mode=WLAN.STA)
wlan.connect(config.WIFI_SSID, auth=(None, config.WIFI_PASS), timeout=50000)
pycom.rgbled(0xffd7000)
#wlan.connect(ssid='F107', auth=(WLAN.WPA2, 'Champlain@2022'))
while not wlan.isconnected():
	pycom.rgbled(0xff0000) 
	#time.sleep(2)
    #machine.idle()
print('\n')
print("WiFi connected succesfully to: ")
print(wlan.ifconfig()) # Print IP configuration
#pycom.rgbled(0xFFFF00) # Yellow
time.sleep(5)

#RTC timestamp current time syncing to get the current date and time
rtc = RTC()
#syncing the rtc to the server
print("Syncing RTC to NTP...")
rtc = RTC()
rtc.ntp_sync("pool.ntp.org", update_period=3600)
while not rtc.synced():
    pass # save power while waiting
#local_time = utc + timezone
time.timezone(-4*60**2)

#get the localtime and format it to add zeros 
def getLocalTime():
	ctime = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(time.localtime()[0],time.localtime()[1], time.localtime()[2],time.localtime()[3], time.localtime()[4], time.localtime()[5])
	return ctime
print(getLocalTime())

# user specified callback function
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

# configure the MQTT client
pycomAwsMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
pycomAwsMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
pycomAwsMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)

pycomAwsMQTTClient.configureOfflinePublishQueueing(config.OFFLINE_QUEUE_SIZE)
pycomAwsMQTTClient.configureDrainingFrequency(config.DRAINING_FREQ)
pycomAwsMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
pycomAwsMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
pycomAwsMQTTClient.configureLastWill(config.LAST_WILL_TOPIC, config.LAST_WILL_MSG, 1)


#pycomAwsMQTTClient.connect()

#Connect to MQTT Host
if pycomAwsMQTTClient.connect():
	pycom.rgbled(0x00ff00)
	print('AWS connection succeeded')
	
elif (not pycomAwsMQTTClient.connect()):
	print('AWS is not connected')

# Subscribe to topic
pycomAwsMQTTClient.subscribe(config.TOPIC, 1, customCallback)
time.sleep(2)

#collect sensors data
## read sensors data on pysense
py = Pycoproc(Pycoproc.PYSENSE)

# Temperature 
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
temperature = mp.temperature() # setting the data sensor to the varible
print("MPL3115A2 temperature: " + str(mp.temperature()))
#humidity
si = SI7006A20(py)
humidity = si.humidity()
print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")

#temperatue
temperature2 = si.temperature()
lora = LoRa()
print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
device_id = ubinascii.hexlify(lora.mac()).decode('ascii')
#light sensor
li = LTR329ALS01(py)
print("Light (channel Blue lux, channel Red lux): " + str(li.light()))
#accelerometer
acc = LIS2HH12(py)
print("Acceleration: " + str(acc.acceleration()))
print("Roll: " + str(acc.roll()))
print("Pitch: " + str(acc.pitch()))
#volatge
print("Battery voltage: " + str(py.read_battery_voltage()))
voltage = py.read_battery_voltage()
roll = acc.roll()
pitch = acc.pitch()

# Send message to host

while True:
	payload=json.dumps({"device_id": device_id,"temperature":  mp.temperature(),"humidity": si.humidity(),"voltage":py.read_battery_voltage(),"roll":acc.roll(), "pitch": acc.pitch(), 
	"timestamp":str(getLocalTime())})
	print(payload)
	mytopic = config.TOPIC +'/'+ device_id +'/aggregate'
	pycomAwsMQTTClient.publish(mytopic, payload, 1)
	pycom.heartbeat(True)
	time.sleep(10)
	print("sleeping for 10 seconds")