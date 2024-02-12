import os
from tkinter import *
from tkinter import filedialog
# get settings from configuration file
configstd={
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
            "dot_time":0.5,
            "time":5, 

            }

config={}
if not(os.path.exists("config.txt")):
    config=configstd
#-----------------------------------
    f=open("config.txt", "w")
    for i in config:
        f.write(str(i)+" "+str(config[i])+"\n")
    f.close()
#-----------------------------------
else:
    f=open("config.txt", "r")
    for i in f:
        try:
            if '\n' in i:
                config.update({i.split(" ")[0]:i.split(" ")[1][:-1]}) 
            else:
                config.update({i.split(" ")[0]:i.split(" ")[1]}) 
        except Exception as e:
            pass
    
    for i in configstd.keys():
        if not(i in config.keys()):
            config.update({i:configstd.get(i)}) 
        
#====================================================#
print(config)
start_prog=False
root = Tk()
root.resizable(False, False)
root.title('Окно конфигураций')

lbl=[[],(13,18,17,20),("Главные настройки", "Тон пробуждения", "Мыши","Задачки"),
    ("Режим окна:","Ширина (пикс.): ","Высота (пикс.): ","Управление: ","Программа: ","Кол-во опытов: "),
    ("Включение тона", "Частота тона (Гц)", "Громкость тона %","Длительность тона (с.)"),
    ("Множ. сумм радиусов (пикс.)","Зона ожидания (пикс.)", "Частота записи (с.)"),
    ("Чувствительность мыши (пикс.)","Время ожидания (c.)","Время ответа (c.)")]

for i in range(len(lbl[2])):
  lbl[0].append(LabelFrame(root, text=lbl[2][i]))
  lbl[0][i].grid(column=i%2, row=i//2, sticky="NEWS", padx=5, pady=5)

for i in range(len(lbl[0])):
  for j in range(len(lbl[3+i])):
    Label(lbl[0][i],text=lbl[3+i][j]).grid(column=0, row=j, sticky="NEWS")
#------------------------------------------------------------------------------------------------

def select_file():
    global file
    filetypes = (('.txt файлы', '*.txt'), ('Все файлы', '*.*'))
    file = filedialog.askopenfilename(title='Выберите файл', initialdir='/', filetypes=filetypes)
    show_file["text"]=file

def ableTone():
  global enable, wids
  for i in wids[1][1:]:
    if enable.get()==0:
      i["state"]="disable"
    else:
      i["state"]="normal"

file="None"

mode = StringVar()
ctrl = StringVar()
prog = StringVar()
enable = IntVar()

lst = [["Оконный", "Экранный"], ["Задачки", "Мыши"], ["Обычное", "Инверсия"]]

wids=[[OptionMenu(lbl[0][0], mode, *lst[0]),
       Spinbox(lbl[0][0], from_= 0, to = 2560),
       Spinbox(lbl[0][0], from_= 0, to = 1440),
       OptionMenu(lbl[0][0], ctrl, *lst[2]),
       OptionMenu(lbl[0][0], prog, *lst[1]),
       Spinbox(lbl[0][0], from_= 0, to = 1440)],

      [Checkbutton(lbl[0][1],variable = enable, onvalue = 1, offvalue = 0, command=ableTone),
       Spinbox(lbl[0][1], from_= 0, to = 20000),
       Spinbox(lbl[0][1], from_= 0, to = 50000),
       Spinbox(lbl[0][1], from_= 0, to = 1000)],
      [Spinbox(lbl[0][2], from_= 0, to = 2560),
       Spinbox(lbl[0][2], from_= 0, to = 5000),
       Spinbox(lbl[0][2], from_= 0, to = 5000)],
      [Spinbox(lbl[0][3], from_= 0, to = 2560),
       Spinbox(lbl[0][3], from_= 0, to = 1440),
       Spinbox(lbl[0][3], from_= 0, to = 2560),
       Button(lbl[0][3], text="Выбор файла",relief="raised", command=select_file)]]

s=list(config.keys())
n=5
for i in wids:
    for j in i:
        if type(j) is Spinbox:
          j.delete(0,"end")
          j.insert(1,config[s[n]])
#          print(s[n])
          n+=1

mode.set(config["screen"])
ctrl.set(config["control"])
prog.set(config["program"])
enable.set(config["tone_play"])

ableTone()

for i in wids:
  for j in range(len(i)):
    if type(i[j]) is Button:
      i[j].grid(column=0, columnspan=2,row=j, sticky="NEWS")
    else:
      i[j].grid(column=1,row=j, sticky="news")

    i[j].config(width=10, relief="groove")
show_file=Label(lbl[0][3], wraplength=340, text=config["file"])
show_file.grid(column=0,columnspan=2,rowspan=2,row=4, sticky="NEWS")
#---------------------------------------------------------------------------------------
def start():
  global start_prog
  s=list(config.keys())
  n=5
  print("-----------------")
  for i in wids:
    for j in range(len(i)):
      if type(i[j]) is Spinbox:
        config[s[n]]=i[j].get()

        n+=1
  config["control"]=ctrl.get()
  config["screen"]=mode.get()
  config["program"]=prog.get()
  config["tone_play"]=enable.get()
  config["file"]=file    
#-----------------------------------
  f=open("config.txt", "w")
  for i in config:
      f.write(str(i)+" "+str(config[i])+"\n")
  f.close()
#-----------------------------------
  start_prog=True
  root.destroy()

done=Button(root, text="Начать Эксперимент", relief="groove", command=start)
done.grid(column=0, row=2, columnspan=2, sticky="NEWS")
root.mainloop()
