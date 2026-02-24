import ctypes
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.colorchooser import askcolor
from tkfontchooser import askfont
import config as cfg

class MainMenu:
    def __init__(self):
        self.result = None
        self.root = tk.Tk(); 
        self.root.resizable(False, False); 
        self.root.title('Configuration window'); 
        self.root.minsize(220, 120)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        user32 = ctypes.windll.user32
        self.displaySize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        # print(displaySize)
        cfg.loadConfig()
        self.config = cfg.getConfig()

        self.valueFrames = self._setToType(self.config)
        self._update_dict_values(self.valueFrames, self.config)

        self._create_widgets()

    def get_timer_value(self):
        self._update_dict_values(self.config, self.valueFrames)
        cfg.updateConfig(self.config)
        return self.valueFrames["general"]["window"]["startTimer"].get()
    
    def _on_close(self):
        self.result = False
        self.root.destroy()

    def start_exp(self):
        self.result = True
        self.root.destroy()

    def _setToType(self, diction):
        new_diction = {}
        for key in diction:
            match diction[key]:
                case dict():
                    new_diction[key] = self._setToType(diction[key])
                case bool():
                        new_diction[key] =  tk.BooleanVar()
                case int():
                        new_diction[key] = tk.IntVar()
                case float():
                        new_diction[key] = tk.DoubleVar()
                case str():
                        new_diction[key] = tk.StringVar()
        return new_diction

    def _update_dict_values(self, dict1, dict2):
        for key, value in dict1.items():
            if key in dict2:
                if isinstance(value, dict) and isinstance(dict2[key], dict):
                    self._update_dict_values(value, dict2[key])
                else:
                    if type(dict1[key]) in [
                        tk.IntVar, tk.BooleanVar, tk.StringVar, tk.DoubleVar
                    ]:
                        dict1[key].set(dict2[key])
                    else:
                        dict1[key] = dict2[key].get()
        return dict1

    def _changeColor(colorConfig, button):
        print(colorConfig)
        colors = askcolor(title="ColorsChooserPicker")
        print(colors)
        if colors[1] is not None:
            button.config(bg=colors[1])
            colorConfig.set(colors[1])

    def _changeFont(self, button):
        font = askfont(text="12+53=65",
                    family=self.valueFrames["Equation"]["graphics"]["font"].get(),
                    size=self.valueFrames["Equation"]["graphics"]["sizes"]["font"].get())
        button.config(text=font["family"])
        self.valueFrames["Equation"]["graphics"]["font"].set(font["family"])

    def _selectFile(self):
        filetypes = (('.txt файлы', '*.txt'), ('Все файлы', '*.*'))
        file = filedialog.askopenfilename(title='Выберите файл', initialdir='/',
                                        filetypes=filetypes)
        print(file)
        if file == "":
            self.valueFrames["Equation"]["file"]["path"].set("None")
        else:
            self.valueFrames["Equation"]["file"]["path"].set(file)

    class CountdownButton(tk.Button):
        def __init__(self, get_timer_value, on_timeout, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.get_timer_value = get_timer_value
            self.on_timeout = on_timeout
            self.count = 0

            self.configure(command=self.start_countdown)

        def start_countdown(self):
            self.configure(state="disabled")
            self.count = self.get_timer_value()
            print(self.count)
            print("start countdown")
            self.countdown()

        def countdown(self):
            print("countdown", self.count)
            if self.count > 0:
                self.count -= 1
                self.configure(text=f"Get Ready...{self.count}")
                self.after(1000, self.countdown)  # repeat after 1 second
            else:
                self.on_timeout()

    def _create_widgets(self):
        nb =             ttk.Notebook(self.root);                                                                                      nb.grid(          row=0, columnspan=3, sticky="NEWS")
        generalTab = ttk.Frame(nb); generalTab.grid(); nb.add(generalTab, text="General")
        mouseTab   = ttk.Frame(nb); mouseTab  .grid(); nb.add(mouseTab,   text="Mouse"  )
        taskTab    = ttk.Frame(nb); taskTab   .grid(); nb.add(taskTab,    text="Task"   )
        pvtTab     = ttk.Frame(nb); pvtTab    .grid(); nb.add(pvtTab,     text="PVT"    )
        controlTab = ttk.Frame(nb); controlTab.grid(); nb.add(controlTab, text="Control")

        programName = self.valueFrames["general"]["experiment"]["program"]

        tk.Label(                     self.root, text="Программа"                                                                       ).grid(column=0, row=1)
        tk.OptionMenu(                self.root, programName, *["Mouses", "Tasks", "PVT", "Control"]).grid(column=1, row=1)
        startButton = self.CountdownButton(
            get_timer_value = self.get_timer_value,
            on_timeout=self.start_exp,
            master = self.root,
            relief = "raised",
            text = "Start Experiment"
        )
        startButton.grid(column=2, row=1, sticky="NEWS")

        # ======== general tab ===========
        windowFrame     = tk.LabelFrame(generalTab, text="Параметры окна" ); windowFrame    .grid(column=0, row=0, sticky="news")
        alarmFrame      = tk.LabelFrame(generalTab, text="Будильник"      ); alarmFrame     .grid(column=0, row=1, sticky="news")
        experimentFrame = tk.LabelFrame(generalTab, text="Experiments"    ); experimentFrame.grid(column=1, row=0, sticky="news")
        timeStampsFrame = tk.LabelFrame(generalTab, text="Временные метки"); timeStampsFrame.grid(column=1, row=1, sticky="news")

        generalConfig = self.valueFrames["general"   ]
        windowConfig     = generalConfig["window"    ]
        alarmConfig      = generalConfig["alarm"     ]
        experimentConfig = generalConfig["experiment"]
        timeStampsConfig = generalConfig["timeStamps"]

        # --------- windowFrame -----------
        tk.Label      (windowFrame, text="Полноэкранный?"                                                            ).grid(column=0, row=0)
        tk.Label      (windowFrame, text="Длина окна"                                                                ).grid(column=0, row=1)
        tk.Label      (windowFrame, text="Высота окна"                                                               ).grid(column=0, row=2)
        tk.Label      (windowFrame, text="Время таймера\nзапуска"                                                    ).grid(column=0, row=3)
        tk.Checkbutton(windowFrame,     variable=windowConfig["fullScreen"],      onvalue=1, offvalue=0              ).grid(column=1, row=0)
        tk.Spinbox    (windowFrame, textvariable=windowConfig["width"     ], width=5, from_=0, to=self.displaySize[0]).grid(column=1, row=1)
        tk.Spinbox    (windowFrame, textvariable=windowConfig["height"    ], width=5, from_=0, to=self.displaySize[1]).grid(column=1, row=2)
        tk.Spinbox    (windowFrame, textvariable=windowConfig["startTimer"], width=5, from_=0, to=20000              ).grid(column=1, row=3)
        # ---------- alarmFrame ----------------
        tk.Label      (alarmFrame, text="Включить?"                                                               ).grid(column=0, row=0)
        tk.Label      (alarmFrame, text="Частота тона"                                                            ).grid(column=0, row=1)
        tk.Label      (alarmFrame, text="Громкость"                                                               ).grid(column=0, row=2)
        tk.Label      (alarmFrame, text="Длительность"                                                            ).grid(column=0, row=3)
        tk.Checkbutton(alarmFrame,     variable=alarmConfig["enable"  ],                     onvalue=1, offvalue=0).grid(column=1, row=0)
        tk.Spinbox    (alarmFrame, textvariable=alarmConfig["freq"    ], width=5, from_=0, to=20000               ).grid(column=1, row=1)
        tk.Spinbox    (alarmFrame, textvariable=alarmConfig["volume"  ], width=5, from_=0, to=20000               ).grid(column=1, row=2)
        tk.Spinbox    (alarmFrame, textvariable=alarmConfig["duration"], width=5, from_=0, to=20000, increment=0.1).grid(column=1, row=3)
        # ---------- experimentFrame ----------------
        tk.Label  (experimentFrame, text="Кол-во раундов"                                              ).grid(column=0, row=1)
        tk.Label  (experimentFrame, text="Имя испытуемого"                                             ).grid(column=0, row=2)
        tk.Label  (experimentFrame, text="Код испытуемого"                                             ).grid(column=0, row=3)
        tk.Spinbox(experimentFrame, textvariable=experimentConfig["round"], width=5,  from_=1, to=20000).grid(column=1, row=1)
        tk.Entry  (experimentFrame, textvariable=experimentConfig["name" ], width=10,                  ).grid(column=1, row=2)
        tk.Entry  (experimentFrame, textvariable=experimentConfig["code" ], width=10,                  ).grid(column=1, row=3)
        # ---------- timeStampsFrame ----------------
        tk.Label      (timeStampsFrame, text="USB-метки?"                                                     ).grid(column=0, row=0)
        tk.Label      (timeStampsFrame, text="Датчик света?"                                                  ).grid(column=0, row=1)
        tk.Label      (timeStampsFrame, text="Размер квадрата света"                                          ).grid(column=0, row=2)
        tk.Checkbutton(timeStampsFrame,     variable=timeStampsConfig["trigger"  ], onvalue=1, offvalue=0     ).grid(column=1, row=0)
        tk.Checkbutton(timeStampsFrame,     variable=timeStampsConfig["light"    ], onvalue=1, offvalue=0     ).grid(column=1, row=1)
        tk.Spinbox    (timeStampsFrame, textvariable=timeStampsConfig["lightSize"], width=5, from_=0, to=20000).grid(column=1, row=2)
        # ======== Mouse Tab =======================
        mouseConfig = self.valueFrames["Mouses"]
        mouseControlConfig  = mouseConfig["control"]
        mouseGraphics       = mouseConfig["graphics"]
        mouseGraphicsSizes  = mouseGraphics["sizes"]
        mouseGraphicsColors = mouseGraphics["colors"]
        mouseControlFrame  = tk.LabelFrame(mouseTab, text="Управление"); mouseControlFrame.grid(column=1, row=0, sticky="news")
        mouseLoggerFrame   = tk.LabelFrame(mouseTab, text="Logger"    ); mouseLoggerFrame .grid(column=1, row=1, sticky="news")
        mouseGraphicsFrame = tk.LabelFrame(mouseTab, text="Графика"   ); mouseGraphicsFrame    .grid(column=0, row=0, sticky="news", rowspan=2)
        # ------- controlFrame ---------------------
        tk.Label      (mouseControlFrame, text="Инверсия?"                                                          ).grid(column=0, row=0)
        tk.Label      (mouseControlFrame, text="Чуствительность\n(1 - размер квадрата)"                             ).grid(column=0, row=1)
        tk.Checkbutton(mouseControlFrame,     variable=mouseControlConfig["inverse"    ], onvalue=1, offvalue=0     ).grid(column=1, row=0)
        tk.Spinbox    (mouseControlFrame, textvariable=mouseControlConfig["sensitivity"], from_=0, to=20000, width=5).grid(column=1, row=1)
        # ----------- loggerFrame --------------------
        tk.Label  (mouseLoggerFrame, text="Frequency"                                                                      ).grid(column=0, row=0)
        tk.Spinbox(mouseLoggerFrame, textvariable=mouseConfig["logger"]["freq"], width=5, increment=0.01, from_=0, to=20000).grid(column=1, row=0)
        # ----------- graphics --------------------
        mousesSizesFrame  = tk.LabelFrame(mouseGraphicsFrame, text="Размеры"); mousesSizesFrame .grid(column=0, row=0, sticky="news")
        mousesColorsFrame = tk.LabelFrame(mouseGraphicsFrame, text="Цвета"  ); mousesColorsFrame.grid(column=1, row=0, sticky="news")

        tk.Label  (mousesSizesFrame, text="Умножитель\nрастояния\n(2 -> 2 радиуса)"                                             ).grid(column=0, row=0)
        tk.Label  (mousesSizesFrame, text="Радиус зоны\nбездействия"                                                            ).grid(column=0, row=1)
        tk.Label  (mousesSizesFrame, text="Радиусы"                                                                             ).grid(column=0, row=2)
        tk.Label  (mousesSizesFrame, text="Скорость мыши"                                                                       ).grid(column=0, row=3)
        tk.Label  (mousesSizesFrame, text="Максимальный\nразброс\n[0.07; 1)"                                                    ).grid(column=0, row=4)
        tk.Spinbox(mousesSizesFrame, textvariable=mouseGraphicsSizes["distMul"      ], width=5, from_=0, to=20000, increment=0.1).grid(column=1, row=0)
        tk.Spinbox(mousesSizesFrame, textvariable=mouseGraphicsSizes["waitZone"     ], width=5, from_=0                         ).grid(column=1, row=1)
        tk.Spinbox(mousesSizesFrame, textvariable=mouseGraphicsSizes["radius"       ], width=5, from_=0, to=200                 ).grid(column=1, row=2)
        tk.Spinbox(mousesSizesFrame, textvariable=mouseGraphicsSizes["speed"        ], width=5, from_=0, to=20                  ).grid(column=1, row=3)
        tk.Spinbox(mousesSizesFrame, textvariable=mouseGraphicsSizes["maxDispersion"], width=5, from_=0, to=0.9,   increment=0.1).grid(column=1, row=4)
        # ---------------------------
        tk.Label(mousesColorsFrame, text="Фон"                  ).grid(column=0, row=0)
        tk.Label(mousesColorsFrame, text="Мышь"                 ).grid(column=0, row=1)
        tk.Label(mousesColorsFrame, text="Нора"                 ).grid(column=0, row=2)
        tk.Label(mousesColorsFrame, text="Путь\nСгенерированный").grid(column=0, row=3)
        tk.Label(mousesColorsFrame, text="Путь\nИспытуемого"    ).grid(column=0, row=4)

        mouseBG     = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["bg"    ].get(), command=lambda element="bg"     : self._changeColor(mouseGraphicsColors[element], mouseBG    )); mouseBG    .grid(column=1, row=0)
        mouseMOUSE  = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["mouse" ].get(), command=lambda element="mouse"  : self._changeColor(mouseGraphicsColors[element], mouseMOUSE )); mouseMOUSE .grid(column=1, row=1)
        mouseHOLE   = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["hole"  ].get(), command=lambda element="hole"   : self._changeColor(mouseGraphicsColors[element], mouseHOLE  )); mouseHOLE  .grid(column=1, row=2)
        mouseGTRAIL = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["gtrail"].get(), command=lambda element="gtrail" : self._changeColor(mouseGraphicsColors[element], mouseGTRAIL)); mouseGTRAIL.grid(column=1, row=3)
        mouseSTRAIL = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["strail"].get(), command=lambda element="strail" : self._changeColor(mouseGraphicsColors[element], mouseSTRAIL)); mouseSTRAIL.grid(column=1, row=4)
        # ----------------------------
        # timeStampsFrame = tk.LabelFrame(mouseTab, text="TimeStamps")
        # timeStampsFrame.grid(column=1, row=1, sticky="news")
        # tk.Label(timeStampsFrame, text="Start Round").grid(column=0, row=0)
        # tk.Label(timeStampsFrame, text="First Reaction").grid(column=0, row=1)
        # ======= Task Tab =====================
        taskValues = self.valueFrames["Equation"]
        taskSizesValues    = taskValues["graphics"]["sizes"]
        taskColorsValues   = taskValues["graphics"]["colors"]
        taskFontFamily     = taskValues["graphics"]["font"]
        taskControlConfig  = taskValues["control"]
        taskDurationConfig = taskValues["duration"]
        taskSelectFile     = taskValues["file"]["path"]
        # ----------------------------
        taskGraphicsFrame = tk.LabelFrame(taskTab, text="Графика"    ); taskGraphicsFrame.grid(column=0, row=0, sticky="news", rowspan=3)
        controlFrame      = tk.LabelFrame(taskTab, text="Control"    ); controlFrame     .grid(column=1, row=1, sticky="news")
        delayFrame        = tk.LabelFrame(taskTab, text="Time Delays"); delayFrame       .grid(column=1, row=2, sticky="news")
        fileChoice        = tk.LabelFrame(taskTab, text="File Choice"); fileChoice       .grid(column=1, row=0, sticky="news")

        taskSizesFrame   = tk.LabelFrame(taskGraphicsFrame, text="Размеры"                                                                     ); taskSizesFrame  .grid(column=0, row=0, sticky="news")
        (                  tk.Label     (taskGraphicsFrame, text="Тип Шрифта"                                                                  )                  .grid(column=0, row=1, sticky="news"))
        taskFONTTYPE     = tk.Button    (taskGraphicsFrame, text=taskFontFamily.get(), command=lambda: self._changeFont(taskFONTTYPE)); taskFONTTYPE    .grid(column=1, row=1)
        taskColorsFrames = tk.LabelFrame(taskGraphicsFrame, text="Цвета"                                                                       ); taskColorsFrames.grid(column=1, row=0, sticky="news")

        taskSizesPlus    = tk.LabelFrame(taskSizesFrame, text="Плюс"    ); taskSizesPlus   .grid(column=0, columnspan=2, row=0, sticky="news")
        taskSizesSquares = tk.LabelFrame(taskSizesFrame, text="Квадраты"); taskSizesSquares.grid(column=0, columnspan=2, row=1, sticky="news")

        tk.Label  (taskSizesPlus, text="Радиус"                                                             ).grid(column=0, row=0)
        tk.Label  (taskSizesPlus, text="Ширина"                                                             ).grid(column=0, row=1)
        tk.Spinbox(taskSizesPlus, textvariable=taskSizesValues["plus"]["radius"], width=5, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(taskSizesPlus, textvariable=taskSizesValues["plus"]["width" ], width=5, from_=0, to=20000).grid(column=1, row=1)
        # --------------------------------------------

        tk.Label  (taskSizesSquares, text="Длина"                                                                 ).grid(column=0, row=0)
        tk.Label  (taskSizesSquares, text="Контур"                                                                ).grid(column=0, row=1)
        tk.Spinbox(taskSizesSquares, textvariable=taskSizesValues["squares"]["length"], width=5, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(taskSizesSquares, textvariable=taskSizesValues["squares"]["width" ], width=5, from_=0, to=20000).grid(column=1, row=1)

        tk.Label  (taskSizesFrame, text="Шрифт"                                                     ).grid(column=0, row=2)
        tk.Spinbox(taskSizesFrame, textvariable=taskSizesValues["font"], width=5,  from_=0, to=20000).grid(column=1, row=2)
        # ---------------------------

        tk.Label(taskColorsFrames, text="Фон"                ).grid(column=0, row=0)
        tk.Label(taskColorsFrames, text="Плюс"               ).grid(column=0, row=1)
        tk.Label(taskColorsFrames, text="Шрифт"              ).grid(column=0, row=2)
        tk.Label(taskColorsFrames, text="Квадрат Правильно"  ).grid(column=0, row=3)
        tk.Label(taskColorsFrames, text="Квадрат Неправильно").grid(column=0, row=4)

        taskBG    = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["bg"   ].get(), command=lambda element="bg"    : self._changeColor(taskColorsValues[element], taskBG   )); taskBG   .grid(column=1, row=0)
        taskPLUS  = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["plus" ].get(), command=lambda element="plus"  : self._changeColor(taskColorsValues[element], taskPLUS )); taskPLUS .grid(column=1, row=1)
        taskFONT  = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["font" ].get(), command=lambda element="font"  : self._changeColor(taskColorsValues[element], taskFONT )); taskFONT .grid(column=1, row=2)
        taskRIGHT = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["right"].get(), command=lambda element="right" : self._changeColor(taskColorsValues[element], taskRIGHT)); taskRIGHT.grid(column=1, row=3)
        taskWRONG = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["wrong"].get(), command=lambda element="wrong" : self._changeColor(taskColorsValues[element], taskWRONG)); taskWRONG.grid(column=1, row=4)
        # ------- controlFrame ---------------------
        tk.Label      (controlFrame, text="Inverse"                                                                                         ).grid(column=0, row=0)
        tk.Label      (controlFrame, text="Sensitivity"                                                                                     ).grid(column=0, row=1)
        tk.Checkbutton(controlFrame,     variable=taskControlConfig["inverse"    ], onvalue=1, offvalue=0                  ).grid(column=1, row=0)
        tk.Spinbox    (controlFrame, textvariable=taskControlConfig["sensitivity"], width=5, increment=0.1, from_=0.1, to=1).grid(column=1, row=1) 
        # ----------- timeDelays --------------------
        tk.Label  (delayFrame, text="Plus Time"                                                                                     ).grid(column=0, row=0)
        tk.Label  (delayFrame, text="Answer Time"                                                                                   ).grid(column=0, row=1)
        tk.Spinbox(delayFrame, textvariable=taskDurationConfig["plus"  ], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(delayFrame, textvariable=taskDurationConfig["answer"], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=1)
        # ----------- fileChoice --------------------
        tk.Label (fileChoice, text="Choose File:"                                                     ).grid(column=0, row=0)
        tk.Button(fileChoice, textvariable=taskSelectFile, command=self._selectFile).grid(column=1, row=0)
        # --------- TimeStamps
        # timeStampsFrame = tk.LabelFrame(taskTab, text="TimeStamps")
        # timeStampsFrame.grid(column=1, row=1, sticky="news")
        # tk.Label(timeStampsFrame, text="Start Round").grid(column=0, row=0)
        # tk.Label(timeStampsFrame, text="First Reaction").grid(column=0, row=1)
        # ======= PVT Tab =====================

        pvtValues = self.valueFrames["PVT"]
        pvtSizesValues     = pvtValues["graphics"]["sizes" ]
        pvtColorsValues    = pvtValues["graphics"]["colors"]
        controlSizesValues = pvtValues["graphics"]["sizes" ]
        pvtDelayValues     = pvtValues["delay"   ]

        # ----------------------------
        pvtGraphicsFrame = tk.LabelFrame(pvtTab, text="Графика"    ); pvtGraphicsFrame.grid(column=0, row=0, sticky="news")
        pvtDelayFrame    = tk.LabelFrame(pvtTab, text="Time Delays"); pvtDelayFrame   .grid(column=1, row=0, sticky="news")
        pvtSizesFrame   = tk.LabelFrame(pvtGraphicsFrame, text="Размеры"); pvtSizesFrame  .grid(column=0, row=0, sticky="news")
        pvtColorsFrames = tk.LabelFrame(pvtGraphicsFrame, text="Цвета"  ); pvtColorsFrames.grid(column=1, row=0, sticky="news")

        pvtCircle =    tk.Label     (pvtSizesFrame, text="Круг"                                                 ); pvtCircle   .grid(column=0, row=0, sticky="news")
        pvtSizesPlus = tk.LabelFrame(pvtSizesFrame, text="Плюс"                                                 ); pvtSizesPlus.grid(column=0, row=1, columnspan=2, sticky="news")
        (              tk.Spinbox   (pvtSizesFrame, textvariable=pvtSizesValues["circleRadius"], width=5, from_=0, to=20000   ).grid(column=1, row=0))

        tk.Label  (pvtSizesPlus, text="Длина"                                                           ).grid(column=0, row=0, sticky="news")
        tk.Label  (pvtSizesPlus, text="Контур"                                                          ).grid(column=0, row=1, sticky="news")
        tk.Spinbox(pvtSizesPlus, textvariable=pvtSizesValues["plus"]["radius"],width=5,from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(pvtSizesPlus, textvariable=pvtSizesValues["plus"]["width"], width=5,from_=0, to=20000).grid(column=1, row=1)
        # ---------------------------
        tk.Label(pvtColorsFrames, text="Фон" ).grid(column=0, row=0)
        tk.Label(pvtColorsFrames, text="Плюс").grid(column=0, row=1)
        tk.Label(pvtColorsFrames, text="Круг").grid(column=0, row=2)

        pvtBG     = tk.Button(pvtColorsFrames, text="***", fg="white", bg=pvtColorsValues["bg"    ].get(), command=lambda element="bg"    : self._changeColor(pvtColorsValues[element], pvtBG    )); pvtBG    .grid(column=1, row=0)
        pvtPLUS   = tk.Button(pvtColorsFrames, text="***", fg="white", bg=pvtColorsValues["plus"  ].get(), command=lambda element="plus"  : self._changeColor(pvtColorsValues[element], pvtPLUS  )); pvtPLUS  .grid(column=1, row=1)
        pvtCIRCLE = tk.Button(pvtColorsFrames, text="***", fg="white", bg=pvtColorsValues["circle"].get(), command=lambda element="circle": self._changeColor(pvtColorsValues[element], pvtCIRCLE)); pvtCIRCLE.grid(column=1, row=2)
        # ----------- timeDelays --------------------
        tk.Label  (pvtDelayFrame, text="Plus Time"                                                                  ).grid(column=0, row=0)
        tk.Label  (pvtDelayFrame, text="EmptyMin"                                                                   ).grid(column=0, row=1)
        tk.Label  (pvtDelayFrame, text="EmptyMax"                                                                   ).grid(column=0, row=2)
        tk.Label  (pvtDelayFrame, text="Answer"                                                                     ).grid(column=0, row=3)
        tk.Label  (pvtDelayFrame, text="MSI"                                                                        ).grid(column=0, row=4)
        tk.Spinbox(pvtDelayFrame, textvariable=pvtDelayValues["plus"    ], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(pvtDelayFrame, textvariable=pvtDelayValues["emptyMin"], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=1)
        tk.Spinbox(pvtDelayFrame, textvariable=pvtDelayValues["emptyMax"], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=2)
        tk.Spinbox(pvtDelayFrame, textvariable=pvtDelayValues["answer"  ], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=3)
        tk.Spinbox(pvtDelayFrame, textvariable=pvtDelayValues["msi"     ], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=4)
        # ======= Control Tab =====================

        controlValues = self.valueFrames["Control"]
        controlColorsValues = controlValues["graphics"]["colors"]
        controlDelayValues  = controlValues["delay"]
        # ----------------------------
        controlGraphicsFrame = tk.LabelFrame(controlTab, text="Графика"    ); controlGraphicsFrame.grid(column=0, row=0, sticky="news")
        controlDelayFrame    = tk.LabelFrame(controlTab, text="Time Delays"); controlDelayFrame   .grid(column=1, row=0, sticky="news")

        controlSizesFrame   = tk.LabelFrame(controlGraphicsFrame, text="Размеры Плюса"); controlSizesFrame  .grid(column=0, row=0, sticky="news")
        controlColorsFrames = tk.LabelFrame(controlGraphicsFrame, text="Цвета"        ); controlColorsFrames.grid(column=1, row=0, sticky="news")

        tk.Label  (controlSizesFrame, text="Длина"                                                                 ).grid(column=0, row=0, sticky="news")
        tk.Label  (controlSizesFrame, text="Контур"                                                                ).grid(column=0, row=1, sticky="news")
        tk.Spinbox(controlSizesFrame, textvariable=controlSizesValues["plus"]["radius"], width=5, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(controlSizesFrame, textvariable=controlSizesValues["plus"]["width"],  width=5, from_=0, to=20000).grid(column=1, row=1)
        # ---------------------------
        (             tk.Label (controlColorsFrames, text="Фон"                                                                                                                                                      ).grid(column=0, row=0))
        (             tk.Label (controlColorsFrames, text="Плюс"                                                                                                                                                     ).grid(column=0, row=1))
        controlBG   = tk.Button(controlColorsFrames, text="***", fg="white", bg=controlColorsValues["bg"  ].get(), command=lambda element="bg"  : self._changeColor(controlColorsValues[element], controlBG  )); controlBG  .grid(column=1, row=0)
        controlPLUS = tk.Button(controlColorsFrames, text="***", fg="white", bg=controlColorsValues["plus"].get(), command=lambda element="plus": self._changeColor(controlColorsValues[element], controlPLUS)); controlPLUS.grid(column=1, row=1)
        # ----------- timeDelays --------------------
        tk.Label  (controlDelayFrame, text="Plus Time"                                                                  ).grid(column=0, row=0)
        tk.Spinbox(controlDelayFrame, textvariable=controlDelayValues["plus"], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=0)

        pass
          
    def run(self):
        self.root.mainloop()
        return self.result

def run():
    menu = MainMenu()
    return menu.run()

if __name__ == "__main__":
    run()