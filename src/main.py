import menu

import config as cfg

cfg.loadConfig()
config = cfg.getConfig()

PROGRAM = config["general"]["experiment"]["program"]

match PROGRAM:
    case "Mouses":
        import Mouses
    case "Tasks":
        import Tasks
    case "PVT":
        import PVT
    case "Control":
        import Control