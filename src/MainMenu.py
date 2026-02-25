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
        cfg.loadConfig()
        self.config = cfg.getConfig()

        self.valueFrames = self._setToType(self.config)
        self._update_dict_values(self.valueFrames, self.config)

        self._create_widgets()
        # self._apply_dark_theme()

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

    def _changeColor(self, colorConfig, button):
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

    def _on_tab_changed(self, event):
        selectedTabID = self.nb.select()
        selectedTabName = self.nb.tab(selectedTabID, "text")
        self.valueFrames["general"]["experiment"]["program"].set(selectedTabName)
        self.startButton.config(text=f"Запустить программу '{selectedTabName}'")

    def _create_widgets(self):

        generalFrame = tk.LabelFrame(self.root, text="Общие настройки", borderwidth=10); generalFrame    .grid(column=0, row=0, sticky="news")

        self.nb = ttk.Notebook(self.root); self.nb.grid(row = 0, column = 1, columnspan=1, sticky="NEWS")
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        mouseTab   = ttk.Frame(self.nb); mouseTab  .grid(); self.nb.add(mouseTab  , text="Mouses" )
        taskTab    = ttk.Frame(self.nb); taskTab   .grid(); self.nb.add(taskTab   , text="Tasks"  )
        pvtTab     = ttk.Frame(self.nb); pvtTab    .grid(); self.nb.add(pvtTab    , text="PVT"    )
        controlTab = ttk.Frame(self.nb); controlTab.grid(); self.nb.add(controlTab, text="Control")

        self.startButton = self.CountdownButton(
            get_timer_value = self.get_timer_value,
            on_timeout=self.start_exp,
            master = self.root,
            relief = "raised",
        )
        self.startButton.grid(column=1, row=1) #, sticky="NEWS")

        # ======== general tab ===========
        generalConfig = self.valueFrames["general"   ]
        windowConfig          = generalConfig["window"    ]
        alarmConfig           = generalConfig["alarm"     ]
        experimentConfig      = generalConfig["experiment"]
        timeStampsConfig      = generalConfig["timeStamps"]
        generalGraphicsConfig = generalConfig["graphics"]
        generalSizesValues    = generalGraphicsConfig["sizes"]
        generalColorsValues   = generalGraphicsConfig["colors"]

        windowFrame          = tk.LabelFrame(generalFrame, text="Параметры окна" ); windowFrame         .grid(column=0, row=0, sticky="news")
        alarmFrame           = tk.LabelFrame(generalFrame, text="Будильник"      ); alarmFrame          .grid(column=0, row=1, sticky="news")
        taskExperimentFrame  = tk.LabelFrame(generalFrame, text="Experiments"    ); taskExperimentFrame .grid(column=1, row=0, sticky="news")
        timeStampsFrame      = tk.LabelFrame(generalFrame, text="Временные метки"); timeStampsFrame     .grid(column=1, row=1, sticky="news")
        generalGraphicsFrame = tk.LabelFrame(generalFrame, text="Общая графика"  ); generalGraphicsFrame.grid(column=0, row=2, columnspan=2, sticky="news")

        generalSizesFrame    = tk.LabelFrame(generalGraphicsFrame, text="Размеры Плюса"); generalSizesFrame   .grid(column=0, row=0, sticky="news")
        generalColorsFrames  = tk.LabelFrame(generalGraphicsFrame, text="Цвета"        ); generalColorsFrames .grid(column=1, row=0, sticky="news")

        tk.Label  (generalSizesFrame, text="Длина"                                                                 ).grid(column=0, row=0, sticky="news")
        tk.Label  (generalSizesFrame, text="Контур"                                                                ).grid(column=0, row=1, sticky="news")
        tk.Spinbox(generalSizesFrame, textvariable=generalSizesValues["plus"]["radius"], width=5, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(generalSizesFrame, textvariable=generalSizesValues["plus"]["width"],  width=5, from_=0, to=20000).grid(column=1, row=1)
        # ---------------------------
        (             tk.Label (generalColorsFrames, text="Плюс"                                                                                                                                                     ).grid(column=0, row=1))
        (             tk.Label (generalColorsFrames, text="Фон"                                                                                                                                                      ).grid(column=0, row=0))
        generalPLUS = tk.Button(generalColorsFrames, text="***", fg="white", bg=generalColorsValues["plus"].get(), command=lambda element="plus": self._changeColor(generalColorsValues[element], generalPLUS)); generalPLUS.grid(column=1, row=1)
        generalBG   = tk.Button(generalColorsFrames, text="***", fg="white", bg=generalColorsValues["bg"  ].get(), command=lambda element="bg"  : self._changeColor(generalColorsValues[element], generalBG  )); generalBG  .grid(column=1, row=0)

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
        tk.Label  (taskExperimentFrame, text="Имя испытуемого"                                             ).grid(column=0, row=2)
        tk.Label  (taskExperimentFrame, text="Код испытуемого"                                             ).grid(column=0, row=3)
        tk.Entry  (taskExperimentFrame, textvariable=experimentConfig["name" ], width=10,                  ).grid(column=1, row=2)
        tk.Entry  (taskExperimentFrame, textvariable=experimentConfig["code" ], width=10,                  ).grid(column=1, row=3)
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
        mouseExperiment     = mouseConfig["experiment"]
        mouseGraphicsSizes  = mouseGraphics["sizes"]
        mouseGraphicsColors = mouseGraphics["colors"]
        mouseExpFrame      = tk.LabelFrame(mouseTab, text="Настройка эксперимента"   ); mouseExpFrame     .grid(column=0, row=0, sticky="news", rowspan=3)
        mouseControlFrame  = tk.LabelFrame(mouseTab, text="Управление"               ); mouseControlFrame .grid(column=1, row=0, sticky="news")
        mouseDelaysFrame   = tk.LabelFrame(mouseTab, text="Time Delays"              ); mouseDelaysFrame  .grid(column=1, row=1, sticky="news")
        mouseLoggerFrame   = tk.LabelFrame(mouseTab, text="Logger"                   ); mouseLoggerFrame  .grid(column=1, row=2, sticky="news")
        mouseGraphicsFrame = tk.LabelFrame(mouseTab, text="Графика"                  ); mouseGraphicsFrame.grid(column=2, row=0, sticky="news", rowspan=3)

        # ------- ExperimentFrame
        mousesSizesFrame  = tk.LabelFrame(mouseExpFrame, text="Размеры"); mousesSizesFrame .grid(column=0, row=1, columnspan=2, sticky="news")

        mousesRoundFrame  = tk.LabelFrame(mouseExpFrame, borderwidth=10); mousesRoundFrame .grid(column=0, row=0, columnspan=2, sticky="news")
        tk.Label  (mousesRoundFrame, text="Кол-во трайлов\nв группе"                                         ).grid(column=0, row=0)
        tk.Label  (mousesRoundFrame, text="Кол-во групп"                                                     ).grid(column=0, row=1)
        tk.Spinbox(mousesRoundFrame, textvariable=mouseExperiment["countInGroup"], width=5, from_=1, to=20000).grid(column=1, row=0)
        tk.Spinbox(mousesRoundFrame, textvariable=mouseExperiment["countOfGroup"], width=5, from_=0, to=20000).grid(column=1, row=1)

        # ------- controlFrame ---------------------
        tk.Label      (mouseControlFrame, text="Инверсия?"                                                          ).grid(column=0, row=0)
        tk.Label      (mouseControlFrame, text="Чуствительность"                             ).grid(column=0, row=1)
        tk.Checkbutton(mouseControlFrame,     variable=mouseControlConfig["inverse"    ], onvalue=1, offvalue=0     ).grid(column=1, row=0)
        tk.Spinbox    (mouseControlFrame, textvariable=mouseControlConfig["sensitivity"], from_=0, to=20000, width=5).grid(column=1, row=1)
        # ----------- durationFrame --------------------
        tk.Label  (mouseDelaysFrame, text="Plus Time"                                                                        ).grid(column=0, row=0)
        tk.Spinbox(mouseDelaysFrame, textvariable=mouseConfig["duration"]["plus"], width=5, increment=0.01, from_=0, to=20000).grid(column=1, row=0)
        # ----------- loggerFrame --------------------
        tk.Label  (mouseLoggerFrame, text="Frequency"                                                                      ).grid(column=0, row=0)
        tk.Spinbox(mouseLoggerFrame, textvariable=mouseConfig["logger"]["freq"], width=5, increment=0.01, from_=0, to=20000).grid(column=1, row=0)
        # ----------- graphics --------------------
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
        tk.Label(mousesColorsFrame, text="Мышь"                 ).grid(column=0, row=0)
        tk.Label(mousesColorsFrame, text="Нора"                 ).grid(column=0, row=1)
        tk.Label(mousesColorsFrame, text="Путь\nСгенерированный").grid(column=0, row=2)
        tk.Label(mousesColorsFrame, text="Путь\nИспытуемого"    ).grid(column=0, row=3)

        mouseMOUSE  = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["mouse" ].get(), command=lambda element="mouse"  : self._changeColor(mouseGraphicsColors[element], mouseMOUSE )); mouseMOUSE .grid(column=1, row=0)
        mouseHOLE   = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["hole"  ].get(), command=lambda element="hole"   : self._changeColor(mouseGraphicsColors[element], mouseHOLE  )); mouseHOLE  .grid(column=1, row=1)
        mouseGTRAIL = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["gtrail"].get(), command=lambda element="gtrail" : self._changeColor(mouseGraphicsColors[element], mouseGTRAIL)); mouseGTRAIL.grid(column=1, row=2)
        mouseSTRAIL = tk.Button(mousesColorsFrame, text="***", fg="white", bg=mouseGraphicsColors["strail"].get(), command=lambda element="strail" : self._changeColor(mouseGraphicsColors[element], mouseSTRAIL)); mouseSTRAIL.grid(column=1, row=3)
        # ======= Task Tab =====================
        taskValues = self.valueFrames["Equation"]
        taskSizesValues    = taskValues["graphics"]["sizes"]
        taskColorsValues   = taskValues["graphics"]["colors"]
        taskFontFamily     = taskValues["graphics"]["font"]
        taskControlConfig  = taskValues["control"]
        taskDurationConfig = taskValues["duration"]
        taskSelectFile     = taskValues["file"]["path"]
        taskExperiment     = taskValues["experiment"]
        # ----------------------------
        taskControlFrame    = tk.LabelFrame(taskTab, text="Управление"    ); taskControlFrame.grid(column=1, row=0, sticky="news")
        taskDelayFrame      = tk.LabelFrame(taskTab, text="Time Delays"); taskDelayFrame     .grid(column=1, row=1, sticky="news")
        taskGraphicsFrame   = tk.LabelFrame(taskTab, text="Графика"    ); taskGraphicsFrame  .grid(column=2, row=0, sticky="news", rowspan=4)
        # ----------- Experiment -------------------
        taskExperimentFrame = tk.LabelFrame(taskTab, text="Настройка эксперимента" ); taskExperimentFrame.grid(column=0, row=0, sticky="news")

        taskRoundFrame  = tk.LabelFrame(taskExperimentFrame, borderwidth=10); taskRoundFrame.grid(column=0, row=0, columnspan=2, sticky="news")
        tk.Label  (taskRoundFrame, text="Кол-во трайлов"                                   ).grid(column=0, row=0)
        tk.Spinbox(taskRoundFrame, textvariable=taskExperiment["round"], width=5,  from_=1, to=20000).grid(column=1, row=0)
        # ----------- fileChoice --------------------
        taskFileFrame       = tk.LabelFrame(taskExperimentFrame, text="File Choice"); taskFileFrame      .grid(column=0, row=1, sticky="news")
        tk.Label (taskFileFrame, text="Choose File:"                                                     ).grid(column=0, row=0)
        tk.Button(taskFileFrame, textvariable=taskSelectFile, command=self._selectFile).grid(column=1, row=0)

        taskSizesFrame   = tk.LabelFrame(taskGraphicsFrame, text="Размеры"                                                                     ); taskSizesFrame  .grid(column=0, row=0, sticky="news")
        (                  tk.Label     (taskGraphicsFrame, text="Тип Шрифта"                                                                  )                  .grid(column=0, row=1, sticky="news"))
        taskFONTTYPE     = tk.Button    (taskGraphicsFrame, text=taskFontFamily.get(), command=lambda: self._changeFont(taskFONTTYPE)); taskFONTTYPE    .grid(column=1, row=1)
        taskColorsFrames = tk.LabelFrame(taskGraphicsFrame, text="Цвета"                                                                       ); taskColorsFrames.grid(column=1, row=0, sticky="news")

        taskSizesSquares = tk.LabelFrame(taskSizesFrame, text="Квадраты"); taskSizesSquares.grid(column=0, columnspan=2, row=1, sticky="news")

        # --------------------------------------------

        tk.Label  (taskSizesSquares, text="Длина"                                                                 ).grid(column=0, row=0)
        tk.Label  (taskSizesSquares, text="Контур"                                                                ).grid(column=0, row=1)
        tk.Spinbox(taskSizesSquares, textvariable=taskSizesValues["squares"]["length"], width=5, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(taskSizesSquares, textvariable=taskSizesValues["squares"]["width" ], width=5, from_=0, to=20000).grid(column=1, row=1)

        tk.Label  (taskSizesFrame, text="Шрифт"                                                     ).grid(column=0, row=2)
        tk.Spinbox(taskSizesFrame, textvariable=taskSizesValues["font"], width=5,  from_=0, to=20000).grid(column=1, row=2)
        # ---------------------------

        tk.Label(taskColorsFrames, text="Шрифт"              ).grid(column=0, row=2)
        tk.Label(taskColorsFrames, text="Квадрат Правильно"  ).grid(column=0, row=3)
        tk.Label(taskColorsFrames, text="Квадрат Неправильно").grid(column=0, row=4)

        taskFONT  = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["font" ].get(), command=lambda element="font"  : self._changeColor(taskColorsValues[element], taskFONT )); taskFONT .grid(column=1, row=2)
        taskRIGHT = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["right"].get(), command=lambda element="right" : self._changeColor(taskColorsValues[element], taskRIGHT)); taskRIGHT.grid(column=1, row=3)
        taskWRONG = tk.Button(taskColorsFrames, text="***", fg="white", bg=taskColorsValues["wrong"].get(), command=lambda element="wrong" : self._changeColor(taskColorsValues[element], taskWRONG)); taskWRONG.grid(column=1, row=4)
        # ------- controlFrame ---------------------
        tk.Label      (taskControlFrame, text="Инверсия?"                              ).grid(column=0, row=0)
        tk.Label      (taskControlFrame, text="Чувствительность\n(1 - размер квадрата)").grid(column=0, row=1)
        tk.Checkbutton(taskControlFrame,     variable=taskControlConfig["inverse"    ], onvalue=1, offvalue=0                  ).grid(column=1, row=0)
        tk.Spinbox    (taskControlFrame, textvariable=taskControlConfig["sensitivity"], width=5, increment=0.1, from_=0.1, to=1).grid(column=1, row=1) 
        # ----------- timeDelays --------------------
        tk.Label  (taskDelayFrame, text="Plus Time"                                                                                     ).grid(column=0, row=0)
        tk.Label  (taskDelayFrame, text="Answer Time"                                                                                   ).grid(column=0, row=1)
        tk.Spinbox(taskDelayFrame, textvariable=taskDurationConfig["plus"  ], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=0)
        tk.Spinbox(taskDelayFrame, textvariable=taskDurationConfig["answer"], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=1)

        # ======= PVT Tab =====================

        pvtValues = self.valueFrames["PVT"]
        pvtSizesValues      = pvtValues["graphics"]["sizes" ]
        pvtColorsValues     = pvtValues["graphics"]["colors"]
        pvtDelayValues      = pvtValues["delay"   ]
        pvtExperimentValues = pvtValues["experiment"]

        # ----------------------------
        pvtExperimentFrame = tk.LabelFrame(pvtTab, text="Настройка эксперимента" ); pvtExperimentFrame.grid(column=0, row=0, sticky="news")

        pvtRoundFrame  = tk.LabelFrame(pvtExperimentFrame, borderwidth=10); pvtRoundFrame .grid(column=0, row=0, columnspan=2, sticky="news")
        tk.Label  (pvtRoundFrame, text="Кол-во трайлов"                                            ).grid(column=0, row=0)
        tk.Spinbox(pvtRoundFrame, textvariable=pvtExperimentValues["round"], width=5, from_=1, to=20000).grid(column=1, row=0)
 

        pvtDelayFrame      = tk.LabelFrame(pvtTab, text="Time Delays"); pvtDelayFrame     .grid(column=1, row=0, sticky="news")
        pvtGraphicsFrame   = tk.LabelFrame(pvtTab, text="Графика"    ); pvtGraphicsFrame  .grid(column=2, row=0, sticky="news")

        pvtSizesFrame   = tk.LabelFrame(pvtGraphicsFrame, text="Размеры"); pvtSizesFrame  .grid(column=0, row=0, sticky="news")
        pvtColorsFrames = tk.LabelFrame(pvtGraphicsFrame, text="Цвета"  ); pvtColorsFrames.grid(column=1, row=0, sticky="news")

        pvtCircle =    tk.Label     (pvtSizesFrame, text="Круг"                                                 ); pvtCircle   .grid(column=0, row=0, sticky="news")
        (              tk.Spinbox   (pvtSizesFrame, textvariable=pvtSizesValues["circleRadius"], width=5, from_=0, to=20000   ).grid(column=1, row=0))

        # ---------------------------
        tk.Label(pvtColorsFrames, text="Круг").grid(column=0, row=2)
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
        controlDelayValues  = controlValues["delay"]
        # ----------------------------
        controlDelayFrame    = tk.LabelFrame(controlTab, text="Time Delays"); controlDelayFrame   .grid(column=1, row=0, sticky="news")

        tk.Label  (controlDelayFrame, text="Plus Time"                                                                  ).grid(column=0, row=0)
        tk.Spinbox(controlDelayFrame, textvariable=controlDelayValues["plus"], width=5, increment=0.1, from_=0, to=20000).grid(column=1, row=0)


    # def _apply_dark_theme(self):

    #     # ====== Цветовая палитра ======
    #     BG_MAIN      = "#0f0f12"
    #     BG_SECOND    = "#1a1a1f"
    #     BG_WIDGET    = "#222229"
    #     FG_MAIN      = "#e6e6e6"
    #     FG_DISABLED  = "#777777"
    #     BORDER       = "#2e2e36"
    #     ACCENT       = "#3a7afe"
    #     HOVER        = "#2a2a33"

    #     self.root.configure(bg=BG_MAIN)

    #     style = ttk.Style()
    #     style.theme_use("clam")  # clam лучше всего кастомизируется

    #     # ====== Общие настройки ttk ======
    #     style.configure(".",
    #         background=BG_SECOND,
    #         foreground=FG_MAIN,
    #         fieldbackground=BG_WIDGET,
    #         bordercolor=BORDER,
    #         lightcolor=BORDER,
    #         darkcolor=BORDER,
    #         troughcolor=BG_WIDGET,
    #         selectbackground=ACCENT,
    #         selectforeground="white",
    #         insertcolor=FG_MAIN,
    #         relief="flat"
    #     )

    #     # ====== Notebook ======
    #     style.configure("TNotebook",
    #         background=BG_MAIN,
    #         borderwidth=0
    #     )

    #     style.configure("TNotebook.Tab",
    #         background=BG_WIDGET,
    #         foreground=FG_MAIN,
    #         padding=(10, 5)
    #     )

    #     style.map("TNotebook.Tab",
    #         background=[("selected", BG_SECOND)],
    #         foreground=[("selected", "white")]
    #     )

    #     # ====== Frame ======
    #     style.configure("TFrame",
    #         background=BG_SECOND
    #     )

    #     # ====== Label ======
    #     style.configure("TLabel",
    #         background=BG_SECOND,
    #         foreground=FG_MAIN
    #     )

    #     # # ====== Button ======
    #     # style.configure("TButton",
    #     #     # background=BG_WIDGET,
    #     #     foreground=FG_MAIN,
    #     #     borderwidth=1,
    #     #     focusthickness=2,
    #     #     padding=6,
    #     #     focuscolor="white",
    #     #     relief="flat"
    #     # )

    #     # style.map("TButton",
    #     #     # background=[("active", HOVER)],
    #     #     foreground=[("disabled", FG_DISABLED)]
    #     # )

    #     # ====== Checkbutton ======
    #     style.configure("TCheckbutton",
    #         background=BG_SECOND,
    #         foreground=FG_MAIN
    #     )

    #     style.map("TCheckbutton",
    #         foreground=[("disabled", FG_DISABLED)]
    #     )

    #     # ====== Entry ======
    #     style.configure("TEntry",
    #         fieldbackground=BG_WIDGET,
    #         foreground=FG_MAIN,
    #         bordercolor=BORDER,
    #         insertcolor=FG_MAIN
    #     )

    #     # =====================================================
    #     # tk.* виджеты (НЕ ttk) — настраиваются вручную
    #     # =====================================================

    #     def style_widget(widget):
    #         cls = widget.__class__.__name__

    #         if cls in ("LabelFrame",):
    #             widget.configure(
    #                 bg=BG_SECOND,
    #                 fg=FG_MAIN,
    #                 highlightbackground=BORDER,
    #                 highlightcolor=ACCENT
    #             )

    #         elif cls in ("Label",):
    #             widget.configure(
    #                 bg=BG_SECOND,
    #                 fg=FG_MAIN
    #             )

    #         elif cls in ("Spinbox", "Entry"):
    #             widget.configure(
    #                 bg=BG_WIDGET,
    #                 fg=FG_MAIN,
    #                 insertbackground=FG_MAIN,
    #                 selectbackground=ACCENT,
    #                 selectforeground="white",
    #                 highlightbackground=BORDER,
    #                 highlightcolor=ACCENT,
    #                 relief="flat"
    #             )

    #         elif cls in ("OptionMenu",):
    #             widget.configure(
    #                 bg=BG_WIDGET,
    #                 fg=FG_MAIN,
    #                 activebackground=HOVER,
    #                 activeforeground="white",
    #                 highlightbackground=BORDER
    #             )
    #             widget["menu"].configure(
    #                 bg=BG_WIDGET,
    #                 fg=FG_MAIN,
    #                 activebackground=ACCENT,
    #                 activeforeground="white"
    #             )

    #         elif cls in ("Checkbutton",):
    #             widget.configure(
    #                 bg=BG_SECOND,
    #                 fg=FG_MAIN,
    #                 selectcolor=BG_WIDGET,
    #                 activebackground=BG_SECOND,
    #                 activeforeground=FG_MAIN
    #             )

    #         elif cls == "Button":
    #             widget.configure(
    #                 fg=FG_MAIN,
    #                 bd=0,                     # убираем системную рамку
    #                 # relief="flat",            # убираем 3D-эффект
    #                 highlightthickness=6,     # толщина белого контура
    #                 # highlightbackground="white",  # цвет контура
    #                 # highlightcolor="white"    # чтобы не менялся при фокусе
    #             )

    #         for child in widget.winfo_children():
    #             style_widget(child)

    #     style_widget(self.root)

    def run(self):
        self.root.mainloop()
        return self.result

def run():
    menu = MainMenu()
    return menu.run()

if __name__ == "__main__":
    run()