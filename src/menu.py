import tkinter as tk
import ctypes
from tkinter import ttk, filedialog
import config as cfg

user32 = ctypes.windll.user32
displaySize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

cfg.loadConfig()
config = cfg.getConfig()
print(config)

root = tk.Tk()
root.resizable(False, False)
root.title('Окно конфигураций')
root.minsize(120, 120)

valueFrames = {
    "general":
        {
            "window": {
                "fullScreen": tk.BooleanVar(),
                "width": tk.IntVar(),
                "height": tk.IntVar(),
                "startTimer": tk.IntVar()
            },
            "tone": {
                "enable": tk.BooleanVar(),
                "freq": tk.IntVar(),
                "volume": tk.IntVar(),
                "delay": tk.DoubleVar()
            },
            "experiment": {
                "program": tk.StringVar(),
                "round": tk.IntVar(),
                "name": tk.StringVar(),
                "code": tk.StringVar()
            },
            "timeStamps": {
                "trigger": tk.BooleanVar(),
                "light": tk.BooleanVar(),
                "lightSize": tk.IntVar()
            }
        },
    "Mouse":
        {
            "control": {
                "inverse": tk.BooleanVar(),
                "sensitivity": tk.IntVar()
            },
            "zoneSize": {
                "distMul": tk.DoubleVar(),
                "waitZone": tk.IntVar(),
                "radius": tk.IntVar()
            },
            "logger": {
                "freq": tk.DoubleVar()
            },
            "timeStamps": {

            }
        },
    "Equation":
        {
            "control": {
                "inverse": tk.BooleanVar(),
                "sensitivity": tk.IntVar()
            },
            "file": {
                "path": tk.StringVar()
            },
            "delay": {
                "plus": tk.DoubleVar(),
                "answer": tk.DoubleVar()
            },
            "timeStamps": {

            }
        },
    "PVT":
        {
            "delay": {
                "plus": tk.DoubleVar(),
                "emptyMin": tk.DoubleVar(),
                "emptyMax": tk.DoubleVar(),
                "answer": tk.DoubleVar(),
                "msi": tk.DoubleVar()
            },
            "timeStamps": {
            
            }
        }
}
programList = ["Mouse", "Equation", "PVT"]

def selectFile():
    filetypes = (('.txt файлы', '*.txt'), ('Все файлы', '*.*'))
    file = filedialog.askopenfilename(title='Выберите файл', initialdir='/', filetypes=filetypes)
    print(file)
    if file == "":
        valueFrames["Equation"]["file"]["path"].set("None")
    else:
        valueFrames["Equation"]["file"]["path"].set(file)



class CountdownButton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 10  # starting count
        self.configure(command=self.start_countdown)

    def countdown(self):
        if self.count > 0:
            self.count -= 1
            self.configure(text=f"Get Ready...{self.count}")
            self.after(1000, self.countdown)  # repeat after 1 second
        else:
            root.destroy()

    def start_countdown(self):
        global config
        self.configure(state="disabled")  # Disable the button to prevent multiple clicks
        # -------------------
        update_dict_values(config, valueFrames)
        cfg.updateConfig(cfg.getConfig())
        self.count = valueFrames["general"]["window"]["startTimer"].get()
        # -------------------
        self.countdown()


def update_dict_values(dict1, dict2):
    for key, value in dict1.items():
        if key in dict2:
            if isinstance(value, dict) and isinstance(dict2[key], dict):
                update_dict_values(value, dict2[key])
            else:
                if type(dict1[key]) in [tk.IntVar, tk.BooleanVar, tk.StringVar, tk.DoubleVar]:
                    dict1[key].set(dict2[key])
                else:
                    dict1[key] = dict2[key].get()
    return dict1


update_dict_values(valueFrames, config)
print(valueFrames["Equation"]["delay"]["plus"].get())

toneState = "normal"

# ======== versatile ===========
nb = ttk.Notebook(root)
nb.grid(row=0)
startButton = (CountdownButton(
    root,
    text="Start Experiment",
    relief="raised"))
startButton.grid(row=1, sticky="NEWS")
# ======== general tab ===========
generalTab = ttk.Frame(nb)
generalTab.grid()
nb.add(generalTab, text="General")
# --------- window LabelFrame -----------
windowFrame = tk.LabelFrame(generalTab, text="Window")
windowFrame.grid(column=0, row=0, sticky="news")

