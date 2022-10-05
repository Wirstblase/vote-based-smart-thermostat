import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore, storage
import _thread
from datetime import datetime
from time import sleep

import sys
if sys.version_info.major == 3:
    unicode = str

cred = credentials.Certificate("./smart-thermostat-9fefa-firebase-adminsdk-ogs5j-163abf5b65.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()

temp_setting_ref = store.collection("temp-setting")
thermo_cmd_ref = store.collection("thermoCmd")
settings_ref = store.collection("settings")

relayUpdateInterval = 30 #30 seconds - default value

print("thermostat running")

tempSettingAverage = float(0)

def updateUpdateInterval():
    doc = settings_ref.document(u'thermostat1').get()
    docdict = doc.to_dict()
    updateInterval = docdict["updateInterval"]
    global relayUpdateInterval
    relayUpdateInterval = int(updateInterval)

def getThermoSetting():
    docs = temp_setting_ref.where("name", ">", '0').stream()
    i=0
    avg=float(0)
    for doc in docs:
        #print(f'{doc.id} => {doc.to_dict()}')
        i=i+1
        temp = doc.to_dict()["temp"]
        #print(temp)
        if(float(temp) > float(26)):
            temp = "26"
            print("temp vote too big, automatically bounded to 26")
        elif(float(temp) < float(15)):
            temp = "15"
            print("temp vote too low, automatically bounded to 15")
        avg = avg + float(temp)

    avg = avg / float(i)
    global tempSettingAverage
    tempSettingAverage = avg
    print(f'tempSettingAverage: {tempSettingAverage}')


def getTempFromDHT():
    #IMPLEMENT THINGIE
    return(float(22))

def update_relay():
    #updates the document that drives the relay
    
    status = "off"
    temp = float(getTempFromDHT())
    if(temp < tempSettingAverage-0.5):
        status = "on"
    if(temp > tempSettingAverage+0.5):
        status = "off"
    now = datetime.now()
    timestamp= now.strftime("%d/%m/%Y %H:%M:%S")
    
    thermo_cmd_ref.document(u'thermostat1').update({
    u'cmd': unicode(status),
    u'lastTemp': unicode(str(temp)),
    u'lastTime':unicode(str(timestamp))
    })

    print(f"temp updated, heating {status}")


updateUpdateInterval()
print(f"refreshing ever {relayUpdateInterval} seconds")
while True:
    sleep(relayUpdateInterval)
    getThermoSetting()
    update_relay()
