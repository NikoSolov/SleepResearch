import numpy as np
import pyray as pr
import config as cfg
from enum import Enum, auto
import os
import glob
from icecream import ic

class GraphicsEvents(Enum):
    windowClose  = auto()
    spacePressed = auto()
    mousePressed = auto()
    mouseWheel   = auto()

SAMPLE_RATE = 44100

# import sounddevice as sd
# class Sound:
#     def __init__(self, volume: int, freq: float):
#         amplitude = volume / 100.0
#         t = np.arange(SAMPLE_RATE) / SAMPLE_RATE
#         mono = (amplitude * np.sin(2.0 * np.pi * freq * t)).astype(np.float32)
#         self._data = np.column_stack([mono, mono])

#     def play(self):
#         print("play")
#         sd.play(self._data, samplerate=SAMPLE_RATE, loop=True,
#                 blocksize=8, latency="low")
    
#     def update(self):
#         pass

#     def stop(self):
#         sd.stop()

class Sound:
    def __init__(self, volume_percent: float, freq: float):
        self._freq    = freq
        self._volume  = volume_percent / 100.0
        self._playing = False
        self._phase   = 0

        pr.init_audio_device()
        self._frame_count = 4096
        pr.set_audio_stream_buffer_size_default(self._frame_count)
        self._stream = pr.load_audio_stream(SAMPLE_RATE, 16, 1)
        pr.set_audio_stream_volume(self._stream, self._volume)

    def _fill(self, frame_count: int):
        t = (self._phase + np.arange(frame_count)) / SAMPLE_RATE
        samples = (32767 * np.sin(2.0 * np.pi * self._freq * t)).astype(np.int16)
        self._phase = (self._phase + frame_count) % SAMPLE_RATE

        buf = pr.ffi.new(f'short[{frame_count}]')
        for i, s in enumerate(samples):
            buf[i] = int(s)

        pr.update_audio_stream(self._stream, buf, frame_count)

    def play(self):
        if not self._playing:
            self._fill(self._frame_count)
            pr.play_audio_stream(self._stream)
            self._playing = True

    def update(self):
        if not self._playing:
            return
        if pr.is_audio_stream_processed(self._stream):
            self._fill(self._frame_count)

    def stop(self):
        if self._playing:
            pr.stop_audio_stream(self._stream)
            self._playing = False

    def unload(self):
        pr.unload_audio_stream(self._stream)


def _color(hex_or_list):
    h = hex_or_list.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return pr.Color(r, g, b, 255)

def _resolve_system_font(family: str) -> str | None:
    dirs = ["C:/Windows/Fonts", "/usr/share/fonts", "/Library/Fonts"]
    for d in dirs:
        for path in glob.glob(f"{d}/**/*.ttf", recursive=True) + \
                    glob.glob(f"{d}/**/*.otf", recursive=True):
            if family.lower().replace(" ", "") in \
               os.path.basename(path).lower().replace(" ", ""):
                return path
    return None

