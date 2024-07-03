import ctypes
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.colorchooser import askcolor
from tkfontchooser import askfont
import config as cfg

user32 = ctypes.windll.user32
displaySize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

cfg.loadConfig()
config = cfg.getConfig()
print(config)

root = tk.Tk()
root.resizable(False, False)
root.title('Configuration window')
root.minsize(120, 120)

# <editor-fold desc="Vars">
valueFrames = {
    "general": {
        "window": {
            "fullScreen": tk.BooleanVar(),
            "width": tk.IntVar(),
            "height": tk.IntVar(),
            "startTimer": tk.IntVar()
        },
        "experiment": {
            "program": tk.StringVar(),
            "round": tk.IntVar(),
            "name": tk.StringVar(),
            "code": tk.StringVar()
        },
        "alarm": {
            "enable": tk.BooleanVar(),
            "freq": tk.IntVar(),
            "volume": tk.IntVar(),
            "duration": tk.DoubleVar()
        },
        "timeStamps": {
            "trigger": tk.BooleanVar(),
            "light": tk.BooleanVar(),
            "lightSize": tk.IntVar()
        }
    },
    "Mouses": {
        "graphics": {
            "sizes": {
                "distMul": tk.DoubleVar(),
                "waitZone": tk.IntVar(),
                "radius": tk.IntVar(),
                "speed": tk.DoubleVar(),
                "maxDispersion": tk.DoubleVar()
            },
            "colors": {
                "bg": tk.StringVar(),
                "mouse": tk.StringVar(),
                "hole": tk.StringVar(),
                "gtrail": tk.StringVar(),
                "strail": tk.StringVar()
            }
        },
        "control": {
            "sensitivity": tk.IntVar(),
            "inverse": tk.BooleanVar()
        },
        "logger": {
            "freq": tk.DoubleVar()
        },
        "timeStamps": {

        }
    },
    "Equation": {
        "graphics": {
            "colors": {
                "plus": tk.StringVar(),
                "bg": tk.StringVar(),
                "right": tk.StringVar(),
                "wrong": tk.StringVar(),
                "font": tk.StringVar()
            },
            "sizes": {
                "plus": {
                    "radius": tk.IntVar(),
                    "width": tk.IntVar()
                },
                "squares": {
                    "length": tk.IntVar(),
                    "width": tk.IntVar()
                },
                "font": tk.IntVar()
            },
            "font": tk.StringVar()
        },
        "control": {
            "sensitivity": tk.DoubleVar(),
            "inverse": tk.BooleanVar()
        },
        "file": {
            "path": tk.StringVar()
        },
        "duration": {
            "plus": tk.DoubleVar(),
            "fastAnswer": tk.DoubleVar(),
            "answer": tk.DoubleVar()
        },
        "timeStamps": {

        }
    },
    "PVT": {
        "delay": {
            "plus": tk.DoubleVar(),
            "emptyMin": tk.DoubleVar(),
            "emptyMax": tk.DoubleVar(),
            "answer": tk.DoubleVar(),
            "msi": tk.DoubleVar()
        },
        "graphics": {
            "color": {
                "bg": tk.StringVar(),
                "plus": tk.StringVar(),
                "circle": tk.StringVar()
            },
            "size": {
                "circleRadius": tk.IntVar(),
                "plus": {
                    "radius": tk.IntVar(),
                    "width": tk.IntVar()
                }
            },
        },
        "timeStamps": {}
    },
    "Control": {
        "delay": {
            "plus": tk.DoubleVar(),
        },
        "graphics": {
            "color": {
                "bg": tk.StringVar(),
                "plus": tk.StringVar(),
            },
            "size": {
                "plus": {
                    "radius": tk.IntVar(),
                    "width": tk.IntVar()
                }
            },
        },
        "timeStamps": {}
    }
}
programList = ["Mouses", "Tasks", "PVT", "Control"]


