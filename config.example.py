
# wifi configuration
WIFI_SSID =  'WIFI'
WIFI_PASS = 'WIFI password'

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'example.us-east-1.amazonaws.com'
AWS_ROOT_CA = '/flash/cert/AmazonRootCA1.pem' 
AWS_CLIENT_CERT = '/flash/cert/certificate.pem.crt'
AWS_PRIVATE_KEY = '/flash/cert/private.pem.key'

################## Subscribe / Publish client #################
CLIENT_ID = 'Morad_pycom'
TOPIC = 'PycomMorad'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'PycomMorad'
LAST_WILL_MSG = 'To All: Last will message'

####################### Shadow updater ########################
THING_NAME = "Morad_PyCOM" #"my thing name"
CLIENT_ID = "ShadowUpdater"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5

# ####################### Delta Listener ########################
THING_NAME = "Morad_PyCOM"#"my thing name"
CLIENT_ID = "DeltaListener"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5

# ####################### Shadow Echo ########################
THING_NAME = "Morad_PyCOM"#"my thing name"
CLIENT_ID = "ShadowEcho"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
