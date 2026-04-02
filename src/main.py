import config as cfg
import Mouses
import Tasks
import PVT
import Control
import MainMenu

if MainMenu.run():
    cfg.loadConfig()
    match cfg.getConfig()["general"]["experiment"]["program"]:
        case "Mouses":
            Mouses.run()
        case "Tasks":
            Tasks.run()
        case "PVT":
            PVT.run()
        case "Control":
            Control.run()