from machine import Pin
from time import sleep
import dht
import time
import network
import ufirestore
from ufirestore.json import FirebaseJson
#MICROPYTHON!!!

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect("insert ssid", "insert password")
    print("Waiting for Wi-Fi connection", end="...")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)
    print()
    
    
from firebase_auth import FirebaseAuth
auth = FirebaseAuth("insert auth token")
email = "insert email"
password = "insert password"
auth.sign_in(email,password)


acctoken = auth.session.access_token
#print("debug access token:")
#print(acctoken)
ufirestore.set_project_id("smart-thermostat-9fefa")
ufirestore.set_access_token(acctoken)

lastLastTime = ""
relay = Pin(2, Pin.OUT)
relay.value(1)

errorLed = Pin(21, Pin.OUT)
errorLed.value(0)

updateInterval = 30 #default-30s
def getUpdateInterval():
    response = ufirestore.get("settings/thermostat1", bg=False)
    doc = FirebaseJson.from_raw(response)
    if doc.exists("fields/updateInterval"):
        updint = str(doc.get("fields/updateInterval"))
        global updateInterval
        updateInterval = int(updint)
        print(f"update interval set to {updateInterval} seconds")

def runThermostat():
    response = ufirestore.get("thermoCmd/thermostat1", bg=False)
    doc = FirebaseJson.from_raw(response)
    
    global lastLastTime
    cmd = ""
    lastTime = ""
    shouldTrigger = 0

    if doc.exists("fields/cmd"):
        errorLed.value(0)
        cmd = str(doc.get("fields/cmd"))
        
    if doc.exists("fields/lastTime"):
        lastTime = str(doc.get("fields/lastTime"))
        
    if(lastTime != lastLastTime):
        if(cmd == "on"):
            shouldTrigger = 1
            
    if(shouldTrigger == 1):
        print("thermostat on")
        relay.value(0)
    else:
        print("thermostat off")
        relay.value(1)
            
    lastLastTime = lastTime
    
    global updateInterval
        
    sleep(updateInterval/2)
    
    response = ufirestore.get("test/test", bg=False) #weirdest workaround ever, daca nu las alt request random da eroare
    #the firebase library for micropython is outdated
    
    sleep(updateInterval/2)
    
    
getUpdateInterval()
while True:
    try:
        runThermostat()
    except:
        print("there is an error lol")
        print("thermostat off")
        relay.value(0)
        errorLed.value(1)
    
