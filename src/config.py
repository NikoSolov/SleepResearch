import os
import json

# Standard configurations
CONFIG_STD = {
    "screen": "Оконный",
    "program": "Задачки",
    "control": "Обычное",
    "file": "None",
    "tone_play": 1,

    # "inverse": 0,

    "width": 1024,
    "height": 768,
    "round": 20,

    "tone_rate": 440,
    "tone_volume": 4096,
    "tone_delay": 1.5,

    "radius_multiplier": 1.5,
    "possible": 200,
    "freq": 0.25,

    "sensivity": 20,
    "dot_time": 0.5,
    "time": 5,

    "lightSize": 20
}

CONFIG = {}


# ------------------------------------------

def loadConfig():
    global CONFIG_STD, CONFIG
    # if "config" file doesn't exist, need to create them from standard set
    CONFIG = CONFIG_STD
    if os.path.exists("config.json"):
        with open('config.json', 'r') as configFile:
            updateConfig(json.load(configFile))
    # ---------------------------------------------------------------------------------------


def updateConfig(config: dict):
    global CONFIG
    CONFIG.update(config)
    with open('config.json', 'w') as configFile:
        printOut()
        json.dump(CONFIG, configFile, indent=4, ensure_ascii=False)


def getConfig():
    global CONFIG
    return CONFIG


def printOut():
    global CONFIG
    print(CONFIG)

# CONFIG.updateConfig()