class Graphics:
    def __init__(self, program: str, lightSensor):
        cfg.loadConfig()
        config = cfg.getConfig()
        # ------------------------------------------------------------------
        self.WIN_SIZE = pr.Vector2(
            config["general"]["window"]["width"], 
            config["general"]["window"]["height"]
        )
        pr.set_trace_log_level(pr.TraceLogLevel.LOG_WARNING)
        pr.init_window(
            int(self.WIN_SIZE.x), int(self.WIN_SIZE.y),
            program,
        )
        if config["general"]["window"]["fullScreen"]:
            pr.toggle_fullscreen()
        pr.set_target_fps(60)
        # pr.disable_cursor()
        # ------------------------------------------------------------------
        self.lightSensor     = lightSensor
        self.lightSensorSize = config["general"]["timeStamps"]["lightSize"]
        self.program         = program

        self.generalGraphicDict = config["general"]["graphics"]
        self.generalColorDict   = self.generalGraphicDict["colors"]
        self.generalSizeDict    = self.generalGraphicDict["sizes"]

        if self.program != "Control":
            self.programGraphicDict = config[self.program]["graphics"]
            self.programColorDict   = self.programGraphicDict["colors"]
            self.programSizeDict    = self.programGraphicDict["sizes"]

        # Шрифт для Equation
        self._font: pr.Font | None = None
        if program == "Equation":
            # font_name = self.programGraphicDict.get("font", "")
            font_name = _resolve_system_font("Comic")
            font_size = self.programSizeDict.get("font", 200)
            self._font = (
                pr.load_font_ex(font_name, font_size, pr.ffi.NULL, 0)
                if font_name
                else pr.get_font_default()
            )

    def _fill(self):
        pr.draw_rectangle_rec(
            pr.Rectangle(0,0,self.WIN_SIZE.x, self.WIN_SIZE.y), pr.BLACK
        )

    def drawInit(self):
        pr.begin_drawing()
        pr.clear_background(_color(self.generalColorDict["bg"]))
        if self.lightSensor.LIGHT_ENABLE:
            pr.draw_rectangle_rec(
                pr.Rectangle(0, 0, self.lightSensorSize, self.lightSensorSize),
                pr.WHITE if self.lightSensor.lightUp() else pr.BLACK
            )

    def drawPlus(self):
        C_PLUS = _color(self.generalColorDict["plus"])
        S_PLUS_RADIUS = self.generalSizeDict["plus"]["radius"]
        S_PLUS_WIDTH  = self.generalSizeDict["plus"]["width"]

        pr.draw_line_ex(
            pr.vector2_add(pr.vector2_scale(self.WIN_SIZE, 0.5), pr.vector2_scale(pr.Vector2(0, -1), S_PLUS_RADIUS)),
            pr.vector2_add(pr.vector2_scale(self.WIN_SIZE, 0.5), pr.vector2_scale(pr.Vector2(0,  1), S_PLUS_RADIUS)),
            S_PLUS_WIDTH, C_PLUS
        )
        pr.draw_line_ex(
            pr.vector2_add(pr.vector2_scale(self.WIN_SIZE, 0.5), pr.vector2_scale(pr.Vector2(-1, 0), S_PLUS_RADIUS)),
            pr.vector2_add(pr.vector2_scale(self.WIN_SIZE, 0.5), pr.vector2_scale(pr.Vector2( 1, 0), S_PLUS_RADIUS)),
            S_PLUS_WIDTH, C_PLUS
        )

    def drawControl(self, status, Event):
        self.drawInit()
        match status:
            case Event.Siren:
                self._fill()
            case Event.Plus:
                self.drawPlus()
        self.update()

    def drawPVT(self, status, Event):
        self.drawInit()
        match status:
            case Event.Siren:
                self._fill()
            case Event.Plus:
                self.drawPlus()
            case Event.Circle:
                pr.draw_circle_v(
                    pr.vector2_scale(self.WIN_SIZE, 0.5),
                    self.programSizeDict["circleRadius"],
                    _color(self.programColorDict["circle"])
                )

        self.update()

    def drawTasks(self, status, Event, equationText: str,
                  rightLevel: float, wrongLevel: float):
        C_RIGHT = _color(self.programColorDict["right"])
        C_WRONG = _color(self.programColorDict["wrong"])
        C_FONT  = _color(self.programColorDict["font"])
        # FONT = self.programGraphicDict['font']
        
        S_SQR_WIDTH = self.programSizeDict["squares"]["width"]
        S_SQR_LENGTH = self.programSizeDict["squares"]["length"]

        equationFont = self._font or pr.get_font_default()
        font_size = int(self.programSizeDict.get("font", 32))

        def drawSquare(
            color = C_RIGHT, 
            pos = (
                pr.vector2_subtract(
                    pr.vector2_scale(self.WIN_SIZE, 0.5),
                    pr.vector2_add(
                        pr.Vector2(0, self.WIN_SIZE.y / 4),
                        pr.vector2_scale(pr.Vector2(1,1), S_SQR_LENGTH // 2)
                    )
                )
            ), 
            sqrHeight = 1, 
            sqrWidth = S_SQR_WIDTH
        ):
            if sqrWidth > 0:
                pr.draw_rectangle_lines_ex(
                    pr.Rectangle(
                        pos.x, pos.y,
                        S_SQR_LENGTH, 
                        S_SQR_LENGTH * sqrHeight
                    ),
                    sqrWidth,
                    color
                )
            else:
                pr.draw_rectangle_rec(
                    pr.Rectangle(
                        pos.x, pos.y,
                        S_SQR_LENGTH, 
                        S_SQR_LENGTH * sqrHeight
                    ),
                    color
                )
                

        self.drawInit()

        match status:
            case Event.Siren:
                self._fill()
            case Event.Plus | Event.AnswerPlus:
                self.drawPlus()
            case Event.Term | Event.Answer:
                text_w = int(pr.measure_text_ex(equationFont, equationText, font_size, 1).x)
                text_h = int(pr.measure_text_ex(equationFont, equationText, font_size, 1).y)
                pr.draw_text_ex(
                    equationFont, equationText,
                    pr.Vector2(self.WIN_SIZE.x / 2 - text_w // 2,
                               self.WIN_SIZE.y / 2 - text_h // 2),
                    font_size, 1, C_FONT,
                )

        match status:
            case Event.Answer:
                drawSquare(
                    color = C_RIGHT, 
                    pos = (
                        pr.vector2_subtract(
                            pr.vector2_scale(self.WIN_SIZE, 0.5),
                            pr.vector2_add(
                                pr.Vector2(0, self.WIN_SIZE.y / 4),
                                pr.vector2_scale(pr.Vector2(1,1), S_SQR_LENGTH // 2)
                            )
                        )
                    )
                )
                drawSquare(
                    color = C_WRONG, 
                    pos = (
                        pr.vector2_add(
                            pr.vector2_scale(self.WIN_SIZE, 0.5),
                            pr.vector2_subtract(
                                pr.Vector2(0, self.WIN_SIZE.y / 4),
                                pr.vector2_scale(pr.Vector2(1,1), S_SQR_LENGTH // 2)
                            )
                        )
                    )
                )

                drawSquare(
                    color = C_RIGHT, 
                    pos = (
                        pr.vector2_subtract(
                            pr.vector2_scale(self.WIN_SIZE, 0.5),
                            pr.vector2_add(
                                pr.Vector2(0, self.WIN_SIZE.y / 4),
                                pr.vector2_scale(pr.Vector2(1, 2*rightLevel-1), S_SQR_LENGTH // 2)
                            )
                        )
                    ),
                    sqrWidth = 0,
                    sqrHeight = rightLevel
                )
                drawSquare(
                    color = C_WRONG, 
                    pos = (
                        pr.vector2_add(
                            pr.vector2_scale(self.WIN_SIZE, 0.5),
                            pr.vector2_subtract(
                                pr.Vector2(0, self.WIN_SIZE.y / 4),
                                pr.vector2_scale(pr.Vector2(1,1), S_SQR_LENGTH // 2)
                            )
                        )
                    ),
                    sqrWidth = 0,
                    sqrHeight = wrongLevel
                )

        self.update()

    def drawMouses(self, status, Event, BallPos):
        C_MOUSE = _color(self.programColorDict["mouse"])
        C_HOLE  = _color(self.programColorDict["hole"])
        RADIUS  = self.programSizeDict["radius"]

        self.drawInit()

        # -------- draw a hole ----------
        if status is not Event.plus:
            pr.draw_circle_v(
                pr.Vector2(self.WIN_SIZE.x - RADIUS, RADIUS),
                RADIUS,
                C_HOLE
            )

        match status:
            case Event.siren:
                self._fill()
            case Event.answer:
                pr.draw_circle_v(pr.Vector2(*BallPos), RADIUS, C_MOUSE)
            case Event.plus:
                self.drawPlus()

        self.update()

    def update(self):
        pr.end_drawing()

    def close(self):
        if self._font:
            pr.unload_font(self._font)
        pr.close_audio_device()
        pr.close_window()

    def get_events(self):
        graphics_events = []
        if (pr.window_should_close() or pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE)):
            graphics_events.append(GraphicsEvents.windowClose)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_SPACE):
            graphics_events.append(GraphicsEvents.spacePressed)
        if (
            pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_LEFT) or
            pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_MIDDLE) or
            pr.is_mouse_button_pressed(pr.MouseButton.MOUSE_BUTTON_RIGHT)
        ):
            graphics_events.append(GraphicsEvents.mousePressed)
            print("Clicked")

        if pr.get_mouse_wheel_move() != 0:
            graphics_events.append(GraphicsEvents.mouseWheel)
            print(self.get_wheel())
        return graphics_events

    def get_wheel(self):
        return pr.get_mouse_wheel_move()