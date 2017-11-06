#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import clr
import json
import logging
import os
import sys
import codecs
import urllib
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime


#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "GiganticMMR"
Website = "https://www.valhallasmostwanted.com"
Description = "!mmr (USERNAME) will grab the mmr of the username passed in"
Creator = "Derek Cody (SkrubDaNub)"
Version = "1.0.0.0"

settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
#---------------------------------------
# Set Variables
#---------------------------------------
m_Response = ""
m_Command = "!mt"
m_CooldownSeconds = 10
m_CommandPermission = "everyone"
m_CommandInfo = ""
m_URL = "https://stats.gogigantic.com/en/gigantic-careers/usersdata/?usernames%5B%5D="
m_Headers = {}

class Settings:
    #Try to load the settings from file
    def __init__(self, settingsFile = None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig',mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')
        else:
            self.OnlyLive = False
            self.Command = "!mmr"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.UseCD = True
            self.Cooldown = 0
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.NoUserFoundResponse = "{0} mmr could not be found"
            self.InvalidParameterCount = "Command not formatted properly, please try again"

    def ReloadSettings(self, data):
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return

    def SaveSettings(self, settingsFile):
        with codecs.open(settingsFile,  encoding='utf-8-sig',mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig',mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return


def Init():
    # Globals
    global MySettings
    # Load in saved settings
    MySettings = Settings(settingsFile)
    # End of Init
    return

def ReloadSettings(jsonData):
    # Globals
    global MySettings

    # Reload saved settings
    MySettings.ReloadSettings(jsonData)

    # End of ReloadSettings
    return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == MySettings.Command:
        if MySettings.OnlyLive:
            startCheck = data.IsLive()
        else:
            startCheck = True

        if(startCheck and Parent.HasPermission(data.User, MySettings.Permission, MySettings.PermissionInfo)):
            if(Parent.IsOnCooldown(ScriptName,MySettings.Command) or Parent.IsOnUserCooldown(ScriptName, MySettings.Command, data.User)):
                if MySettings.UseCD:
                    cooldownDuration = Parent.GetCooldownDuration(ScriptName,MySettings.Command)
                    usercooldownduration = Parent.GetUserCooldownDuration(ScriptName, MySettings.Command,data.user)

                    if(cooldownDuration > usercooldownDuration):
                        m_CooldownRemaining = cooldownDuration
                        Parent.SendTwitchMessage(MySettings.OnCooldown.format(data.User,m_CooldownRemaining))

                    else:
                        m_CooldownRemaining = Parent.GetUserCooldownDuration(ScriptName,MySettings.Command,data.User)
                        Parent.SendTwitchMessage(MySettings.OnUserCooldown.format(data.User,m_CooldownRemaining))

            else:
                #Do Work here
                if(data.GetParamCount() > 2):
                    Parent.SendTwitchMessage(MySettings.InvalidParameterCount.format())

                userName = data.GetParam(1)
                queryURL = m_URL + urllib.quote_plus(userName)
                data = Parent.GetRequest(queryURL, m_Headers)
                status = json.loads(data)
                if(status["status"] == 200):
                    parsed_json = json.loads(status["response"])
                    if( userName in parsed_json["data"]):
                        base10mmr = parsed_json["data"][userName]["all"]["total"]["motiga_skill"]
                        mmr = base10mmr * 100
                        Parent.SendTwitchMessage(MySettings.BaseResponse.format(userName,str(mmr)))
                    else:
                        Parent.SendTwitchMessage(MySettings.NoUserFoundResponse.format(userName))
                else:
                    Parent.SendTwitchMessage("Could not contact website please try again later")

    return
#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
 return

def UpdateSettings():
    with open(m_ConfigFile) as ConfigFile:
        MySettings.__dict__ = json.load(ConfigFile)
    return
def SetDefaults():
    """Set default settings function"""
    # Globals
    global MySettings

    # Set defaults by not supplying a settings file
    MySettings = Settings()

    # Save defaults back to file
    MySettings.Save(settingsFile)

    # End of SetDefaults
    return
