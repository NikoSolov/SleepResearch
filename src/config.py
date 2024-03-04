import json
import os

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

        "siren": {
            "enable": True,
            "freq": 440,
            "volume": 4096,
            "duration": 1.5
        },
        "timeStamps": {
            "trigger": True,
            "light": True,
            "lightSize": 20
        }

    },
    "Mouse": {
        "graphics": {
            "sizes": {
                "distMul": 1.5,
                "waitZone": 200,
                "radius": 40,
                "speed": 10,
                "maxDispersion": 0.5
            },
            "colors": {
                "bg": "#c0c0c0",
                "mouse": "#ff0000",
                "hole": "#000000",
                "gtrail": "#0000ff",
                "strail": "#00ff00"
            }
        },
        "control": {
            "sensitivity": 20,
            "inverse": False
        },

        "logger": {
            "freq": 0.25
        },
        "timeStamps": {
        }
    },
    "Equation": {
        "duration": {
            "plus": 0.5,
            "fastAnswer": 2.5,
            "answer": 5
        },
        "graphics": {
            "colors": {
                "plus": "#808080",
                "bg": "#c0c0c0",
                "right": "#00ff00",
                "wrong": "#0000ff",
                "font": "#ffffff"
            },
            "sizes": {
                "plus": {
                    "radius": 15,
                    "width": 2
                },
                "squares":
                    {
                        "length": 100,
                        "width": 0
                    },
                "font": 15

            },
            "font": "Comic Sans"
        },
        "file": {
            "path": "None"
        },
        "control": {
            "sensitivity": 0.5,
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
