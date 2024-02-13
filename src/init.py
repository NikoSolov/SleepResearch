import os

import xlsxwriter

import config as cfg

import menu

# ==============================================================================================
config = cfg.getConfig()
print(config)
import pygame as pg
import numpy
import serial.tools.list_ports
import time
from random import uniform

# =========== GET ALL CONFIG CONSTANTS ==========
WIN_WIDTH = config["general"]["window"]["width"]
WIN_HEIGHT = config["general"]["window"]["height"]
FULLSCREEN = config["general"]["window"]["fullScreen"]
ROUND = config["general"]["experiment"]["round"]
PROGRAM = config["general"]["experiment"]["program"]
LIGHT_SIZE = config["general"]["timeStamps"]["lightSize"]

pg.mixer.init(44100, -16, 2, 512)
pg.init()

if not (os.path.exists("result")):
    os.mkdir("result")

# initialize window

if int(FULLSCREEN):
    root = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.FULLSCREEN)
else:
    root = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pg.time.Clock()

# initialize COM-Port
port_work = True
portname = ""
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    if "USB-SERIAL CH340" in desc:
        portname = port
if portname == "":  port_work = False

try:
    time_code = serial.Serial(port=portname, baudrate=9600, timeout=.1)
    time.sleep(2)
except Exception as e:
    port_work = False
#    print(e)

# create the siren's sample
TONE = config["general"]["tone"]
arr = numpy.array(
    [int(TONE["volume"]) * numpy.sin(2.0 * numpy.pi * int(TONE["freq"]) * x / 44100) for x in
     range(0, 44100)]).astype(numpy.int16)
arr2 = numpy.c_[arr, arr]
sound = pg.sndarray.make_sound(arr2)
start_prog = True
# play tone
if int(TONE["enable"]) and start_prog == True:  # and port_work==True:
    print("play")
    if port_work: time_code.write(bytearray([1]))
    sound.play(-1)
    pg.time.wait(int(float(TONE["delay"]) * 1000))
    sound.stop()

