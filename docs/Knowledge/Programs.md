All Crosses are WHITE
GUI:
- Config
	- Last Program : String
Common config:
- Graphics:
	- Screen Mode (Windowed, Fullscreen) : Boolean
	- Screen size : Int, Int
	- Control: Normal, Inverse : Boolean
	- Sensivity : Int
- Logger
	- ФИО : String
	- Код Испытуемого : String
- Alarm(Tone)
	- Enable (0/1) : Boolean
	- Frequency : Int
	- Volume : Int 
	- Delay : Int
- Number of Rounds : Int

- Mouse:
	- Config:
		- Graphics
			- Radius of Hole : Int 
			- Radius of Mouse? (there is limitation)
			- Radius of Possibilities Zone
			- Velocity of Mouse
		- Logger
			- Coordinate write frequence
	- Graphics:
		- Circles
	- TimeStamps:
		1. Alarm
		2n. Start Round (n - number of round)
		6n. First Reaction (n - number of round)
		8. End
	- Logger:
		- Images:
			- Trails (Зеленый - испытуемый, Синий - исходный)
		- Text:
			- Coordinates (Исходный, Пользователя)
			- Main Log
				- For each Round (FileName: )
					- Round Number
					- Reaction Time
					- Right/Wrong/Missed
					- Number of Wheel Notches
					- Процент путь в Оптимальной Области
					- Длины Зеленой и Идеальной Зеленой 
					- Финальные координаты
				- For All (FileName: )
					- Hit
					- Missed
					- Display resolution
- Equations
	- Config
		- Cross Time
		- Filename of Block 
		- Round Max Time
	- Graphics:
		- Text
		- Squares
		- Cross (From Beginning)
	- TimeStamps:
		1. Alarm
		3n. Start Round (n - number of round) 
		6n. First Reaction (n - number of round)
		8. End 
	- Logger:
		- For each (FileName: )
			- Round Number
			- Equation
			- Оценка_примера
			- Ответил
				- True
				- False
				- Slept (Missed)
			- Вывод
				- True (True is True and False is False)
				- False (True is False and False is True)
				- Missed (Missed)
			- Reaction Time
		- For All (FileName: )
			- Filename of Block
			- Number of Right and Wrong equations
			- T->T F->F T->F F->T Missed
- PVT (Cross (0.5) -> Empty (2-4 sec) -> Red Circle (3 sec) -> Empty (0.5 sec) -> Next Round )
	- Config
		- Cross time: $n$ sec
		- Empty time $[a,b]$ sec 
		- Circle time: $m$ sec
		- EmptyAfterCircle (**M**id**S**timule**I**nterval): $k$ sec
	- Graphics:
		- Circle (Red)
		- Cross
	- TimeStamps
		1. Alarm
		4n. Start Round With Cross (n - number of round)
		5n. Circle Appears (n - Round Number)
		6n. First Reaction After Circle Appeares (n - number of round)
		8. End
	- Logger:
		- For each (FileName: )
			- Round Time (From Cross to Cross)
			- Round Number
			- Reaction Time
			- Hit or Missed
		- For All (FileName: )
		- 
			- Count of Hits
			- Percentage of Hit to All
			- Mean of Reaction Time \*
- Control Arousal
	- Config
		- Cross Time: $m$ sec
	- Graphics:
		- Cross
	- TimeStamps
		1. Alarm
		6. Touch da button	
		7. Start (Cross appearance)
		8. End
---

Добавить, изменить

- Цифры светло серые 
- Крест вместо точки
- Фон по темнее
- Парабола - траектория, скорость **постоянна**
- Equations:
	- Round Time is constant (Solve + Wait = Round Time)

---
1. Siren
2. Plus - `plusTime = 2` 
	1. C_bg
	2. c_plus
	3. len_plus
	4. width_plus
	