def changeColor(colorConfig, button):
    print(colorConfig)
    colors = askcolor(title="ColorsChooserPicker")
    print(colors[1])
    button.config(bg=colors[1])
    colorConfig.set(colors[1])
def changeFont(button):
    font = askfont(text="12+53=65",
                   family=valueFrames["Equation"]["graphics"]["font"].get(),
                   size=valueFrames["Equation"]["graphics"]["sizes"]["font"].get())
    button.config(text=font["family"])
    valueFrames["Equation"]["graphics"]["font"].set(font["family"])

def selectFile():
    filetypes = (('.txt файлы', '*.txt'), ('Все файлы', '*.*'))
    file = filedialog.askopenfilename(title='Выберите файл', initialdir='/',
                                      filetypes=filetypes)
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
            cfg.loadConfig()
            PROGRAM = cfg.getConfig()["general"]["experiment"]["program"]

            match PROGRAM:
                case "Mouses":
                    import Mouses
                case "Tasks":
                    import Tasks
                case "PVT":
                    import PVT
                case "Control":
                    import Control

    def start_countdown(self):
        global config
        self.configure(
            state="disabled")  # Disable the button to prevent multiple clicks
        # -------------------
        update_dict_values(config, valueFrames)
        print(config["Equation"]["graphics"]["font"])
        cfg.updateConfig(config)
        self.count = valueFrames["general"]["window"]["startTimer"].get()
        # -------------------
        self.countdown()


def update_dict_values(dict1, dict2):
    for key, value in dict1.items():
        if key in dict2:
            if isinstance(value, dict) and isinstance(dict2[key], dict):
                update_dict_values(value, dict2[key])
            else:
                if type(dict1[key]) in [tk.IntVar, tk.BooleanVar, tk.StringVar,
                                        tk.DoubleVar]:
                    dict1[key].set(dict2[key])
                else:
                    dict1[key] = dict2[key].get()
    # print(dict1)
    return dict1


# </editor-fold>

update_dict_values(valueFrames, config)

print(valueFrames["Mouses"]["graphics"]["colors"]["mouse"].get())

# ======== versatile ===========
nb = ttk.Notebook(root)
nb.grid(row=0, columnspan=3)
startButton = (CountdownButton(
    root,
    text="Start Experiment",
    relief="raised"))
startButton.grid(row=1,column=2, sticky="NEWS")
tk.Label(root, text="Программа").grid(column=0, row=1)
(tk.OptionMenu(
    root,
    valueFrames["general"]["experiment"]["program"],
    *programList)
 .grid(column=1, row=1))
# ======== general tab ===========
# <editor-fold desc="Setting General">
generalTab = ttk.Frame(nb)
generalTab.grid()
nb.add(generalTab, text="General")
# --------- window LabelFrame -----------
# <editor-fold desc="Window Frame">
windowFrame = tk.LabelFrame(generalTab, text="Параметры окна")
windowFrame.grid(column=0, row=0, sticky="news")
windowConfig = valueFrames["general"]["window"]
tk.Label(windowFrame, text="Полноэкранный?").grid(column=0, row=0)
tk.Label(windowFrame, text="Длина окна").grid(column=0, row=1)
tk.Label(windowFrame, text="Высота окна").grid(column=0, row=2)
tk.Label(windowFrame, text="Время таймера\nзапуска").grid(column=0, row=3)