# set to start program
main = True
# -----------------------------------------------------------------
# -----------------------------------------------------------------
if start_prog == True:

    if PROGRAM == "Equation":
        from textGen import Gen

        # ============ GET ALL CONSTANTS =========
        DIR_NAME = "Tasks " + time.strftime("%d.%m.%y %H.%M.%S")
        FILEPATH = config["Equation"]["file"]["path"]
        PLUS_TIME = config["Equation"]["delay"]["plus"]
        ANSWER_TIME = config["Equation"]["delay"]["answer"]
        CONTROL = config["Equation"]["control"]
        print(f"CONTROL: {CONTROL}")
        # =========================================
        roundi = 0

        pg.font.init()
        myfont = pg.font.SysFont('Comic Sans MS', 150)

        r = w = TT = FF = TF = FT = missed = 0
        sqr = 200
        red = 0
        green = 0

        log = []
        answer = True

        fill = 0
        fillstep = 1
        new = True
        file_not = False
        dot_flag = True


        class sqr():
            intances = []

            def __init__(self, x, y, size, color, fill=0):
                self.x = x
                self.y = y
                self.size = size
                self.color = color
                self.fill = fill
                sqr.intances.append(self)

            def draw(self, root):
                pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.size), width=2)
                if self.fill < 0:
                    #    print(self.x, self.size-self.fill, self.size, self.fill)
                    pg.draw.rect(root, self.color, (self.x, self.y + self.size + self.fill, self.size, abs(self.fill)))
                elif self.fill > 0:
                    pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.fill))


        if FILEPATH != "None":
            try:
                fin = open(FILEPATH, "r")
                # print(fin)
            except Exception as e:
                print(e)
                file_not = True

        size = 100
        good = sqr((WIN_WIDTH - size) / 2, WIN_HEIGHT / 4 - size / 2, size, (0, 255, 0))
        bad = sqr((WIN_WIDTH - size) / 2, WIN_HEIGHT * (3 / 4) - size / 2, size, (255, 0, 0))

        while main:

            if new == True:
                root.fill((128, 128, 128))
                pg.draw.circle(root, (255, 255, 255), (WIN_WIDTH // 2, WIN_HEIGHT // 2), (10))
                pg.draw.rect(root, (255, 255, 255), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
                pg.display.update()
                pg.time.wait(int(PLUS_TIME * 1000))

                roundi += 1
                if roundi > ROUND: break
                rtime = 0
                new = False
                pg.event.clear()
                if port_work: time_code.write(bytearray([3]))
                if (FILEPATH != "None") and file_not == False:
                    d = fin.readline()
                    # print(d)
                    if d == "": break
                    d = d.split()
                    text = d[0]
                    res = bool(int(d[1]))
                else:
                    # print("Gen")
                    d = Gen()
                    text = d[2]
                    res = bool(int(d[1]))
                if res == True:
                    r += 1
                else:
                    w += 1
                a = time.time()

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    # if port: time_code.write(bytearray([0]))
                    main = False

                if event.type == pg.MOUSEWHEEL:
                    if rtime == 0:
                        rtime = time.time() - a;
                        print(rtime)
                        if port_work: time_code.write(bytearray([4]))
                    if CONTROL["inverse"]:
                        if event.y < 0:
                            good.fill += event.y * CONTROL["sensitivity"]
                            bad.fill = 0
                        else:
                            bad.fill += event.y * CONTROL["sensitivity"]
                            good.fill = 0
                    else:
                        if event.y > 0:
                            good.fill -= event.y * CONTROL["sensitivity"]
                            bad.fill = 0
                        else:
                            bad.fill -= event.y * CONTROL["sensitivity"]
                            good.fill = 0

            if abs(good.fill) > size or abs(bad.fill) > size:
                if abs(good.fill) > size:
                    log.append([str(roundi), text, str(res), "True", str(res == True), str(round(rtime, 4))])
                    answer = True
                if abs(bad.fill) > size:
                    log.append([str(roundi), text, str(res), "False", str(res == False), str(round(rtime, 4))])
                    answer = False

                if res == True and answer == True:
                    TT += 1
                if res == False and answer == False:
                    FF += 1
                if res == True and answer == False:
                    TF += 1
                if res == False and answer == True:
                    FT += 1

                good.fill = 0
                bad.fill = 0
                new = True

            if time.time() - a > ANSWER_TIME:
                #        time_code.write(bytearray([3,0]))
                rtime = time.time() - a
                log.append([str(roundi), text, str(res), "Missed", "Missed", str(round(rtime, 4))])
                bad.fill = good.fill = 0
                missed += 1
                new = True

            # -----------------------------v
            textSur = myfont.render(text, True, (255, 255, 255))
            root.fill((128, 128, 128))
            pg.draw.rect(root, (0, 0, 0), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
            root.blit(textSur, ((WIN_WIDTH - textSur.get_width()) / 2, (WIN_HEIGHT - textSur.get_height()) / 2))
            good.draw(root)
            bad.draw(root)
            pg.display.update()
            clock.tick(60)
        #    ---------------------------
        #    pg.image.save(root, "vid/"+str(vid)+".png")
        #    images.append(imageio.imread("vid/"+str(vid)+".png"))
        #    vid+=1
        #    ----------------------
        # -----------------------------^
        # imageio.mimsave('vid/movie.gif', images)

        # ==== Create Log SpreadSheet ==================
        TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}.xlsx")
        MainLog = TABLE.add_worksheet("MainLog")
        MainLog.merge_range("A1:B1", "Задачи")
        MainLog.merge_range("C1:G1", "Ответил")
        MainLog.write("A2", "True");
        MainLog.write("B2", "False");
        MainLog.write("C2", "T->T");
        MainLog.write("D2", "F->F");
        MainLog.write("E2", "T->F");
        MainLog.write("F2", "F->T");
        MainLog.write("G2", "Missed")
        MainLog.write("A3", f"{r}");
        MainLog.write("B3", f"{w}");
        MainLog.write("C3", f"{TT}");
        MainLog.write("D3", f"{FF}");
        MainLog.write("E3", f"{TF}");
        MainLog.write("F3", f"{FT}");
        MainLog.write("G3", f"{missed}")
        MainLog.write("A4", "Раунд");
        MainLog.write("B4", "Пример");
        MainLog.write("C4", "Оценка_примера");
        MainLog.write("D4", "Ответил");
        MainLog.write("E4", "Вывод");
        MainLog.write("F4", "Время реакции")
        for i in range(len(log)):
            MainLog.write(f"A{5 + i}", f"{log[i][0]}")
            MainLog.write(f"B{5 + i}", f"{log[i][1]}")
            MainLog.write(f"C{5 + i}", f"{log[i][2]}")
            MainLog.write(f"D{5 + i}", f"{log[i][3]}")
            MainLog.write(f"E{5 + i}", f"{log[i][4]}")
            MainLog.write(f"F{5 + i}", f"{log[i][5]}")
        TABLE.close()
        # fout.write(i[0] + "\t" + i[1] + "\t" + i[2] + "\t\t" + i[3] + "\t" + i[4] + "\t" + i[5] + "\n")

        # fout.write("Задачи\t\t\tОтветил\nTrue\tFalse\t\tT->T\tF->F\tT->F\tF->T\tMissed\n")
        # fout.write(
        #     str(r) + "\t" + str(w) + "\t\t" + str(TT) + "\t" + str(FF) + "\t" + str(TF) + "\t" + str(FT) + "\t" + str(
        #         missed) + "\n")
        # fout.close()


    elif PROGRAM == "Mouse":
        # -----------------------------------------------
        from random import randint

        # ========= GET ALL CONSTANTS ==========
        DIR_NAME = f"Mouse_{time.strftime("%d.%m.%y %H.%M.%S")}"
        WAIT_ZONE = config["Mouse"]["zoneSize"]["waitZone"]
        DISTANCE_MULTIPLIER = config["Mouse"]["zoneSize"]["distMul"]
        LOG_FREQ = config["Mouse"]["logger"]["freq"]
        CONTROL = config["Mouse"]["control"]
        # =======================================
        photo = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
        # -------- Setting Log Files -------------
        if not (os.path.exists("result")):
            os.mkdir("result")
        if not (os.path.exists(f"result/{DIR_NAME}")):
            os.mkdir(f"result/{DIR_NAME}")
        if not (os.path.exists(f"result/{DIR_NAME}/log_img")):
            os.mkdir(f"result/{DIR_NAME}/log_img")
        # --- Setup Excel SpreadSheet -------------
        TABLE = xlsxwriter.Workbook(f"result/{DIR_NAME}/{DIR_NAME}.xlsx")
        # ---- Fill Up Defaults ----------------------
        MainLog = TABLE.add_worksheet("MainLog")
        MainLog.write("A1", "Arrived")
        MainLog.write("B1", "Missed")
        MainLog.merge_range("C1:D1", "Screen Resolution")
        MainLog.write("C2", f"{WIN_WIDTH}")
        MainLog.write("D2", f"{WIN_HEIGHT}")
        MainLog.merge_range("A3:A4", "Round №")
        MainLog.merge_range("B3:B4", "Arrived?")
        MainLog.merge_range("C3:D3", "Length")
        MainLog.merge_range("E3:E4", "Length Difference")
        MainLog.merge_range("F3:F4", "Reaction Time")
        MainLog.merge_range("G3:H3", "Last coord")
        MainLog.write("C4", "Blue")
        MainLog.write("D4", "Green")
        MainLog.write("G4", "x")
        MainLog.write("H4", "y")


        # --------------------------------------------

        # if not (os.path.exists("result/" + DIR_NAME + "/log_txt")):
        #    os.mkdir("result/" + DIR_NAME + "/log_txt")

        class ball():
            x = 0
            r = 40
            y = WIN_HEIGHT - r * 2


        class hole():
            r = 40
            x = WIN_WIDTH - r
            y = r


        class path():
            x = 0
            y = 0


        new = True
        roundData = []
        arrived = 0
        missed = 0
        s = 0
        s2 = 0
        currentRound = 0
        tim = 0

        # ---------------------------------------------
        steps = 0
        while main:
            if new == True:
                steps = 0
                currentRound += 1
                if currentRound > int(ROUND): break
                # ======= Create Position Table ===============================
                ROUND_LOG = TABLE.add_worksheet(f"Trajectories_{currentRound}")
                # ------- Default Headers-------------
                ROUND_LOG.merge_range("A1:C1", "Trajectory")
                ROUND_LOG.write("B2", "Green")
                ROUND_LOG.write("C2", "Blue")
                ROUND_LOG.write("A3", "x")
                ROUND_LOG.write("C3", "y")
                ROUND_LOG.write("B3", "y")
                ROUND_LOG.merge_range("F1:G1", "Screen Resolution")
                ROUND_LOG.write("E1", "Frequency")
                # -------------------------------------
                ROUND_LOG.write("E2", f"{LOG_FREQ}")
                ROUND_LOG.write("F2", f"{WIN_WIDTH}")
                ROUND_LOG.write("G2", f"{WIN_HEIGHT}")
                # ==========================================
                # f = open("result/" + DIR_NAME + "/log_txt/" + str(ri) + ".txt", "w")
                # f.write("Траектории | Разрешение: " + str(WIN_WIDTH) + "x" + str(WIN_HEIGHT) + " | Частота в секундах: " + str(
                #     config["freq"]) + "\n")
                # f.write("Зеленая\t\tСиняя\n")
                # f.write("x\ty\tx\ty\n")
                # =========================================
                rtime = 0
                new = False
                movement = False
                # ---- write timeStamps -----------------
                if port_work: time_code.write(bytearray([2]))
                # ---- Create PATH_SURFACE --------------
                photo.fill((128, 128, 128))
                pg.draw.circle(photo, (0, 0, 0), (hole.x, hole.y), hole.r)
                pg.draw.rect(photo, (255, 0, 0), (0, WIN_HEIGHT - WAIT_ZONE, WAIT_ZONE, WAIT_ZONE), width=2)
                # ------------------------------
                s = 0
                s2 = 0

                # -norm------------------------------------------------v
                ball.x, ball.y = ball.r, WIN_HEIGHT - ball.r
                path.x, path.y = ball.x + ball.r / 2, ball.y - ball.r / 2
                # -------------------------------------------------^

                m = randint(1, 4)
                x1, y1 = WIN_WIDTH - (2 * hole.r + ball.r), ball.r
                x2, y2 = WIN_WIDTH - ball.r, ball.r + 2 * hole.r
                # -----------------------------------------------
                if m == 1:
                    c = (y1 - ball.y) / ((x1 - ball.x) ** 2)
                    c = uniform(c, c + c / 2)
                    delta_y = lambda: 2 * c * (ball.x - ball.r)
                if m == 2:
                    c = (y2 - ball.y) / ((x2 - ball.x) ** 2)
                    c = uniform(c, c - c / 2)
                    delta_y = lambda: 2 * c * (ball.x - ball.r)
                if m == 3:
                    c = (ball.y - y1) / ((x1 - ball.x) ** 2)
                    c = uniform(c, c + c / 2)
                    delta_y = lambda: 2 * c * (ball.x - x1)
                if m == 4:
                    c = (ball.y - y2) / ((x2 - ball.x) ** 2)
                    c = uniform(c - c / 2, c)
                    delta_y = lambda: 2 * c * (ball.x - x2)
                atime = tim = time.time()
            # -----------------------------------------------------v
            det_x, det_y = ball.x + ball.r / 2, ball.y - ball.r / 2
            det2_x, det2_y = path.x, path.y
            # -----------------------------------------------------^

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    #            if port_work: time_code.write(bytearray([0]))
                    main = False
                if event.type == pg.MOUSEWHEEL and (ball.x > WAIT_ZONE or ball.y < WIN_HEIGHT - WAIT_ZONE):
                    if rtime == 0:
                        rtime = time.time() - atime;
                        print(rtime)
                        if port_work: time_code.write(bytearray([4]))
                    movement = True
                    if CONTROL["inverse"]:
                        ball.y += event.y * 20
                    else:
                        ball.y -= event.y * 20

            # -----------------------------------------------------------------------------------------------------------------v
            #    print((time()-tim))

            if (time.time() - tim) > float(LOG_FREQ):
                tim = time.time()
                #        print("check")
                # f.write(str(int(ball.x + ball.r / 2)) + "\t" + str(int(ball.y - ball.r / 2)) + "\t" + str(
                #     int(path.x)) + "\t" + str(int(path.y)) + "\n")
                ROUND_LOG.write(f"A{steps + 4}", int(ball.x + ball.r / 2))
                ROUND_LOG.write(f"B{steps + 4}", int(ball.y - ball.r / 2))
                # ROUND_LOG.write(f"C{steps + 4}", int(Path["x"]))
                ROUND_LOG.write(f"C{steps + 4}", int(path.y))

                steps += 1

            ball.y += delta_y() * 5
            ball.x += 5
            path.y += delta_y() * 5
            path.x += 5

            root.fill((128, 128, 128))
            if not (ball.x > WAIT_ZONE or ball.y < WIN_HEIGHT - WAIT_ZONE):
                pg.draw.rect(root, (255, 255, 255), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
            if (ball.x > WAIT_ZONE or ball.y < WIN_HEIGHT - WAIT_ZONE):
                pg.draw.rect(root, (0, 0, 0), (0, 0, LIGHT_SIZE, LIGHT_SIZE))
            pg.draw.circle(root, (0, 0, 0), (hole.x, hole.y), hole.r)
            pg.draw.circle(root, (128, 0, 0), (ball.x, ball.y), ball.r)
            # ------------------------------------------------------------------------------------------------------------------v
            pg.draw.line(photo, (0, 255, 0), (det_x, det_y), (ball.x + ball.r / 2, ball.y - ball.r / 2), 2)
            pg.draw.rect(photo, (0, 0, 255), (path.x, path.y, 3, 3))
            # -------------------------------------------------------------------------------------------------------------------^

            pg.display.update()
            #    ---------------------------
            #    pg.image.save(root, "vid/"+str(vid)+".png")
            #    images.append(imageio.imread("vid/"+str(vid)+".png"))
            #    vid+=1
            #    ----------------------
            clock.tick(60)

            s += (((ball.x + ball.r / 2) - det_x) ** 2 + ((ball.y - ball.r / 2) - det_y) ** 2) ** (1 / 2)
            s2 += ((path.x - det2_x) ** 2 + (path.y - det2_y) ** 2) ** (1 / 2)

            l = ((ball.x - hole.x) ** 2 + (ball.y - hole.y) ** 2) ** (1 / 2)
            flag = (l <= DISTANCE_MULTIPLIER * ball.r)
            if (ball.x + ball.r > WIN_WIDTH or ball.y + ball.r > WIN_HEIGHT or ball.y - ball.r < 0) or flag:
                if movement == False: rtime = time.time() - atime
                pg.image.save(photo, "result/" + DIR_NAME + "/log_img/" + str(currentRound) + ".png")
                if movement == False:
                    flag = "Missed"
                else:
                    if flag:
                        arrived += 1
                    else:
                        missed += 1

                roundData.append([flag, round(s), round(s2), int(ball.x), int(ball.y), round(rtime, 4)])
                new = True

        # # imageio.mimsave('vid/movie.gif', images)
        # f = open("result/" + DIR_NAME + "/main_log.txt", "w")
        # f.write("Мыши:\tДобравшиеся\tПропавшие\tДобравшиеся сами\tРазрешение окна: " + str(WIN_WIDTH) + "x" + str(
        #     WIN_HEIGHT) + "\n")
        # f.write("\t" + str(g) + "\t\t" + str(not_g) + "\t\t" + str(a_g) + "\n")
        # f.write("\t\tДлины:\t\t\t\t\tФин. координаты:\n")
        # f.write("Раунд\tПопал\tСиний\tЗеленый\tРазница\tВремя реакции\tx\ty\n")
        # # print(a)
        # for i in range(len(a)):
        #     f.write(str(i + 1) + "\t" + str(a[i][0]) + "\t" + str(a[i][1]) + "\t" + str(a[i][2]) + "\t" + str(
        #         a[i][1] - a[i][2]) + "\t" + str(a[i][5]) + "\t\t" + str(a[i][3]) + "\t" + str(a[i][4]) + "\n")
        # f.close()
        # ------- Filling the Main Log --------------
        MainLog.write("A2", f"{arrived}")
        MainLog.write("B2", f"{missed}")

        for i in range(len(roundData)):
            MainLog.write(i + 4, 0, f"{i + 1}")
            MainLog.write(i + 4, 1, f"{roundData[i][0]}")
            MainLog.write(i + 4, 2, f"{roundData[i][1]}")
            MainLog.write(i + 4, 3, f"{roundData[i][2]}")
            MainLog.write(i + 4, 4, f"{roundData[i][1] - roundData[i][2]}")
            MainLog.write(i + 4, 5, f"{roundData[i][5]}")
            MainLog.write(i + 4, 6, f"{roundData[i][3]}")
            MainLog.write(i + 4, 7, f"{roundData[i][4]}")

        # --- close excel table
        TABLE.close()

if port_work: time_code.write(bytearray([5]))
pg.quit()
