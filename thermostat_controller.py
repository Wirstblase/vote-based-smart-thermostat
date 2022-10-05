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

temp_setting_ref = store.collection("temp-setting").document(u'user4')
thermo_cmd_ref = store.collection("thermoCmd").document("thermostat1")
settdoc = temp_setting_ref.get()
settdocdict = settdoc.to_dict()
thermodoc = thermo_cmd_ref.get()
thermodocdict = thermodoc.to_dict()

name = settdocdict["name"]
currentTemp = thermodocdict["lastTemp"]
currentTempPreference = settdocdict["temp"]
lastUpdate = thermodocdict["lastTime"]
sensorLocation = thermodocdict["location"]
statuss = thermodocdict["cmd"]

print("copyright ⓒ 2022 s00flea engineering")
print("")
print(f"welcome, {name}")
print("")
print(f"the temperature was last updated on {lastUpdate}, \nmeasured by temp_sensor_1 located in {sensorLocation}")
print("")
print(f"the current temperature is: {currentTemp} degrees ")
print(f"your personal preference is: {currentTempPreference} degrees ")
print(f"the heater is currently: {statuss}")
print("")
print("in case of great discrepancy, please consult to the other members")
print("-------------------")
opt = input("do you wish to adjust your preference? (yes/no) - ")
if("yes" in opt):
    newTemp = input("please state your desired temperature - ")
    newTempFloat = 0
    try:
        newTempFloat = float(newTemp)
        if(newTempFloat > float(26)):
            print("don't exaggerate it! the council knows")
            print("temperature is now set to the max limit of 26 degrees")
            newTempFloat = float(26)
        if(newTempFloat < float(15)):
            print("don't exaggerate it! the council knows")
            print("temperature is now set to the min limit of 15 degrees")
            newTempFloat = float(15)

        temp_setting_ref.update({u'temp':unicode(str(newTempFloat))})
        print("your preference has been updated!")
        print("have a pleasant day")
    except:
        print("temperature must be a number like 19.50")
elif("no" in opt):
    print("have a pleasant day")
else:
    print("command invalid, wasting the AI's time is a punishable crime :0")
    sleep(3)
    print("the council will be informed.")
    sleep(10)
    print("have a pleasant day")
        