(tk.Checkbutton(
    windowFrame,
    variable=windowConfig["fullScreen"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    windowFrame,
    width=5,
    textvariable=windowConfig["width"],
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Spinbox(windowFrame,
            width=5,
            textvariable=windowConfig["height"], from_=0,
            to=20000)
 .grid(column=1, row=2))
(tk.Spinbox(windowFrame,
            width=5,
            textvariable=windowConfig["startTimer"],
            from_=0, to=20000)
 .grid(column=1, row=3))
# </editor-fold>
# ---------- tone LabelFrame ----------------
# <editor-fold desc="Alarm Frame">
alarmFrame = tk.LabelFrame(generalTab, text="Будильник")
alarmFrame.grid(column=0, row=1, sticky="news")
alarmConfig = valueFrames["general"]["alarm"]
tk.Label(alarmFrame, text="Включить?").grid(column=0, row=0)
tk.Label(alarmFrame, text="Частота тона").grid(column=0, row=1)
tk.Label(alarmFrame, text="Громкость").grid(column=0, row=2)
tk.Label(alarmFrame, text="Длительность").grid(column=0, row=3)
(tk.Checkbutton(
    alarmFrame,
    variable=alarmConfig["enable"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    alarmFrame,
    width=5,
    textvariable=alarmConfig["freq"],
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Spinbox(
    alarmFrame,
    width=5,
    textvariable=alarmConfig["volume"],
    from_=0, to=20000)
 .grid(column=1, row=2))
(tk.Spinbox(
    alarmFrame,
    width=5,
    textvariable=alarmConfig["duration"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=3))
# </editor-fold>
# ---------- experiment ----------------
# <editor-fold desc="Experiment Frame">
experimentFrame = tk.LabelFrame(generalTab, text="Experiments")
experimentFrame.grid(column=1, row=0, sticky="news")
experimentConfig = valueFrames["general"]["experiment"]

tk.Label(experimentFrame, text="Кол-во раундов").grid(column=0, row=1)
tk.Label(experimentFrame, text="Имя испытуемого").grid(column=0, row=2)
tk.Label(experimentFrame, text="Код испытуемого").grid(column=0, row=3)


(tk.Spinbox(
    experimentFrame,
    width=5,
    textvariable=experimentConfig["round"],
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Entry(
    experimentFrame,
    width=10,
    textvariable=experimentConfig["name"])
 .grid(column=1, row=2))
(tk.Entry(
    experimentFrame,
    width=10,
    textvariable=experimentConfig["code"])
 .grid(column=1, row=3))
# </editor-fold>
# -------------------------------------
# <editor-fold desc="TimeStamps Frame">
timeStampsFrame = tk.LabelFrame(generalTab, text="Временные метки")
timeStampsFrame.grid(column=1, row=1, sticky="news")
timeStampsConfig = valueFrames["general"]["timeStamps"]
print(timeStampsConfig)
print(timeStampsConfig["lightSize"])
tk.Label(timeStampsFrame, text="USB-метки?").grid(column=0, row=0)
tk.Label(timeStampsFrame, text="Датчик света?").grid(column=0, row=1)
tk.Label(timeStampsFrame, text="Размер квадрата света").grid(column=0, row=2)
(tk.Checkbutton(
    timeStampsFrame,
    variable=timeStampsConfig["trigger"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Checkbutton(
    timeStampsFrame,
    variable=timeStampsConfig["light"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=1))
(tk.Spinbox(
    timeStampsFrame,
    width=5,
    textvariable=timeStampsConfig["lightSize"],
    from_=0, to=20000)
 .grid(column=1, row=2))
# </editor-fold>
# </editor-fold>
# ======== Mouse Tab =======================
# <editor-fold desc="Mouse Tab">
mouseTab = ttk.Frame(nb)
mouseTab.grid()
nb.add(mouseTab, text="Mouse")
mouseConfig = valueFrames["Mouses"]
# ------- controlFrame ---------------------
# <editor-fold desc="Control Frame">
controlFrame = tk.LabelFrame(mouseTab, text="Управление")
controlFrame.grid(column=1, row=0, sticky="news")
mouseControlConfig = mouseConfig["control"]
tk.Label(controlFrame, text="Инверсия?").grid(column=0, row=0)
tk.Label(controlFrame, text="Чуствительность\n(1 - размер квадрата)").grid(
    column=0, row=1)
(tk.Checkbutton(
    controlFrame,
    variable=mouseControlConfig["inverse"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    controlFrame,
    width=5,
    textvariable=mouseControlConfig["sensitivity"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# </editor-fold>
# ----------- loggerFrame --------------------
# <editor-fold desc="Logger Frame">
loggerFrame = tk.LabelFrame(mouseTab, text="Logger")
loggerFrame.grid(column=1, row=1, sticky="news")
tk.Label(loggerFrame, text="Frequency").grid(column=0, row=0)
(tk.Spinbox(
    loggerFrame,
    width=5,
    textvariable=mouseConfig["logger"]["freq"],
    increment=0.01,
    from_=0, to=20000)
 .grid(column=1, row=0))
# </editor-fold>
# ----------- graphics --------------------
# <editor-fold desc="Graphics">
graphics = tk.LabelFrame(mouseTab, text="Графика")
graphics.grid(column=0, row=0, rowspan=2, sticky="news")
mouseGraphics = mouseConfig["graphics"]
# <editor-fold desc="Sizes">
mouseGraphicsSizes = mouseGraphics["sizes"]
Sizes = tk.LabelFrame(graphics, text="Размеры")
Sizes.grid(column=0, row=0, sticky="news")
tk.Label(Sizes, text="Умножитель\nрастояния\n(2 -> 2 радиуса)").grid(column=0,
                                                                    row=0)
tk.Label(Sizes, text="Радиус зоны\nбездействия").grid(column=0, row=1)
tk.Label(Sizes, text="Радиусы").grid(column=0, row=2)
tk.Label(Sizes, text="Скорость мыши").grid(column=0, row=3)
tk.Label(Sizes, text="Максимальный\nразброс\n[0.07; 1)").grid(column=0, row=4)
(tk.Spinbox(
    Sizes,
    width=5,
    textvariable=mouseGraphicsSizes["distMul"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    Sizes,
    width=5,
    textvariable=mouseGraphicsSizes["waitZone"],
    from_=0, to=200)
 .grid(column=1, row=1))
(tk.Spinbox(
    Sizes,
    width=5,
    textvariable=mouseGraphicsSizes["radius"],
    from_=0, to=200)
 .grid(column=1, row=2))
(tk.Spinbox(
    Sizes,
    width=5,
    textvariable=mouseGraphicsSizes["speed"],
    from_=0, to=20)
 .grid(column=1, row=3))
(tk.Spinbox(
    Sizes,
    width=5,
    textvariable=mouseGraphicsSizes["maxDispersion"],
    increment=0.1,
    from_=0, to=0.9)
 .grid(column=1, row=4))
# </editor-fold>
# ---------------------------
# <editor-fold desc="Colors">
mouseGraphicsColors = mouseGraphics["colors"]
Colors = tk.LabelFrame(graphics, text="Цвета")
Colors.grid(column=1, row=0, sticky="news")
tk.Label(Colors, text="Фон").grid(column=0, row=0)
tk.Label(Colors, text="Мышь").grid(column=0, row=1)
tk.Label(Colors, text="Нора").grid(column=0, row=2)
tk.Label(Colors, text="Путь\nСгенерированный").grid(column=0, row=3)
tk.Label(Colors, text="Путь\nИспытуемого").grid(column=0, row=4)

mouseBG = tk.Button(Colors,
                    text="***", fg="white",
                    bg=mouseGraphicsColors["bg"].get(),
                    command=lambda element="bg": changeColor(
                        mouseGraphicsColors[element], mouseBG))
mouseBG.grid(column=1, row=0)
mouseMOUSE = tk.Button(Colors,
                       text="***", fg="white",
                       bg=mouseGraphicsColors["mouse"].get(),
                       command=lambda element="mouse": changeColor(
                           mouseGraphicsColors[element], mouseMOUSE))
mouseMOUSE.grid(column=1, row=1)
mouseHOLE = tk.Button(Colors,
                      text="***", fg="white",
                      bg=mouseGraphicsColors["hole"].get(),
                      command=lambda element="hole": changeColor(
                          mouseGraphicsColors[element], mouseHOLE))
mouseHOLE.grid(column=1, row=2)
mouseGTRAIL = tk.Button(Colors,
                        text="***", fg="white",
                        bg=mouseGraphicsColors["gtrail"].get(),
                        command=lambda element="gtrail": changeColor(
                            mouseGraphicsColors[element], mouseGTRAIL))
mouseGTRAIL.grid(column=1, row=3)
mouseSTRAIL = tk.Button(Colors,
                        text="***", fg="white",
                        bg=mouseGraphicsColors["strail"].get(),
                        command=lambda element="strail": changeColor(
                            mouseGraphicsColors[element], mouseSTRAIL))
mouseSTRAIL.grid(column=1, row=4)
# </editor-fold>
# </editor-fold>
# ----------------------------
# timeStampsFrame = tk.LabelFrame(mouseTab, text="TimeStamps")
# timeStampsFrame.grid(column=1, row=1, sticky="news")
# tk.Label(timeStampsFrame, text="Start Round").grid(column=0, row=0)
# tk.Label(timeStampsFrame, text="First Reaction").grid(column=0, row=1)
# </editor-fold>
# ======= Task Tab =====================
# <editor-fold desc="Task">
taskTab = ttk.Frame(nb)
taskTab.grid()
taskValues = valueFrames["Equation"]
nb.add(taskTab, text="Task")
# ----------------------------
# <editor-fold desc="Graphics">
taskGraphicsFrame = tk.LabelFrame(taskTab, text="Графика")
taskGraphicsFrame.grid(column=0, row=0, rowspan=3, sticky="news")

taskSizesValues = taskValues["graphics"]["sizes"]
taskSizesFrame = tk.LabelFrame(taskGraphicsFrame, text="Размеры")
taskSizesFrame.grid(column=0, row=0, sticky="news")

taskFontType = tk.Label(taskGraphicsFrame, text="Тип Шрифта")
taskFontType.grid(column=0, row=1, sticky="news")

taskFONTTYPE = tk.Button(taskGraphicsFrame,
                     text=taskValues["graphics"]["font"].get(),
                     command=lambda element="plus": changeFont(taskFONTTYPE))
taskFONTTYPE.grid(column=1, row=1)

# <editor-fold desc="Sizes">
taskSizesPlus = tk.LabelFrame(taskSizesFrame, text="Плюс")
taskSizesPlus.grid(column=0, columnspan=2, row=0, sticky="news")
tk.Label(taskSizesPlus, text="Радиус").grid(column=0, row=0)
tk.Label(taskSizesPlus, text="Ширина").grid(column=0, row=1)
(tk.Spinbox(
    taskSizesPlus,
    width=5,
    textvariable=taskSizesValues["plus"]["radius"],
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    taskSizesPlus,
    width=5,
    textvariable=taskSizesValues["plus"]["width"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# --------------------------------------------
taskSizesPlus = tk.LabelFrame(taskSizesFrame, text="Квадраты")
taskSizesPlus.grid(column=0, columnspan=2, row=1, sticky="news")
tk.Label(taskSizesPlus, text="Длина").grid(column=0, row=0)
tk.Label(taskSizesPlus, text="Контур").grid(column=0, row=1)
(tk.Spinbox(
    taskSizesPlus,
    width=5,
    textvariable=taskSizesValues["squares"]["length"],
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    taskSizesPlus,
    width=5,
    textvariable=taskSizesValues["squares"]["width"],
    from_=0, to=20000)
 .grid(column=1, row=1))
tk.Label(taskSizesFrame, text="Шрифт").grid(column=0, row=2)
(tk.Spinbox(
    taskSizesFrame,
    width=5,
    textvariable=taskSizesValues["font"],
    from_=0, to=20000)
 .grid(column=1, row=2))
# </editor-fold>
# ---------------------------
# <editor-fold desc="Colors">
taskColorsValues = taskValues["graphics"]["colors"]
taskColorsFrames = tk.LabelFrame(taskGraphicsFrame, text="Цвета")
taskColorsFrames.grid(column=1, row=0, sticky="news")
tk.Label(taskColorsFrames, text="Фон").grid(column=0, row=0)
tk.Label(taskColorsFrames, text="Плюс").grid(column=0, row=1)
tk.Label(taskColorsFrames, text="Шрифт").grid(column=0, row=2)
tk.Label(taskColorsFrames, text="Квадрат Правильно").grid(column=0, row=3)
tk.Label(taskColorsFrames, text="Квадрат Неправильно").grid(column=0, row=4)

taskBG = tk.Button(taskColorsFrames,
                   text="***", fg="white",
                   bg=taskColorsValues["bg"].get(),
                   command=lambda element="bg": changeColor(
                       taskColorsValues[element], taskBG))
taskBG.grid(column=1, row=0)
taskPLUS = tk.Button(taskColorsFrames,
                     text="***", fg="white",
                     bg=taskColorsValues["plus"].get(),
                     command=lambda element="plus": changeColor(
                         taskColorsValues[element], taskPLUS))
taskPLUS.grid(column=1, row=1)
taskFONT = tk.Button(taskColorsFrames,
                     text="***", fg="white",
                     bg=taskColorsValues["font"].get(),
                     command=lambda element="font": changeColor(
                         taskColorsValues[element], taskFONT))
taskFONT.grid(column=1, row=2)
taskRIGHT = tk.Button(taskColorsFrames,
                      text="***", fg="white",
                      bg=taskColorsValues["right"].get(),
                      command=lambda element="right": changeColor(
                          taskColorsValues[element], taskRIGHT))
taskRIGHT.grid(column=1, row=3)
taskWRONG = tk.Button(taskColorsFrames,
                      text="***", fg="white",
                      bg=taskColorsValues["wrong"].get(),
                      command=lambda element="wrong": changeColor(
                          taskColorsValues[element], taskWRONG))
taskWRONG.grid(column=1, row=4)
# </editor-fold>
# </editor-fold>
# # ------- controlFrame ---------------------
# <editor-fold desc="control">
controlFrame = tk.LabelFrame(taskTab, text="Control")
controlFrame.grid(column=1, row=1, sticky="news")
tk.Label(controlFrame, text="Inverse").grid(column=0, row=0)
tk.Label(controlFrame, text="Sensitivity").grid(column=0, row=1)
(tk.Checkbutton(
    controlFrame,
    variable=valueFrames["Equation"]["control"]["inverse"],
    onvalue=1, offvalue=0)
 .grid(column=1, row=0))
(tk.Spinbox(
    controlFrame,
    width=5,
    increment=0.1,
    textvariable=valueFrames["Equation"]["control"]["sensitivity"],
    from_=0.1, to=1)
 .grid(column=1, row=1))
# </editor-fold>
# ----------- timeDelays --------------------
# <editor-fold desc="timeDelays">
delayFrame = tk.LabelFrame(taskTab, text="Time Delays")
delayFrame.grid(column=1, row=2, sticky="news")
tk.Label(delayFrame, text="Plus Time").grid(column=0, row=0)
tk.Label(delayFrame, text="Answer Time").grid(column=0, row=1)
(tk.Spinbox(
    delayFrame,
    width=5,
    textvariable=valueFrames["Equation"]["duration"]["plus"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    delayFrame,
    width=5,
    textvariable=valueFrames["Equation"]["duration"]["answer"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=1))
# </editor-fold>
# ----------- fileChoice --------------------
# <editor-fold desc="fileChoice">
fileChoice = tk.LabelFrame(taskTab, text="File Choice")
fileChoice.grid(column=1, row=0, sticky="news")
tk.Label(fileChoice, text="Choose File:").grid(column=0, row=0)
(tk.Button(
    fileChoice,
    textvariable=valueFrames["Equation"]["file"]["path"],
    command=selectFile)
 .grid(column=1, row=0))
# </editor-fold>
# # --------- TimeStamps
# timeStampsFrame = tk.LabelFrame(taskTab, text="TimeStamps")
# timeStampsFrame.grid(column=1, row=1, sticky="news")
# tk.Label(timeStampsFrame, text="Start Round").grid(column=0, row=0)
# tk.Label(timeStampsFrame, text="First Reaction").grid(column=0, row=1)
# </editor-fold>
# ======= PVT Tab =====================
# <editor-fold desc="PVT">
pvtTab = ttk.Frame(nb)
pvtTab.grid()
nb.add(pvtTab, text="PVT")
pvtValues = valueFrames["PVT"]
# ----------------------------
# <editor-fold desc="Graphics">
pvtGraphicsFrame = tk.LabelFrame(pvtTab, text="Графика")
pvtGraphicsFrame.grid(column=0, row=0, sticky="news")

# <editor-fold desc="Sizes">
pvtSizesValues = pvtValues["graphics"]["size"]
pvtSizesFrame = tk.LabelFrame(pvtGraphicsFrame, text="Размеры")
pvtSizesFrame.grid(column=0, row=0, sticky="news")

pvtCircle = tk.Label(pvtSizesFrame, text="Круг")
pvtCircle.grid(column=0, row=0, sticky="news")
(tk.Spinbox(
    pvtSizesFrame,
    width=5,
    textvariable=pvtSizesValues["circleRadius"],
    from_=0, to=20000)
 .grid(column=1, row=0))
pvtSizesPlus = tk.LabelFrame(pvtSizesFrame, text="Плюс")
pvtSizesPlus.grid(column=0, row=1, columnspan=2, sticky="news")

(tk.Label(pvtSizesPlus, text="Длина")
 .grid(column=0, row=0, sticky="news"))

(tk.Spinbox(
    pvtSizesPlus,
    width=5,
    textvariable=pvtSizesValues["plus"]["radius"],
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Label(pvtSizesPlus, text="Контур")
 .grid(column=0, row=1, sticky="news"))

(tk.Spinbox(
    pvtSizesPlus,
    width=5,
    textvariable=pvtSizesValues["plus"]["width"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# </editor-fold>
# # ---------------------------
# <editor-fold desc="Colors">
pvtColorsValues = pvtValues["graphics"]["color"]
pvtColorsFrames = tk.LabelFrame(pvtGraphicsFrame, text="Цвета")
pvtColorsFrames.grid(column=1, row=0, sticky="news")
tk.Label(pvtColorsFrames, text="Фон").grid(column=0, row=0)
tk.Label(pvtColorsFrames, text="Плюс").grid(column=0, row=1)
tk.Label(pvtColorsFrames, text="Круг").grid(column=0, row=2)

pvtBG = tk.Button(pvtColorsFrames,
                   text="***", fg="white",
                   bg=pvtColorsValues["bg"].get(),
                   command=lambda element="bg": changeColor(
                       pvtColorsValues[element], pvtBG))
pvtBG.grid(column=1, row=0)
pvtPLUS = tk.Button(pvtColorsFrames,
                     text="***", fg="white",
                     bg=pvtColorsValues["plus"].get(),
                     command=lambda element="plus": changeColor(
                         pvtColorsValues[element], pvtPLUS))
pvtPLUS.grid(column=1, row=1)
pvtCIRCLE = tk.Button(pvtColorsFrames,
                     text="***", fg="white",
                     bg=pvtColorsValues["circle"].get(),
                     command=lambda element="circle": changeColor(
                         pvtColorsValues[element], pvtCIRCLE))
pvtCIRCLE.grid(column=1, row=2)
# # </editor-fold>
# </editor-fold>
# # ----------- timeDelays --------------------
# <editor-fold desc="timeDelays">
pvtDelayValues = pvtValues["delay"]
pvtDelayFrame = tk.LabelFrame(pvtTab, text="Time Delays")
pvtDelayFrame.grid(column=1, row=0, sticky="news")
tk.Label(pvtDelayFrame, text="Plus Time").grid(column=0, row=0)
tk.Label(pvtDelayFrame, text="EmptyMin").grid(column=0, row=1)
tk.Label(pvtDelayFrame, text="EmptyMax").grid(column=0, row=2)
tk.Label(pvtDelayFrame, text="Answer").grid(column=0, row=3)
tk.Label(pvtDelayFrame, text="MSI").grid(column=0, row=4)
(tk.Spinbox(
    pvtDelayFrame,
    width=5,
    textvariable=pvtDelayValues["plus"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    pvtDelayFrame,
    width=5,
    textvariable=pvtDelayValues["emptyMin"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=1))
(tk.Spinbox(
    pvtDelayFrame,
    width=5,
    textvariable=pvtDelayValues["emptyMax"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=2))
(tk.Spinbox(
    pvtDelayFrame,
    width=5,
    textvariable=pvtDelayValues["answer"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=3))
(tk.Spinbox(
    pvtDelayFrame,
    width=5,
    textvariable=pvtDelayValues["msi"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=4))
# </editor-fold>
# </editor-fold>
# ======= Control Tab =====================
# <editor-fold desc="Control">
controlTab = ttk.Frame(nb)
controlTab.grid()
nb.add(controlTab, text="Control")
controlValues = valueFrames["Control"]
# ----------------------------
# <editor-fold desc="Graphics">
controlGraphicsFrame = tk.LabelFrame(controlTab, text="Графика")
controlGraphicsFrame.grid(column=0, row=0, sticky="news")

# <editor-fold desc="Sizes">
controlSizesValues = pvtValues["graphics"]["size"]
controlSizesFrame = tk.LabelFrame(controlGraphicsFrame, text="Размеры Плюса")
controlSizesFrame.grid(column=0, row=0, sticky="news")

(tk.Label(controlSizesFrame, text="Длина")
 .grid(column=0, row=0, sticky="news"))

(tk.Label(controlSizesFrame, text="Контур")
 .grid(column=0, row=1, sticky="news"))

(tk.Spinbox(
    controlSizesFrame,
    width=5,
    textvariable=controlSizesValues["plus"]["radius"],
    from_=0, to=20000)
 .grid(column=1, row=0))
(tk.Spinbox(
    controlSizesFrame,
    width=5,
    textvariable=controlSizesValues["plus"]["width"],
    from_=0, to=20000)
 .grid(column=1, row=1))
# </editor-fold>
# # ---------------------------
# <editor-fold desc="Colors">
controlColorsValues = controlValues["graphics"]["color"]
controlColorsFrames = tk.LabelFrame(controlGraphicsFrame, text="Цвета")
controlColorsFrames.grid(column=1, row=0, sticky="news")
tk.Label(controlColorsFrames, text="Фон").grid(column=0, row=0)
tk.Label(controlColorsFrames, text="Плюс").grid(column=0, row=1)

controlBG = tk.Button(controlColorsFrames,
                   text="***", fg="white",
                   bg=controlColorsValues["bg"].get(),
                   command=lambda element="bg": changeColor(
                       controlColorsValues[element], controlBG))
controlBG.grid(column=1, row=0)
controlPLUS = tk.Button(controlColorsFrames,
                     text="***", fg="white",
                     bg=controlColorsValues["plus"].get(),
                     command=lambda element="plus": changeColor(
                         controlColorsValues[element], controlPLUS))
controlPLUS.grid(column=1, row=1)
# # </editor-fold>
# </editor-fold>
# # ----------- timeDelays --------------------
# <editor-fold desc="timeDelays">
controlDelayValues = controlValues["delay"]
controlDelayFrame = tk.LabelFrame(controlTab, text="Time Delays")
controlDelayFrame.grid(column=1, row=0, sticky="news")
tk.Label(controlDelayFrame, text="Plus Time").grid(column=0, row=0)
(tk.Spinbox(
    controlDelayFrame,
    width=5,
    textvariable=controlDelayValues["plus"],
    increment=0.1,
    from_=0, to=20000)
 .grid(column=1, row=0))
# </editor-fold>
# </editor-fold>

root.mainloop()
