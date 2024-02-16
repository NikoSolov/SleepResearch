import os
import json

# Standard configurations
CONFIG_STD = {
    "general": {
        "window": {
            "fullScreen": False,
            "width": 1024,
            "height": 768,
            "startTimer": 1
        },
        "experiment": {
            "program": "Equation",
            "round": 20,
            "name": "Иванов",
            "code": "1234",
        },

        "tone": {
            "enable": True,
            "freq": 440,
            "volume": 4096,
            "delay": 1.5
        },
        "timeStamps": {
            "trigger": False,
            "light": True,
            "lightSize": 20
        }

    },
    "Mouse": {
        "zoneSize": {
            "distMul": 1.5,
            "waitZone": 200,
            "radius": 40
        },
        "colors": {
            "bg": "#c0c0c0",
            "mouse": "#ff0000",
            "hole": "#000000"
        },
        "logger": {
            "freq": 0.25
        },
        "control": {
            "sensitivity": 20,
            "inverse": False
        },
        "timeStamps": {
        }
    },
    "Equation": {
        "delay": {
            "plus": 0.5,
            "answer": 5
        },
        "colors": {
            "bg": "#c0c0c0",
            "right": "#00ff00",
            "wrong": "#0000ff",
            "text": "#ffffff"
        },
        "file": {
            "path": "None"
        },
        "control": {
            "sensitivity": 20,
            "inverse": False
        },
        "timeStamps": {
        }
    },
    "PVT": {
        "delay": {
            "plus": 0.5,
            "emptyMin": 2,
            "emptyMax": 4,
            "answer": 5,
            "msi": 0.5
        },
        "color": {
            "bg": "#404040",
            "plus": "#808080",
            "circle": "#808080"
        },
        "size": {
            "circleRadius": 25,
            "plus": {
                "radius": 15,
                "width": 2
            }
        },
        "timeStamps": {
        }
    }
}

CONFIG = {}


# ------------------------------------------

def loadConfig():
    global CONFIG_STD, CONFIG
    # if "config" file doesn't exist, need to create them from standard set
    if os.path.exists("config.json"):
        print("config exists")
        with open('config.json', 'r') as configFile:
            updateConfig(json.load(configFile))
    else:
        updateConfig(CONFIG_STD)
    # ---------------------------------------------------------------------------------------


def updateConfig(config: dict):
    global CONFIG
    print(f"Change to: {config}")
    CONFIG.update(config)
    with open('config.json', 'w') as configFile:
        json.dump(CONFIG, configFile, indent=4, ensure_ascii=False)


def getConfig():
    global CONFIG
    return CONFIG


def printOut():
    global CONFIG
    print(CONFIG)
