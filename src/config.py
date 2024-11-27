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
            "round": 20,
            "name": "Иванов",
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
            "lightSize": 60,
            "manualStamps": True,
            "manualStampsKey": "K_SPACE"
        }

    },
    "Mouses": {
        "graphics": {
            "sizes": {
                "distMul": 1.5,
                "waitZone": 200,
                "radius": 40,
                "speed": 8,
                "maxDispersion": 0.5
            },
            "colors": {
                "bg": "#404040",
                "mouse": "#ff0000",
                "hole": "#c0c0c0",
                "gtrail": "#0000ff",
                "strail": "#00ff00"
            }
        },
        "control": {
            "sensitivity": 20,
            "inverse": True
        },

        "logger": {
            "freq": 0.01
        },
        "timeStamps": {
        }
    },
    "Equation": {
        "duration": {
            "plus": 0.5,
            "fastAnswer": 2,
            "answer": 5
        },
        "graphics": {
            "colors": {
                "plus": "#c0c0c0",
                "bg": "#404040",
                "right": "#00ff00",
                "wrong": "#ff0000",
                "font": "#c0c0c0"
            },
            "sizes": {
                "plus": {
                    "radius": 30,
                    "width": 10
                },
                "squares": {
                    "length": 150,
                    "width": 3
                },
                "font": 150
            },
            "font": "Comic Sans"
        },
        "file": {
            "path": "None"
        },
        "control": {
            "sensitivity": 0.3,
            "inverse": True
        },
        "timeStamps": {}
    },
    "PVT": {
        "delay": {
            "plus": 0.5,
            "emptyMin": 1.5,
            "emptyMax": 3,
            "answer": 3,
            "msi": 0.5
        },
        "graphics": {
            "color": {
                "bg": "#404040",
                "plus": "#c0c0c0",
                "circle": "#ff0000"
            },
            "size": {
                "circleRadius": 40,
                "plus": {
                    "radius": 30,
                    "width": 10
                }
            },
        },
        "timeStamps": {}
    },
    "Control": {
        "delay": {
            "plus": 120,
        },
        "graphics": {
            "color": {
                "bg": "#404040",
                "plus": "#c0c0c0",
            },
            "size": {
                "plus": {
                    "radius": 30,
                    "width": 10
                }
            },
        },
        "timeStamps": {}
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
    # CONFIG = config
    with open('config.json', 'w') as configFile:
        json.dump(CONFIG, configFile, indent=4, ensure_ascii=False)


def getConfig():
    global CONFIG
    return CONFIG


def printOut():
    global CONFIG
    print(CONFIG)
