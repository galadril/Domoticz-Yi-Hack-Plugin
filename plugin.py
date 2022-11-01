#           Yi Hack Plugin
#
#           Author:     galadril, 2020
#
"""
<plugin key="YiHack" name="Yi Hack" author="galadril" version="0.0.1" wikilink="https://github.com/galadril/Domoticz-Yi-Hack-Plugin" externallink="">
    <description>
        <h2>Yi Hack Plugin</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Enable and disable Yi cameras that have the Yi Hack installed (MStar or AllWinner)</li>
        </ul>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Status, On/Off</li>
            <li>Status led, On/Off</li>
            <li>Status IR led, On/Off</li>
            <li>Save video on motion, On/Off</li>
            <li>Rotate, On/Off</li>
            <li>Detection sensitivity, Low/Medium/High</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="0.0.0.0"/>
        <param field="Port" label="Port" width="200px" required="true" default="8080"/>
        <param field="Username" label="Username" width="200px" required="false" default=""/>
        <param field="Password" label="Password" width="200px" required="false" default=""/>
        <param field="Mode6" label="Debug" width="200px">
            <options>
                <option label="None" value="0"  default="true" />
                <option label="Python Only" value="2"/>
                <option label="Basic Debugging" value="62"/>
                <option label="Basic + Messages" value="126"/>
                <option label="Connections Only" value="16"/>
                <option label="Connections + Queue" value="144"/>
                <option label="All" value="-1"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import sys
import json
import base64

class BasePlugin:
    YiConn = None
    nextConnect = 1
    oustandingPings = 0
    
    cameraState = 0
    ledState = 0
    irState = 0
    motionState = 0
    rotateState = 0
    sensitivityState = 0
    
    sendData = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/get_configs.sh?conf=camera'}
    sendOnAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?switch_on=yes'}
    sendOffAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?switch_on=no'}
    sendOnLedAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?led=yes'}
    sendOffLedAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?led=no'}
    sendOnIRAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?ir=yes'}
    sendOffIRAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?ir=no'}
    sendOnRotateAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?rotate=yes'}
    sendOffRotateAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?rotate=no'}
    sendOnMotionAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?save_video_on_motion=yes'}
    sendOffMotionAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?save_video_on_motion=no'}
    sendSensitivityLowAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?sensitivity=low'}
    sendSensitivityMediumAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?sensitivity=medium'}
    sendSensitivityHighAction = {'Verb':'GET', 'URL':'/cgi-bin/camera_settings.sh?sensitivity=high'}
    sendAfterConnect = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/get_configs.sh?conf=camera'}
    
    encoded_credentials = ''
    basicAuth = ''
        
    def onStart(self):
        if Parameters["Mode6"] != "0":
            Domoticz.Debugging(int(Parameters["Mode6"]))
            DumpConfigToLog()

        if (len(Devices) == 0):
            Domoticz.Device(Name="Status",  Unit=1, TypeName="Switch").Create()
            Domoticz.Device(Name="Led",  Unit=2, TypeName="Switch").Create()
            Domoticz.Device(Name="IR Led",  Unit=3, TypeName="Switch").Create()
            Domoticz.Device(Name="Rotate",  Unit=4, TypeName="Switch").Create()
            Domoticz.Device(Name="Save video on motion", Unit=5, TypeName="Switch").Create()
            Domoticz.Device(Name="Detection sensitivity",  Unit=6, TypeName="Selector Switch", Options={"LevelActions": "0|10|20|30", "LevelNames": "Off|Low|Medium|High", "LevelOffHidden": "true"}).Create()
            Domoticz.Log("Devices created.")
        if (1 in Devices):
            self.cameraState = Devices[1].nValue
            
        credentials = ('%s:%s' % (Parameters["Username"], Parameters["Password"]))
        encoded_credentials = base64.b64encode(credentials.encode('ascii'))
        basicAuth = 'Basic %s' % encoded_credentials.decode("ascii")
        
        sendData = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/get_configs.sh?conf=camera', 'Headers' : {'Authorization': basicAuth}}
        sendOnAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?switch_on=yes', 'Headers' : {'Authorization': basicAuth}}
        sendOffAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?switch_on=no', 'Headers' : {'Authorization': basicAuth}}
        sendOnLedAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?led=yes', 'Headers' : {'Authorization': basicAuth}}
        sendOffLedAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?led=no', 'Headers' : {'Authorization': basicAuth}}
        sendOnIRAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?ir=yes', 'Headers' : {'Authorization': basicAuth}}
        sendOffIRAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?ir=no', 'Headers' : {'Authorization': basicAuth}}
        sendOnRotateAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?rotate=yes', 'Headers' : {'Authorization': basicAuth}}
        sendOffRotateAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?rotate=no', 'Headers' : {'Authorization': basicAuth}}
        sendOnMotionAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?save_video_on_motion=yes', 'Headers' : {'Authorization': basicAuth}}
        sendOffMotionAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?save_video_on_motion=no', 'Headers' : {'Authorization': basicAuth}}
        sendSensitivityLowAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?sensitivity=low', 'Headers' : {'Authorization': basicAuth}}
        sendSensitivityMediumAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?sensitivity=medium', 'Headers' : {'Authorization': basicAuth}}
        sendSensitivityHighAction = { 'Verb' : 'GET', 'URL'  : '/cgi-bin/camera_settings.sh?sensitivity=high', 'Headers' : {'Authorization': basicAuth}}
        
        Domoticz.Debug("Set basic auth to: "+basicAuth)
        sendAfterConnect = sendData
        
        self.YiConn = Domoticz.Connection(Name="YiConn", Transport="TCP/IP", Protocol="HTTP", Address=Parameters["Address"], Port=Parameters["Port"])
        self.YiConn.Connect()
        
        for Device in Devices:
            UpdateDevice(Device, Devices[Device].nValue, Devices[Device].sValue, 1)
            
        Domoticz.Heartbeat(10)
        return True
        
    def onConnect(self, Connection, Status, Description):
        if (Status == 0):
            Domoticz.Log("Connected successfully to: "+Connection.Address+":"+Connection.Port)
            if (1 in Devices):
                self.cameraState = Devices[1].nValue
            self.YiConn.Send(self.sendAfterConnect)
        else:
            Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Connection.Address+":"+Connection.Port)
            Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Connection.Address+":"+Connection.Port+" with error: "+Description)
            for Key in Devices:
                UpdateDevice(Key, 0, Devices[Key].sValue, 1)
        return True

    def onMessage(self, Connection, Data):
        try:
            Response = json.loads(Data["Data"])
            DumpJSONResponseToLog(Response)
        
            if ('SWITCH_ON' in Response):
                if (Response["SWITCH_ON"] == 'yes'):
                    self.cameraState = 1
                else:
                    self.cameraState = 0
                UpdateDevice(1, self.cameraState, '', 0)
                
            if ('LED' in Response):
                if (Response["LED"] == 'yes'):
                    self.ledState = 1
                else:
                    self.ledState = 0
                UpdateDevice(2, self.ledState, '', 0)
                
            if ('LED' in Response):
                if (Response["LED"] == 'yes'):
                    self.irState = 1
                else:
                    self.irState = 0
                UpdateDevice(3, self.irState, '', 0)
            
            if ('ROTATE' in Response):
                if (Response["ROTATE"] == 'yes'):
                    self.rotateState = 1
                else:
                    self.rotateState = 0
                UpdateDevice(4, self.rotateState, '', 0)
                
            if ('SAVE_VIDEO_ON_MOTION' in Response):
                if (Response["SAVE_VIDEO_ON_MOTION"] == 'yes'):
                    self.motionState = 1
                else:
                    self.motionState = 0
                UpdateDevice(5, self.motionState, '', 0)
                
            if ('SENSITIVITY' in Response): 
                if (Response["SENSITIVITY"] == 'low'):
                    self.sensitivityState = 10
                    UpdateDevice(6, self.sensitivityState, 'Low', 0)
                elif (Response["SENSITIVITY"] == 'medium'):
                    self.sensitivityState = 20
                    UpdateDevice(6, self.sensitivityState, 'Medium', 0)
                else:
                    self.sensitivityState = 30
                    UpdateDevice(6, self.sensitivityState, 'High', 0)
                
        except: 
            Domoticz.Log("No json payload received.")
            
        return True

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + ", Connected: " + str(self.YiConn.Connected()))

        Command = Command.strip()
        action, sep, params = Command.partition(' ')
        action = action.capitalize()

        if (str(Unit) == '1'):
            if (action == 'On'):
                self.cameraState = 1;
                self.sendAfterConnect = self.sendOnAction
            else:
                self.cameraState = 0;
                self.sendAfterConnect = self.sendOffAction
        elif (str(Unit) == '2'):
            if (action == 'On'):
                self.ledState = 1;
                self.sendAfterConnect = self.sendOnLedAction
            else:
                self.ledState = 0;
                self.sendAfterConnect = self.sendOffLedAction
                
        elif (str(Unit) == '3'):
            if (action == 'On'):
                self.irState = 1;
                self.sendAfterConnect = self.sendOnIRAction
            else:
                self.irState = 0;
                self.sendAfterConnect = self.sendOffIRAction
                
        elif (str(Unit) == '4'):
            if (action == 'On'):
                self.rotateState = 1;
                self.sendAfterConnect = self.sendOnRotateAction
            else:
                self.rotateState = 0;
                self.sendAfterConnect = self.sendOffRotateAction
                
        elif (str(Unit) == '5'):
            if (action == 'On'):
                self.motionState = 1;
                self.sendAfterConnect = self.sendOnMotionAction
            else:
                self.motionState = 0;
                self.sendAfterConnect = self.sendOffMotionAction
                
        elif (str(Unit) == '6'):
            self.sensitivityState = Level;
            if (Level == 10):
                self.sendAfterConnect = self.sendSensitivityLowAction
            elif (Level == 20):
                self.sendAfterConnect = self.sendSensitivityMediumAction
            else: 
                self.sendAfterConnect = self.sendSensitivityHighAction
                
        if (self.YiConn.Connected() == False):
            self.YiConn.Connect()
        else:
            self.YiConn.Send(self.sendAfterConnect)
        
        return True

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)
        return

    def onHeartbeat(self):
        try:
            if (self.YiConn.Connected()):
                if (self.oustandingPings > 3):
                    self.YiConn.Disconnect()
                    self.nextConnect = 0
                else:
                    self.YiConn.Send(self.sendData)
                    self.oustandingPings = self.oustandingPings + 1
            else:
                # if not connected try and reconnected every 3 heartbeats
                self.oustandingPings = 0
                self.nextConnect = self.nextConnect - 1
                self.sendAfterConnect = self.sendData
                if (self.nextConnect <= 0):
                    self.nextConnect = 1
                    self.YiConn.Connect()
            return True
        except:
            Domoticz.Log("Unhandled exception in onHeartbeat, forcing disconnect.")
            self.onDisconnect(self.YiConn)
            self.YiConn = None
        
    def onDisconnect(self, Connection):
        Domoticz.Log("Device has disconnected")
        return

    def onStop(self):
        Domoticz.Log("onStop called")
        return True

    def TurnOn(self):
        self.YiConn.Send(self.sendOnAction)
        return

    def TurnOff(self):
        self.YiConn.Send(self.sendOffAction)
        return

    def ClearDevices(self):
        # Stop everything and make sure things are synced
        self.cameraState = 0
        self.SyncDevices(0)
        return
        
global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Settings count: " + str(len(Settings)))
    for x in Settings:
        Domoticz.Debug( "'" + x + "':'" + str(Settings[x]) + "'")
    for x in Images:
        Domoticz.Debug( "'" + x + "':'" + str(Images[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def DumpJSONResponseToLog(jsonDict):
    if isinstance(jsonDict, dict):
        Domoticz.Log("JSON Response Details ("+str(len(jsonDict))+"):")
        for x in jsonDict:
            if isinstance(jsonDict[x], dict):
                Domoticz.Log("--->'"+x+" ("+str(len(jsonDict[x]))+"):")
                for y in jsonDict[x]:
                    Domoticz.Log("------->'" + y + "':'" + str(jsonDict[x][y]) + "'")
            else:
                Domoticz.Log("--->'" + x + "':'" + str(jsonDict[x]) + "'")

def UpdateDevice(Unit, nValue, sValue, TimedOut):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it 
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue) or (Devices[Unit].TimedOut != TimedOut):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue), TimedOut=TimedOut)
            Domoticz.Log("Update "+str(nValue)+":'"+str(sValue)+"' ("+Devices[Unit].Name+")")
    return

# Synchronise images to match parameter in hardware page
def UpdateImage(Unit):
    if (Unit in Devices) and (Parameters["Mode1"] in Images):
        Domoticz.Debug("Device Image update: '" + Parameters["Mode1"] + "', Currently "+str(Devices[Unit].Image)+", should be "+str( Images[Parameters["Mode1"]].ID))
        if (Devices[Unit].Image != Images[Parameters["Mode1"]].ID):
            Devices[Unit].Update(nValue=Devices[Unit].nValue, sValue=str(Devices[Unit].sValue), Image=Images[Parameters["Mode1"]].ID)
    return
