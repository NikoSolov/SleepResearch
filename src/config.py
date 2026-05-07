import json
import os

# Standard configurations
CONFIG_STD = {
    "general": {
        "window": {
            "fullScreen": False,
            "width": 1024,
            "height": 768,
            "startTimer": 5
        },
        "experiment": {
            "program": "Mouses",
            "name": "Subject",
            "code": "1234",
        },
        "alarm": {
            "enable": True,
            "freq": 440,
            "volume": 4096,
            "duration": 1.5
        },
        "timeStamps": {
            "trigger": True,
            "light": True,
            "lightSize": 60
        },
        "graphics": {
            "sizes": {
                "plus": {
                    "radius": 30,
                    "width": 10
                },
            },
            "colors": {
                "plus": "#c0c0c0",
                "bg": "#404040"
            }
        },
        "control": {
            "inverse": True
        }
    },
    "Mouses": {
        "duration": {
            "plus": 5.0,
        },
        "experiment":{
            "countInGroup": 3,
            "countOfGroup": 2
        },
        "graphics": {
            "sizes": {
                "distMul": 1.5,
                "waitZone": 200,
                "radius": 40,
                "speed": 8,
                "maxDispersion": 0.5,
                "minDispersion": 0.0
            },
            "colors": {
                "mouse": "#ff0000",
                "hole": "#c0c0c0",
                "gtrail": "#0000ff",
                "strail": "#00ff00"
            }
        },
        "control": {
            "sensitivity": 20,
        },

        "logger": {
            "freq": 0.01
        },
    },
    "Equation": {
        "experiment" : {
            "round" : 20,
            "fileMode": False,
            "filePath": "None",
            "generatedTermCount": 4
        },
        "duration": {
            "plus": 0.5,
            "fastAnswer": 2.0,
            "answer": 5.0,
            "term": 1.0,
            "pause": 0.5
        },
        "graphics": {
            "colors": {
                "right": "#00ff00",
                "wrong": "#ff0000",
                "font": "#c0c0c0"
            },
            "sizes": {
                "squares": {
                    "length": 150,
                    "width": 3
                },
                "font": 150
            },
            "font": "Comic Sans"
        },
        "control": {
            "sensitivity": 0.3,
        }
    },
    "PVT": {
        "experiment" : {
            "round" : 20
        },
        "delay": {
            "plus": 0.5,
            "emptyMin": 1.5,
            "emptyMax": 3,
            "answer": 3,
            "msi": 0.5
        },
        "graphics": {
            "colors": {
                "circle": "#ff0000"
            },
            "sizes": {
                "circleRadius": 40,
            },
        }
    },
    "Control": {
        "delay": {
            "plus": 120,
        }
    }
}

CURRENT_CONFIG = {}


def loadConfig():
    global CONFIG_STD, CURRENT_CONFIG
    # if "config" file doesn't exist, need to create them from standard set
    if os.path.exists("config.json"):
        print("config exists")
        importConfig('config.json')
    else:
        saveConfig(CONFIG_STD)
    # ---------------------------------------------------------------------------------------

def saveConfig(new_config):
    setConfig(new_config)
    exportConfig('config.json')

def importConfig(filePath):
    with open(filePath, 'r') as configFile:
        setConfig(json.load(configFile))

def exportConfig(filePath):
    print(filePath)
    with open(filePath, 'w') as configFile:
        json.dump(getConfig(), configFile, indent=4, ensure_ascii=False)


def getConfig():
    global CURRENT_CONFIG
    return CURRENT_CONFIG

def setConfig(new_config: dict):
    global CURRENT_CONFIG
    CURRENT_CONFIG.update(new_config)

def resetConfig():
    global CONFIG_STD
    saveConfig(CONFIG_STD)

def printConfig():
    global CURRENT_CONFIG
    print(CURRENT_CONFIG)