tk.Label(windowFrame, text="Full Screen").grid(column=0, row=0)
tk.Label(windowFrame, text="Width").grid(column=0, row=1)
tk.Label(windowFrame, text="Height").grid(column=0, row=2)
tk.Label(windowFrame, text="Start Timer").grid(column=0, row=3)

(tk.Checkbutton(
    windowFrame,
    variable=valueFrames["general"]["window"]["fullScreen"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    windowFrame,
    textvariable=valueFrames["general"]["window"]["width"],
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Spinbox(windowFrame, textvariable=valueFrames["general"]["window"]["height"], from_=0, to=20000)
 .grid(column=1, row=2))
(tk.Spinbox(windowFrame, textvariable=valueFrames["general"]["window"]["startTimer"], from_=0, to=20000)
 .grid(column=1, row=3))
# ---------- tone LabelFrame ----------------
toneFrame = tk.LabelFrame(generalTab, text="Tone")
toneFrame.grid(column=1, row=0, sticky="news")
tk.Label(toneFrame, text="Enable").grid(column=0, row=0)
tk.Label(toneFrame, text="Freq").grid(column=0, row=1)
tk.Label(toneFrame, text="Volume").grid(column=0, row=2)
tk.Label(toneFrame, text="Delay").grid(column=0, row=3)
(tk.Checkbutton(
    toneFrame,
    variable=valueFrames["general"]["tone"]["enable"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    toneFrame,
    textvariable=valueFrames["general"]["tone"]["freq"],
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Spinbox(
    toneFrame,
    textvariable=valueFrames["general"]["tone"]["volume"],
    from_=0, to=20000)
 .grid(column=1, row=2))
(tk.Spinbox(
    toneFrame,
    textvariable=valueFrames["general"]["tone"]["delay"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=3))
# ---------- experiment ----------------
experimentFrame = tk.LabelFrame(generalTab, text="Experiments")
experimentFrame.grid(column=0, row=1, sticky="news")
tk.Label(experimentFrame, text="Program").grid(column=0, row=0)
tk.Label(experimentFrame, text="Num. Rounds").grid(column=0, row=1)
tk.Label(experimentFrame, text="Name").grid(column=0, row=2)
tk.Label(experimentFrame, text="Code").grid(column=0, row=3)

(tk.OptionMenu(
    experimentFrame,
    valueFrames["general"]["experiment"]["program"],
    *programList)
 .grid(column=1, row=0))
(tk.Spinbox(
    experimentFrame,
    textvariable=valueFrames["general"]["experiment"]["round"],
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Entry(
    experimentFrame,
    textvariable=valueFrames["general"]["experiment"]["name"])
 .grid(column=1, row=2))
(tk.Entry(
    experimentFrame,
    textvariable=valueFrames["general"]["experiment"]["code"])
 .grid(column=1, row=3))
# ---------- experiment ----------------
timeStampsFrame = tk.LabelFrame(generalTab, text="TimeStamp")
timeStampsFrame.grid(column=1, row=1, sticky="news")
tk.Label(timeStampsFrame, text="Trigger").grid(column=0, row=0)
tk.Label(timeStampsFrame, text="Light Sensor").grid(column=0, row=1)
tk.Label(timeStampsFrame, text="Light Size  ").grid(column=0, row=2)
(tk.Checkbutton(
    timeStampsFrame,
    variable=valueFrames["general"]["timeStamps"]["trigger"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Checkbutton(
    timeStampsFrame,
    variable=valueFrames["general"]["timeStamps"]["light"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=1))
(tk.Spinbox(
    timeStampsFrame,
    textvariable=valueFrames["general"]["timeStamps"]["lightSize"],
    from_=0, to=20000)
 .grid(column=1, row=2))
# ======== Mouse Tab =======================
mouseTab = ttk.Frame(nb)
mouseTab.grid()
nb.add(mouseTab, text="Mouse")
# ------- controlFrame ---------------------
controlFrame = tk.LabelFrame(mouseTab, text="Control")
controlFrame.grid(column=0, row=0, sticky="news")
tk.Label(controlFrame, text="Inverse").grid(column=0, row=0)
tk.Label(controlFrame, text="Sensitivity").grid(column=0, row=1)
(tk.Checkbutton(
    controlFrame,
    variable=valueFrames["Mouse"]["control"]["inverse"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    controlFrame,
    textvariable=valueFrames["Mouse"]["control"]["sensitivity"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# ----------- loggerFrame --------------------
loggerFrame = tk.LabelFrame(mouseTab, text="Logger")
loggerFrame.grid(column=0, row=1, sticky="news")
tk.Label(loggerFrame, text="Frequency").grid(column=0, row=0)
(tk.Spinbox(
    loggerFrame,
    textvariable=valueFrames["Mouse"]["logger"]["freq"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
# ----------- zoneSize --------------------
zoneSize = tk.LabelFrame(mouseTab, text="Zone Sizes")
zoneSize.grid(column=1, row=0, sticky="news")
tk.Label(zoneSize, text="Distance Multiplier").grid(column=0, row=0)
tk.Label(zoneSize, text="Disability Zone").grid(column=0, row=1)
(tk.Spinbox(
    zoneSize,
    textvariable=valueFrames["Mouse"]["zoneSize"]["distMul"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    zoneSize,
    textvariable=valueFrames["Mouse"]["zoneSize"]["waitZone"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# --------- TimeStamps
timeStampsFrame = tk.LabelFrame(mouseTab, text="TimeStamps")
timeStampsFrame.grid(column=1, row=1, sticky="news")
tk.Label(timeStampsFrame, text="Start Round").grid(column=0, row=0)
tk.Label(timeStampsFrame, text="First Reaction").grid(column=0, row=1)
# ======= Equation Tab =====================
equationTab = ttk.Frame(nb)
equationTab.grid()
nb.add(equationTab, text="Equation")
# ------- controlFrame ---------------------
controlFrame = tk.LabelFrame(equationTab, text="Control")
controlFrame.grid(column=0, row=0, sticky="news")
tk.Label(controlFrame, text="Inverse").grid(column=0, row=0)
tk.Label(controlFrame, text="Sensitivity").grid(column=0, row=1)
(tk.Checkbutton(
    controlFrame,
    variable=valueFrames["Equation"]["control"]["inverse"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    controlFrame,
    textvariable=valueFrames["Equation"]["control"]["sensitivity"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# ----------- timeDelays --------------------
delayFrame = tk.LabelFrame(equationTab, text="Time Delays")
delayFrame.grid(column=0, row=1, sticky="news")
tk.Label(delayFrame, text="Plus Time").grid(column=0, row=0)
tk.Label(delayFrame, text="Answer Time").grid(column=0, row=1)
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["Equation"]["delay"]["plus"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["Equation"]["delay"]["answer"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=1))
# ----------- fileChoice --------------------
fileChoice = tk.LabelFrame(equationTab, text="File Choice")
fileChoice.grid(column=1, row=0, sticky="news")
tk.Label(fileChoice, text="Choose File:").grid(column=0, row=0)
(tk.Button(
    fileChoice,
    textvariable=valueFrames["Equation"]["file"]["path"],
    command=selectFile)
 .grid(column=1, row=0))
# --------- TimeStamps
timeStampsFrame = tk.LabelFrame(equationTab, text="TimeStamps")
timeStampsFrame.grid(column=1, row=1, sticky="news")
tk.Label(timeStampsFrame, text="Start Round").grid(column=0, row=0)
tk.Label(timeStampsFrame, text="First Reaction").grid(column=0, row=1)

# ======= PVT Tab =====================
pvtTab = ttk.Frame(nb)
pvtTab.grid()
nb.add(pvtTab, text="PVT")
# ---- timeDelays ---------------------
delayFrame = tk.LabelFrame(pvtTab, text="Time Delays")
delayFrame.grid(column=0, row=1, sticky="news")
tk.Label(delayFrame, text="Plus Time").grid(column=0, row=0)
tk.Label(delayFrame, text="Empty Min").grid(column=0, row=1)
tk.Label(delayFrame, text="Empty Max").grid(column=0, row=2)
tk.Label(delayFrame, text="Answer Time").grid(column=0, row=3)
tk.Label(delayFrame, text="MSI").grid(column=0, row=4)
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["PVT"]["delay"]["plus"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["PVT"]["delay"]["emptyMin"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["PVT"]["delay"]["emptyMax"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=2))
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["PVT"]["delay"]["answer"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=3))
(tk.Spinbox(
    delayFrame,
    textvariable=valueFrames["PVT"]["delay"]["msi"],
    increment= 0.1,
    from_=0, to=20000)
 .grid(column=1, row=4))

root.mainloop()
