import json
from types import SimpleNamespace

CONFIG_STD = {
    "General": {
        "window": {
            "fullScreen": False,
            "width": 1024,
            "height": 768,
            "startTimer": 1
        },
        "experiment": {
            "program": "Equation",
            "round": 20,
            "name": "Ivanov",
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
        "graphics": {
            "sizes": {
                "distMul": 1.5,
                "waitZone": 200,
                "radius": 40
            },
            "colors": {
                "bg": "#c0c0c0",
                "mouse": "#ff0000",
                "hole": "#000000"
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
        "delay": {
            "plus": 0.5,
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
                "squares": 100,
                "font": 15

            },
            "font": "Comic Sans"
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
print(str(CONFIG_STD))

config = json.loads(str(CONFIG_STD), object_hook=lambda d: SimpleNamespace(**d))

print(config.General.window)
