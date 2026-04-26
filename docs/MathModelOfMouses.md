# 1 Выявление требований

Известно, что в этой графической программе должны быть два круга:
- "Мышь" - красный круг, двигающаяся по траектории параболы, с левого нижнего угла к правому верхнему
- "Нора" - черный круг, находящийся в правом верхнем углу экрана, в который должен попасть мышь

Радиус Норы всегда больше или равно радиусу Мыши.

Траектория параболы генерируется так, чтобы Мышь не смогла попасть в Нору

<u>Задача испытуемого</u>: с помощью колесика мыши перемещать траекторию Мыши вертикально, чтобы Мышь коснулась норы и коснулась краев окна программы.

<u>Дополнительные требования</u>: движение Мыши по траектории должно быть с постоянной скоростью без ускорения и общим направлением вверх направо.


# 2 Задание констант

Вся система включает в себя следующие константные параметры, при которых программа будет запускаться:
- $W, H$ - длина и высота окна соответственно
- $R_M, R_H$ - радиус мыши и радиус норы соответственно. 

По этим данным можно вычислить позиции позиции мыши и норы с учетом, что ось ордината направлена снизу вверх:
- $\mathbf{P_M} = \begin{pmatrix}R_M\\ H-R_M\end{pmatrix}$ - мышь на старте с заданным радиусом $R_M$
- $\mathbf{P_H} = \begin{pmatrix}W-R_H\\ R_H\end{pmatrix}$ - нора с заданным радиусом $R_H$


Также можно высчитать критические позиции Мыши, где она одновременно касается края окна программы и норы. Таких позиции две: одна касается верхнего края окна, другая касается правой стороны окна.

Есть задача найти расстояние по одной из осей позиции, которая позволит удовлетворить условию касания Мыши с Норой. Это рассчитывается через теорему Пифагора:

$$
\begin{array}{l}
(R_M+R_H)^2 = X^2+(R_H-R_M)^2 \\[10pt]
X = 2\sqrt{R_MR_H}
\end{array}
$$

Теперь можно расписать формулы критических позиций:

- $\mathbf{S_T} = \begin{pmatrix}W-R_H-2\sqrt{R_H R_M}\\ R_M\end{pmatrix}$ - верхняя критическая позиция, касается верхнего края окна и левее норы
- $\mathbf{S_B} = \begin{pmatrix}W-R_H\\ R_H+2\sqrt{R_H R_M}\end{pmatrix}$ - верхняя критическая позиция, касается правого края окна и ниже норы

# 3 Разброс траекторий

**Разбросом траекторий** называется вертикальное смещение критических позиций, что задает испытуемому растояние для ручного смещения заданной параболы.

Пусть переменная $q\in[0, 1]$ будет задавать **степень смещения**. Тогда формулы смещенных критической позиции можно расписать как линейные интерполяции от $q$.

**Сложностью траекторий** называется минимальное расстояние, на которое необходимо сместить параболу, чтобы Мышь коснулась Норы. 

Нижнюю критическую позицию возможно смещать вниз до касания нижнего края экрана, расстояние которого можно вычислить:
$$
D = H-(R_H+2\sqrt{R_HR_M}+R_M)
$$

Верхнюю критическую позицию можно смещать наверх на то же расстояние.

> В ранних версиях модели верхняя критическая позиция смещалась вправо от Норы на расстояние $D$. Этого подхода был недостаток: при сильном смещении *вертикальная парабола* направленная к верхнему края экрана имела намного большую **сложность**.  

Ниже представлены формулы смещенных критических позиций:
$$
\begin{array}{l}
    \mathbf{S_T}(q) = \begin{pmatrix}W-R_H-2\sqrt{R_H R_M}\\ R_M\end{pmatrix} - 
    \begin{pmatrix} 0 \\ D\end{pmatrix} \cdot q \\[20pt]
    \mathbf{S_B}(q) = \begin{pmatrix}W-R_H\\ R_H+2\sqrt{R_H R_M}\end{pmatrix} +
    \begin{pmatrix} 0 \\ D\end{pmatrix} \cdot q
\end{array}
$$


# 4 Подбор параболических траекторий

Данная подзадача имеет пространство решений, но для простоты было решено создать ещё одно требование к генерации траекторий: вершина параболы всегда находится в начальной позиции Мыши. Таким образом изгибов во время пути не будут и траектория будет предсказуема.

## 4.1 Элементарные параболы: $x^2$ и $\sqrt{x}$

Для начала зададим формулы траектории к заданным критическим точкам через формулы параболы. Эталонными формулами, задающие *вертикальные и горизонтальные* параболы будут:

$$
y=\dfrac{y_1-y_0}{(x_1-x_0)^2}\cdot(x-x_0)^2+y_0,\\[10pt]
x=\dfrac{(x_1-x_0)}{(y_1-y_0)^2}\cdot(y-y_0)^2+x_0,
$$

где $(x_0, y_0)$ - позиция вершины, $(x_1, y_1)$ - позиция критической позиции, через которую парабола проходит.

Относительно видов парабол и критических позиций в итоге получается четыре возможные параболы:

$$
T_{1T}: y=\dfrac{\mathbf{S_T}_y(q)-\mathbf{P_M}_y}{(\mathbf{S_T}_x(q)-\mathbf{P_M}_x)^2}\cdot(x-\mathbf{P_M}_x)^2+\mathbf{P_M}_y,\\[10pt]
T_{2T}: x=\dfrac{(\mathbf{S_T}_x(q)-\mathbf{P_M}_x)}{(\mathbf{S_T}_y(q)-\mathbf{P_M}_y)^2}\cdot(y-\mathbf{P_M}_y)^2+\mathbf{P_M}_x, \\[10pt]
T_{1B}: y=\dfrac{\mathbf{S_B}_y(q)-\mathbf{P_M}_y}{(\mathbf{S_B}_x(q)-\mathbf{P_M}_x)^2}\cdot(x-\mathbf{P_M}_x)^2+\mathbf{P_M}_y,\\[10pt]
T_{2B}: x=\dfrac{(\mathbf{S_B}_x(q)-\mathbf{P_M}_x)}{(\mathbf{S_B}_y(q)-\mathbf{P_M}_y)^2}\cdot(y-\mathbf{P_M}_y)^2+\mathbf{P_M}_x,
$$

Учитывая формулы смещенных критических парабол можно упростить формулы 

$$
T_{1T}: y=\dfrac{\mathbf{S_T}_y-qD-\mathbf{P_M}_y}{(\mathbf{S_T}_x-\mathbf{P_M}_x)^2}\cdot(x-\mathbf{P_M}_x)^2+\mathbf{P_M}_y,\\[10pt]
T_{2T}: x=\dfrac{(\mathbf{S_T}_x-\mathbf{P_M}_x)}{(\mathbf{S_T}_y-qD-\mathbf{P_M}_y)^2}\cdot(y-\mathbf{P_M}_y)^2+\mathbf{P_M}_x, \\[10pt]
T_{1B}: y=\dfrac{\mathbf{S_B}_y+qD-\mathbf{P_M}_y}{(\mathbf{S_B}_x-\mathbf{P_M}_x)^2}\cdot(x-\mathbf{P_M}_x)^2+\mathbf{P_M}_y,\\[10pt]
T_{2B}: x=\dfrac{(\mathbf{S_B}_x-\mathbf{P_M}_x)}{(\mathbf{S_B}_y+qD-\mathbf{P_M}_y)^2}\cdot(y-\mathbf{P_M}_y)^2+\mathbf{P_M}_x,
$$

## 4.2 Проблемы использования элементарных парабол

Как можно заметить при $q=1$ парабола $T_{2B}$ не существует:
$$
\mathbf{S_B}_y+D-\mathbf{P_M}_y = R_H+2\sqrt{R_MR_H} + (H-(R_H+2\sqrt{R_HR_M}+R_M)) - (H-R_M) = 0 \\
$$

Также при программировании движения Мыши по заданной траектории придется использовать изменение аргументов $x$ или $y$ в зависимости от выбранной параболы. 

## 4.3 Квадратичная кривая Безье

Ещё одним способом задания парабол является задание Квадратичной кривой Безье.

https://en.wikipedia.org/wiki/B%C3%A9zier_curve

$$
\begin{array}{l}
\mathbf{B}(t) = \\
= \mathbf{P_0}\cdot(1-t)^2+\mathbf{P_1}\cdot 2(1-t)t + \mathbf{P_2}\cdot t^2=\\
= (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t^2+2(\mathbf{P_1}-\mathbf{P_0})\cdot t + \mathbf{P_0}
\end{array}
$$

Чтобы задать кривую Безье по заданной формулы параболы, например, $y(x)$ необходимо:
1. Задать точки $\mathbf{P_0}$ и $\mathbf{P_2}$ как начало и конец рисуемой параболы: 
$$\mathbf{P_0}=\begin{pmatrix} x_0 \\ y(x_0) \end{pmatrix}, \mathbf{P_2}=\begin{pmatrix} x_1 \\ y(x_1) \end{pmatrix}$$
2. Точка $\mathbf{P_1}$ задается пересечением касательных параболы в точках при аргументах $x_0$ и $x_1$.


Вычислим значение по ординате точки пересечения касательных

$$
\begin{array}{l}
y_t\left(\dfrac{x_0+x_1}{2}\right) =\\
= y'(x_0)\left(\dfrac{x_0+x_1}{2}-x_0\right)+y(x_0) = \\
= 2a(x_0-x_{v})\left(\dfrac{x_1-x_0}{2}\right)+a(x_0-x_{v})^2+y_{v} = \\
= a(x_0x_1 - x_0^2-x_{v}x_1+x_vx_0)+a(x_0^2-2x_0x_{v}+x_{v}^2)+y_{v} = \\
= a(x_0x_1-x_v(x_0+x_1)+x_{v}^2)+y_{v} \\
\end{array}
$$
---

Так как в нашем случае вершина параболы совпадает с начальной точкой кривой, то $x_v=x_0$
$$
a(x_0x_1-x_0(x_0+x_1)+x_{0}^2)+y_{v} =y_{v}\\
$$

Поэтому можно расписать точки кривых Безье для любой параболы и критических точек:

$$
\begin{array}{l}
\mathbf{P_0}=\mathbf{P_M}=\begin{pmatrix} R_M \\[10pt] H-R_M \end{pmatrix},\\
\mathbf{P_2}=\left[\begin{pmatrix} \dfrac{\mathbf{P_M}_x+\mathbf{S_X}_x}{2} \\[10pt] \mathbf{P_0}_y \end{pmatrix}, \begin{pmatrix}  \mathbf{P_0}_x \\[10pt] \dfrac{\mathbf{P_M}_y+\mathbf{S_X}_y\pm qD}{2} \end{pmatrix}\right], \\
\mathbf{P_1}=\mathbf{S_X}
\end{array}
$$

Использование квадратичной кривой Безье в последствии может решить проблемы из пункта 3.2:
1. Отстутствие формулы для прямой представимая через формулу параболы
2. Управление позиции Мыши через регулировки одного аргумента $t$ для обоих компонент позиции $x$, $y$.
3. Возможность создавать другие виды парабол (не будет имплементировано из-за высокой сложности)


# 5 Движение с постоянной скоростью
При заданном дискретном шаге $S$, должно выполняться уравнение:
$$
    \forall S>0 : \| \mathbf{B}(t_{0}+t_\Delta) - \mathbf{B}(t_{0})\|=S,
$$
где $t_{0}$ - позиция интерполяции, при котором $B(t_0)$ - текущая позиция на кривой Безье, и $t_d$ - шаг позиции интерполяции, который необходимо найти.

## 5.1 Решение с аппроксимацией

Быстрое решение:
$$
    t_d=\dfrac{S}{\|\mathbf{B}(t)'(t_0)\|}=\dfrac{S}{\|2(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t+2(\mathbf{P_1}-\mathbf{P_0})\|}
$$

Это решение выходит из идеи, что скорость на протяжении кривой меняется и поэтому нужно определить, сколько "времени" $t_d$ должно пройти, чтобы пройти шаг $S$ c текущей скоростью $\|B'(t_0)\|$.

После нескольких реализованных модель выяснилось, что данное решение работает с точностью до 4 знака после запятой при малом $S$ и 24 кадров в секунду.

Это решение, как и решение точное, не существует, если кривая представима в виде линии

## 5.2 Точное решение

Учитывая, что $B(t)$ - функция квадратичной кривой Безье, данное уравнение можно расписать следующим образом:

$$

\begin{array}{l}
\| \mathbf{B}(t_{0}+t_\Delta) - \mathbf{B}(t_{0})\|= \\[5pt]
=\| (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot (t_0+t_\Delta)^2+2(\mathbf{P_1}-\mathbf{P_0})\cdot (t_0+t_\Delta) + \mathbf{P_0} - ((\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t_0^2+2(\mathbf{P_1}-\mathbf{P_0})\cdot t_0 + \mathbf{P_0})\|= \\[5pt]
=\| (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot (t_0^2+2t_0t_\Delta+t_\Delta^2)+2(\mathbf{P_1}-\mathbf{P_0})\cdot (t_0+t_\Delta)  - (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t_0^2 - 2(\mathbf{P_1}-\mathbf{P_0})\cdot t_0 \|= \\[5pt]
=\| (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot (2t_0t_\Delta+t_\Delta^2)+2(\mathbf{P_1}-\mathbf{P_0})\cdot t_\Delta\|= \\[5pt]
=\| t_\Delta^2\cdot(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})+t_\Delta\cdot(2t_0(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})+2(\mathbf{P_1}-\mathbf{P_0}))\| 
\end{array}
$$

Выделим константы отдельными символами:

$$
\begin{array}{l}
\mathbf{C} = (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\\
\mathbf{D} = (\mathbf{P_1}-\mathbf{P_0})
\end{array}
$$

Продолжим переписывать уравнение:

$$
\begin{array}{l}
\| t_\Delta^2\cdot(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})+t_\Delta\cdot(2t_0(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})+2(\mathbf{P_1}-\mathbf{P_0}))\| = S \\[5pt]
\| t_\Delta^2\cdot \mathbf{C}+t_\Delta\cdot(2t_0\mathbf{C}+2\mathbf{D})\| = S  \\[5pt]
\sqrt{(t_\Delta^2\cdot \mathbf{C_x}+t_\Delta\cdot(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2))^2 + (t_\Delta^2\cdot \mathbf{C_y}+t_\Delta\cdot(2t_0\mathbf{C_x}^2+2\mathbf{D_y}^2))^2} = S  \\[5pt]
(t_\Delta^2\cdot \mathbf{C_x}+t_\Delta\cdot(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2))^2 + (t_\Delta^2\cdot \mathbf{C_y}+t_\Delta\cdot(2t_0\mathbf{C_x}^2+2\mathbf{D_y}^2))^2 = S^2  \\[5pt]
t_\Delta^2\cdot\left[(t_\Delta\cdot \mathbf{C_x}+(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2))^2 + (t_\Delta\cdot \mathbf{C_y}+(2t_0\mathbf{C_x}^2+2\mathbf{D_y}^2))^2\right] = S^2  \\[5pt]
t_\Delta^2\cdot\left[(t_\Delta^2\cdot \mathbf{C_x}^2+2t_\Delta\cdot \mathbf{C_x}(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2)+(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2)^2) + (t_\Delta^2\cdot \mathbf{C_y}^2+2t_\Delta\cdot \mathbf{C_y}(2t_0\mathbf{C_y}^2+2\mathbf{D_y}^2)+(2t_0\mathbf{C_y}^2+2\mathbf{D_y}^2)^2)\right] = S^2  \\[5pt]
t_\Delta^2\cdot\left[t_\Delta^2\cdot \left(\mathbf{C_x}^2+\mathbf{C_y}^2\right)+2t_\Delta\cdot \left(\mathbf{C_x}\left(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2\right)+\mathbf{C_y}\left(2t_0\mathbf{C_y}^2+2\mathbf{D_y}^2\right)\right)+\left(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2\right)^2+ \left(2t_0\mathbf{C_y}^2+2\mathbf{D_y}^2\right)^2\right] = S^2
\end{array}
$$

Также выделим константы отдельными символами:

$$
\begin{array}{l}
C_1 = (\mathbf{C_x}^2+\mathbf{C_y}^2)\\
C_2 = (\mathbf{C_x}(2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2)+\mathbf{C_y}(2t_0\mathbf{C_y}^2+2\mathbf{D_y}^2))\\
C_3 = (2t_0\mathbf{C_x}^2+2\mathbf{D_x}^2)^2+ (2t_0\mathbf{C_y}^2+2\mathbf{D_y}^2)^2
\end{array}
$$

Продолжим переписывать уравнение:

$$
\begin{array}{l}
t_\Delta^2\cdot\left[(t_\Delta^2\cdot C_1+2t_\Delta\cdot C_2+C_3)\right] = S^2 \\
t_\Delta^4\cdot C_1+2t_\Delta^3\cdot C_2+t_\Delta^2\cdot C_3 - S^2 = 0 \\
\end{array}
$$

В итоге получаем уравнение вида:
$$
ax^4+bx^3+cx^2-d^2=0,
$$
где $a\ge0, c\ge0$. Так как шаг будет затрагивать только двe позиции на кривой, то необходимых решений должно быть тоже два: один положительный, один отрицательный (вперед, назад). 

А не тут то было 🥲. При получении корней, пары из них используются для одного направления, потому что при изменении $t_0$ один из пары корней не может быть определен.

Все решения полинома:

$$
\left[
\begin{array}{l}
+a_{5}+\frac{1}{2}\sqrt{\frac{b^{2}}{2a^{2}}-\frac{4c}{3a}+a_{6}-a_{4}}-\frac{b}{4a}\\[5pt]
+a_{5}-\frac{1}{2}\sqrt{\frac{b^{2}}{2a^{2}}-\frac{4c}{3a}+a_{6}-a_{4}}-\frac{b}{4a}\\[5pt]
-a_{5}+\frac{1}{2}\sqrt{\frac{b^{2}}{2a^{2}}-\frac{4c}{3a}-a_{6}-a_{4}}-\frac{b}{4a}\\[5pt]
-a_{5}-\frac{1}{2}\sqrt{\frac{b^{2}}{2a^{2}}-\frac{4c}{3a}-a_{6}-a_{4}}-\frac{b}{4a}\\[5pt]
\end{array}
\right.
$$

Необходимые для движения вперед:

$$
\left[
\begin{array}{l}
+a_{5}+\frac{1}{2}\sqrt{\frac{b^{2}}{2a^{2}}-\frac{4c}{3a}+a_{6}-a_{4}}-\frac{b}{4a}\\[5pt]
-a_{5}+\frac{1}{2}\sqrt{\frac{b^{2}}{2a^{2}}-\frac{4c}{3a}-a_{6}-a_{4}}-\frac{b}{4a}\\[5pt]
\end{array}
\right. ,\\[5pt]
a_{6}=\frac{\left(\frac{4bc}{a^{2}}-\frac{b^{3}}{a^{3}}\right)}{4\sqrt{\frac{b^{2}}{4a^{2}}+a_{4}-\frac{2c}{3a}}} , 
a_{5}=\frac{1}{2}\sqrt{\frac{b^{2}}{4a^{2}}+a_{4}-\frac{2c}{3a}} ,\\[5pt]

a_{4}=\frac{a_{3}}{3\cdot2^{\frac{1}{3}}a}+\frac{2^{\frac{1}{3}}a_{2}}{3a\cdot a_{3}} ,\\[5pt]
a_{3}=\left(\sqrt{a_{1}^{2}-4a_{2}^{3}}+a_{1}\right)^{\frac{1}{3}} ,\\[5pt]

a_{2}=\left(c^{2}-12ad^{2}\right) , a_{1}=\left(72acd^{2}-27b^{2}d^{2}+2c^{3}\right) ,\\[5pt]

a=\left(A_{1}.x^{2}+A_{1}.y^{2}\right), b=\left(2A_{1}.xA_{2}.x+2A_{1}.yA_{2}.y\right),
c=\left(A_{2}.x^{2}+A_{2}.y^{2}\right), d=S, \\[5pt]

A_{1}=\left(P_{0}-2P_{1}+P_{2}\right), A_{2}=\left(2P_{1}-2P_{0}\right)+2t_{0}A_{1}
$$

Это способ очень емкий относительно вычислительных ресурсов и он лучше аппроксимации только с 5-го значения после запятой при заданном шаге для нормальной скорости и 24 кадров в секунду (42 мс), что относительно программы для экспериментов не так важно.

К тому же этот способ не решает ранее выявленные проблемы - нет решении при кривой, которая представима в виде линии.

Модель в Desmos: https://www.desmos.com/calculator/pae41rjxga?lang=ru

## 5.3 Локальные решения при прямой

В каких случаях нельзя найти решения:

$$
\|2(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t+2(\mathbf{P_1}-\mathbf{P_0})\|=0\\
\begin{cases}
(\mathbf{P_1}-\mathbf{P_0}) = \begin{pmatrix}0\\0\end{pmatrix}\\
\left[
\begin{array}{l}
t=0 \\
(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2}) = \begin{pmatrix}0\\0\end{pmatrix} \\
\end{array} \\
\right.
\end{cases}
$$

$(\mathbf{P_1}-\mathbf{P_0}) = \begin{pmatrix}0\\0\end{pmatrix}$ - когда первая и вторая точка кривой совпадают;  
$(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2}) = \begin{pmatrix}0\\0\end{pmatrix}$ - когда точки лежат на одной прямой и вторая равноудалена от первой и третьей

---

По сути, можно представить позицию точки $\mathbf{P_1}$ через интерполяцию на отрезке $\mathbf{P_0}\mathbf{P_2}$:
$$
\mathbf{P_1}=\mathbf{P_0}+(\mathbf{P_2}-\mathbf{P_0})\cdot q, q\in[0, 1]
$$

Тогда квадратичная кривая Безье представима в виде:
$$
\begin{array}{l}
B(t) =\\
= (\mathbf{P_0}-2(\mathbf{P_0}+(\mathbf{P_2}-\mathbf{P_0})\cdot q)+\mathbf{P_2})\cdot t^2+2(\mathbf{P_0}+(\mathbf{P_2}-\mathbf{P_0})\cdot q-\mathbf{P_0})\cdot t + \mathbf{P_0} =\\
= ((1-2q)\cdot (\mathbf{P_2}-\mathbf{P_0}))\cdot t^2+2q\cdot (\mathbf{P_2}-\mathbf{P_0})\cdot t + \mathbf{P_0}
\end{array}
$$

При $q=\dfrac12$ вторая точка равноудалена от первой и третьей точки - $(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2}) = \begin{pmatrix}0\\0\end{pmatrix}$ и кривая становиться прямой:

$$
\begin{array}{l}
\mathbf{B}(t) = (\mathbf{P_2}-\mathbf{P_0})\cdot t + \mathbf{P_0} \\
\mathbf{B}'(t) = (\mathbf{P_2}-\mathbf{P_0})
\end{array} 
$$

При $q=0$  первая и вторая точка кривой совпадают - $(\mathbf{P_1}-\mathbf{P_0}) = \begin{pmatrix}0\\0\end{pmatrix}$ и кривая становиться прямой:

$$
\begin{array}{l}
\mathbf{B}(t) = (\mathbf{P_2}-\mathbf{P_0})\cdot t^2 + \mathbf{P_0} \\
\mathbf{B}'(t) = 2(\mathbf{P_2}-\mathbf{P_0})\cdot t
\end{array}
$$

Так как позицию точек кривой поменять нельзя во время движения, было принято решение перемещать начальную позицию за счет изменения $t_0$. Но есть проблема.

При $q=0$, $t_d=\dfrac{S}{\|\mathbf{B}'(t_0)\|}=\dfrac{S}{\|2(\mathbf{P_2}-\mathbf{P_0})\cdot t_0\|}$ и при $t_0\to0, t_d\to\infty$, поэтому необходимо задавать такой $t_0$, при котором будет баланс: недалеко от начала и небольшой начальный шаг. Это вычисляется из уравнения:
$$
\begin{array}{l}
\dfrac{S}{\|2(\mathbf{P_2}-\mathbf{P_0})\cdot t_0\|} = t_0 \\[10pt]
t_0 = \dfrac{S}{2t_0\cdot\|(\mathbf{P_2}-\mathbf{P_0})\|} \\[10pt]
t_0^2 = \dfrac{S}{2\cdot\|(\mathbf{P_2}-\mathbf{P_0})\|} \\[10pt]
t_0 = \sqrt{\dfrac{S}{2\cdot\|(\mathbf{P_2}-\mathbf{P_0})\|}}
\end{array}
$$

Теперь в коде будет срабатывать условие:
$$
\begin{cases}
\|\mathbf{P_1}-\mathbf{P_0}\| = 0\\
t_0 = 0
\end{cases} \Longrightarrow t_0 = \sqrt{\dfrac{S}{2\cdot\|(\mathbf{P_2}-\mathbf{P_0})\|}}
$$


```python
class MousesMechanics():
    def step(self):
        if np.all((self.P1 - self.P0) == 0) and self.t == 0:
            self.t = np.sqrt(self.STEP/(2*np.linalg.norm(self.P2 - self.P0)))

        self.t += self.STEP / np.linalg.norm(
            2 * (self.P0 - 2 * self.P1 + self.P2) * self.t +
            2 * (self.P1 - self.P0)
        )
```

# 6 Нахождение решений

Данная математическая предполагает предсказуемые решения для любых парабол.

Каждая парабола всегда имеет по два решения: ближайшая и дальняя критические точки.

Решением для ближайшей точки каждой параболы является расчитанное смещение $D=H-(R_H+2\sqrt{R_HR_M}+R_M)$.

Для дальних точек решения расписаны через составлении формул парабол, проходящие через смещенные точки $\mathbf{S_B}(q)$ и $\mathbf{S_T}(q)$, имеющие вертикальное смещение $Y$, при котором парабола в последствии будет проходить в другие критические точки. 

Формулы расписаны:
$$
\begin{array}{l}
\dfrac{\mathbf{S_{T_y}}(q)-\mathbf{P_{M_y}}}{(\mathbf{S_{T_x}}(q)-\mathbf{P_{M_x}})^2}(\mathbf{S_{B_x}}-\mathbf{P_{M_x}})^2+\mathbf{P_{M_y}} + Y_1=\mathbf{S_{B_y}}\\[20pt]
\dfrac{\mathbf{S_{B_y}}(q)-\mathbf{P_{M_y}}}{(\mathbf{S_{B_x}}(q)-\mathbf{P_{M_x}})^2}(\mathbf{S_{T_x}}-\mathbf{P_{M_x}})^2+\mathbf{P_{M_y}} + Y_2=\mathbf{S_{T_y}}\\[20pt]

\dfrac{\mathbf{S_{T_x}}(q)-\mathbf{P_{M_x}}}{(\mathbf{S_{T_y}}(q)-\mathbf{P_{M_y}})^2}(\mathbf{S_{B_y}}-\mathbf{P_{M_y}} - Y_3)^2+\mathbf{P_{M_x}} =\mathbf{S_{B_x}}\\[20pt]

\dfrac{\mathbf{S_{B_x}}(q)-\mathbf{P_{M_x}}}{(\mathbf{S_{B_y}}(q)-\mathbf{P_{M_y}})^2}(\mathbf{S_{T_y}}-\mathbf{P_{M_y}} - Y_4)^2+\mathbf{P_{M_x}} =\mathbf{S_{T_x}}\\[20pt]

\end{array}
$$

Распишем с упрощениями:

$$

\begin{array}{l}
\dfrac{\mathbf{S_{T_y}}+qD-\mathbf{P_{M_y}}}{(\mathbf{S_{T_x}}-\mathbf{P_{M_x}})^2}(\mathbf{S_{B_x}}-\mathbf{P_{M_x}})^2+\mathbf{P_{M_y}} + Y_1=\mathbf{S_{B_y}}\\[20pt]
\dfrac{\mathbf{S_{B_y}}-qD-\mathbf{P_{M_y}}}{(\mathbf{S_{B_x}}-\mathbf{P_{M_x}})^2}(\mathbf{S_{T_x}}-\mathbf{P_{M_x}})^2+\mathbf{P_{M_y}} + Y_2=\mathbf{S_{T_y}}\\[20pt]

\dfrac{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}{(\mathbf{S_{T_y}}+qD-\mathbf{P_{M_y}})^2}(\mathbf{S_{B_y}}-\mathbf{P_{M_y}} - Y_3)^2+\mathbf{P_{M_x}} =\mathbf{S_{B_x}}\\[20pt]

\dfrac{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}{(\mathbf{S_{B_y}}-qD-\mathbf{P_{M_y}})^2}(\mathbf{S_{T_y}}-\mathbf{P_{M_y}} - Y_4)^2+\mathbf{P_{M_x}} =\mathbf{S_{T_x}}\\[20pt]

\end{array}
$$

При упрощении получаем:

$$

\begin{array}{l}
Y_1=(\mathbf{S_{B_y}} - \mathbf{P_{M_y}}) - (\mathbf{S_{T_y}}-\mathbf{P_{M_y}}) \left(\dfrac{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}\right)^2 -  qD\cdot \left(\dfrac{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}\right)^2 \\[20pt]

Y_2=(\mathbf{S_{T_y}} - \mathbf{P_{M_y}}) - (\mathbf{S_{B_y}}-\mathbf{P_{M_y}}) \left(\dfrac{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}\right)^2 +  qD\cdot \left(\dfrac{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}\right)^2 \\[20pt]

Y_3=(\mathbf{S_{B_y}} - \mathbf{P_{M_y}}) - (\mathbf{S_{T_y}}-\mathbf{P_{M_y}}) \left(\dfrac{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}\right)^{\frac12} -  qD\cdot \left(\dfrac{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}\right)^{\frac12} \\[20pt]

Y_4=(\mathbf{S_{T_y}} - \mathbf{P_{M_y}}) - (\mathbf{S_{B_y}}-\mathbf{P_{M_y}}) \left(\dfrac{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}\right)^{\frac12} +  qD\cdot \left(\dfrac{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}\right)^{\frac12} \\[20pt]

\end{array}
$$

Заменим константы отдельными символов

$$

\begin{array}{l}
A = (\mathbf{S_{B_y}} - \mathbf{P_{M_y}}) = (H-(R_H+2\sqrt{R_HR_M}+R_M))\\[5pt]
B = (\mathbf{S_{T_y}}-\mathbf{P_{M_y}}) = (H-2R_M) \\[5pt]
C = \left(\dfrac{\mathbf{S_{B_x}}-\mathbf{P_{M_x}}}{\mathbf{S_{T_x}}-\mathbf{P_{M_x}}}\right) = \left(\dfrac{W-(R_H+2\sqrt{R_HR_M}+R_M)}{W-2R_M}\right) \\[10pt]
D = H-(R_H+2\sqrt{R_HR_M}+R_M) = A \\[20pt]

\begin{array}{ll}
Y_1= A - B\cdot C^2 -  qA\cdot C^2 & = A -(B+qA)\cdot C^2 \\[5pt]
Y_2= B - A\cdot C^{-2} +  qA\cdot C^{-2} &= B+(q-1)\cdot A\cdot C^{-2}  \\[5pt]
Y_3= A - B\cdot C^{\frac12} -  qA\cdot C^{\frac12} &= A -(B+qA)\cdot C^{\frac12}\\[5pt]
Y_4= B - A \cdot C^{-\frac12} +  qA\cdot C^{-\frac12} &= B+(q-1)\cdot A\cdot C^{-\frac12}\\[5pt]
\end{array}

\end{array}
$$


В итоге данные решения представимы формулами с константами и переменной $q\in[0,1]$:

$$
\begin{array}{l}

A=(H-(R_H+2\sqrt{R_HR_M}+R_M)) \\
B=(H-2R_M) \\
C=\left(\dfrac{W-(R_H+2\sqrt{R_HR_M}+R_M)}{W-2R_M}\right) \\

Y_1\in\left[q\cdot A, B+(q-1)\cdot A\cdot C^2\right] \\
Y_2\in\left[q\cdot A, -A+(B+q\cdot A)\cdot C^{-2} \right] \\
Y_3\in\left[q\cdot A, B+(q-1)\cdot A\cdot C^{\frac12} \right] \\
Y_4\in\left[q\cdot A, -A+(B+q\cdot A)\cdot C^{-\frac12} \right] \\
\end{array}
$$

Эти формулы прописаны в коде:
```python
class MouseMechanics()
    def startTrail(self):
        self.t = 0
        self.yOffset = 0
        self.lastT = 0
        self.disp = rd(0, self.MAX_DISPERSION)
        self.choice = ch([0, 1, 2, 3])
        self.BallPos = self.START_POS

        ic("==============================")
        ic(self.choice, self.disp)

        self.P2 = [
            self.BOTTOM_POS(self.disp),
            self.TOP_POS(self.disp)
        ][self.choice // 2]

        self.P1 = [
            np.array([(self.P2[0] + self.P0[0])/2, self.P0[1]]),
            np.array([self.P0[0], (self.P2[1] + self.P0[1])/2]),
        ][self.choice % 2]

        q = self.disp
        A = self.INTERVAL
        B = self.WIN_SIZE[1] - 2*self.RADIUS_MOUSE
        C = (self.WIN_SIZE[0] - (self.RADIUS_MOUSE + self.RADIUS_HOLE + 2 * np.sqrt(self.RADIUS_HOLE * self.RADIUS_MOUSE)))/(self.WIN_SIZE[0] - 2*self.RADIUS_MOUSE)
        self.answer = np.array([
            [- B - (q - 1) * A * C**(2)  , - q * A                      ],
            [- B - (q - 1) * A * C**(1/2), - q * A                      ],
            [  q * A                     , - A + (B + q * A) * C**(-2)  ],
            [  q * A                     , - A + (B + q * A) * C**(-1/2)],
        ])[self.choice]

```

# 7 Отрисовка части кривой Безье

Программы "Мыши" подразумевает экспорт данных экспериментов с рисунками траекторий. Для сокращения размера файла и поддержания идеального качества картинки был выбрана векторная графика, которая позволяет оперировать координатами фигур.

Отрисовать круги для Норы, последней позиции Мыши и зоны бездействия легко. Также легко отрисовать сгенерированную траекторию мыши, так как изначально известны координаты кривой Безье и их можно просто использовать. 

А отрисовать траекторию испытуемого сложнее из-за того, что она состоит из частей изначальной кривой Безье смещенной вверх или вниз и вертикальных отрезков. Поэтому необходимо понять как выбирать часть кривой Безье.

Для этого введем две переменные:
- $t_L$ - значение $t$ при последнем смещении испытуемого.
- $t_C$ - значение $t$ при текущем смещении.

На самом деле, логика задание кривой от части исходной кривой Безье абсолютно такая же, как и задание кривой для параболы.

В итоге получаем такие точки части кривой Безье:

$$
\mathbf{P_0} = \mathbf{B}(t_L), \\ 
\mathbf{P_1}= \mathbf{B}'(t_L)\left(\dfrac{t_L+t_D}{2}-t_L\right)+\mathbf{B}(t_L)\\
\mathbf{P_2}=\mathbf{B}(t_D),
$$

Эти формулы есть в функции `getPartial()`

```python
class MouseMechanics():
    def bezier(self, t:float, P0, P1, P2):
        return (
            P0 * (1 - t) * (1 - t)
          + P1 * 2 * (1 - t) * t
          + P2 * t * t 
        )
    def function(self, t: float):
        return self.bezier(t, self.P0, self.P1, self.P2)
    def derivative(self, t):
        return (
          - self.P0 * 2 * (1 - t)
          + self.P1 * 2 * (1 - 2 * t)
          + self.P2 * 2 * t 
        )
    def getPartial(self):
        return (np.array([
            self.function(self.lastT), # last Pos
            (self.t - self.lastT) / 2 * self.derivative(self.lastT) + self.function(self.lastT),
            self.function(self.t) # current Pos
        ]) + np.array([0, self.yOffset])).astype(np.int16)
```


# Приложение

Здесь собраны общие теоремы, которые были использованы в математической модели, и их доказательства

## 1 Теорема о позиции точки пересечения касательных на параболе

**Теорема**: значение абсциссы точки пересечения двух касательных параболы является суммой половины значений абсциссы точек этих касательных.

$$
x_I=\dfrac{x_0+x_1}{2}
$$

**Доказательство**.

Зададим аргументы точек касательных и распишем общую формулу значения абсциссы точки пересечения:

$$
y'(x_0)(x_I-x_0)+y(x_0) = y'(x_1)(x_I-x_1)+y(x_1)\\[10pt]
x_I=\dfrac{(y'(x_0)x_0-y'(x_1)x_1)-(y(x_0)-y(x_1))}{y'(x_0)-y'(x_1)}\\
$$

Далее зададим формулу исходной параболы и вычислим её производную. 

$$
y(x) = a(x-x_{v})^2+y_{v} = a\cdot x^2+(2ax_{v})\cdot x+(ax_{v}^2 + y_{v})\\
y'(x) = 2a(x-x_{v}) = 2a\cdot x-2ax_{v}\\
$$

Вычислим значение аргумента точки пересечения касательных относительно заданной параболы 

$$
\begin{array}{l}
x_I=\dfrac{(y'(x_0)x_0-y'(x_1)x_1)-(y(x_0)-y(x_1))}{y'(x_0)-y'(x_1)} = \\[10pt] 
=\dfrac{
    2a(x_0-x_{v})x_0-2a(x_1-x_{v})x_1
    -((a(x_0-x_{v})^2+y_{v})-(a(x_1-x_{v})^2+y_{v}))
    }{2a(x_0-x_{v})-2a(x_1-x_{v})} = \\[20pt]
=\dfrac{
    2a(x_0^2-x_{v}x_0-x_1^2+x_{v}x_1)
    -a(x_0^2-2x_0x_{v}-x_1^2+2x_1x_{v})
    }{2a(x_0-x_1)} = \\[20pt]
=\dfrac{
    (2x_0^2-2x_{v}x_0-2x_1^2+2x_{v}x_1)-(x_0^2-2x_{v}x_0-x_1^2+2x_{v}x_1)
    }{2(x_0-x_1)} = \\[20pt]
=\dfrac{x_0^2-x_1^2}{2(x_0-x_1)} =\boxed{\dfrac{x_0+x_1}{2}}
\end{array}
$$

## 2 Теорема о позиции точки пересечения касательных на кривой Безье

**Теорема**: значение абсциссы точки пересечения двух касательных параболы является суммой половины значений абсциссы точек этих касательных.

$$
t_I=\dfrac{t_0+t_1}{2}
$$

**Доказательство**.

Зададим аргументы точек касательных и распишем общую формулу значения абсциссы точки пересечения:

$$
\mathbf{B}'(t_0)(t_I-t_0)+\mathbf{B}(t_0) = \mathbf{B}'(t_1)(t_I-t_1)+\mathbf{B}(t_1) \\[10pt]
t_I=\dfrac{(\mathbf{B}'(t_0)t_0-\mathbf{B}'(t_1)t_1)-(\mathbf{B}(t_0)-\mathbf{B}(t_1))}{\mathbf{B}'(t_0)-\mathbf{B}'(t_1)}\\
$$

Далее зададим формулу исходной параболы и вычислим её производную. 

$$
\begin{array}{l}
\mathbf{B}(x) = (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t^2+2(\mathbf{P_1}-\mathbf{P_0})\cdot t + \mathbf{P_0}\\[10pt]

\mathbf{B}'(x) = 2(\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2})\cdot t+2(\mathbf{P_1}-\mathbf{P_0})\\

\end{array}
$$

Для упрощения вычисления введем отдельные символы для констант:
$$
\begin{array}{l}
\mathbf{K} = (\mathbf{P_0}-2\mathbf{P_1}+\mathbf{P_2}), 
\mathbf{N} = (\mathbf{P_1}-\mathbf{P_0}), \\[10pt]

\mathbf{B}(x) = \mathbf{K}\cdot t^2+2\mathbf{N}\cdot t + \mathbf{P_0}\\[10pt]
\mathbf{B}'(x) = 2\mathbf{K}\cdot t+2\mathbf{N}\\
\end{array}
$$

Вычислим значение аргумента точки пересечения касательных относительно заданной кривой

$$
\begin{array}{l}
t_I=\dfrac{(\mathbf{B}'(t_0)t_0-\mathbf{B}'(t_1)t_1)-(\mathbf{B}(t_0)-\mathbf{B}(t_1))}{\mathbf{B}'(t_0)-\mathbf{B}'(t_1)} \\[10pt]
=\dfrac{
    ((2\mathbf{K}\cdot t_0+2\mathbf{N})t_0-(2\mathbf{K}\cdot t_1+2\mathbf{N})t_1)-(\mathbf{K}\cdot t_0^2+2\mathbf{N}\cdot t_0 + \mathbf{P_0}-(\mathbf{K}\cdot t_1^2+2\mathbf{N}\cdot t_1 + \mathbf{P_0}))}{(2\mathbf{K}\cdot t_0+2\mathbf{N})-(2\mathbf{K}\cdot t_1+2\mathbf{N})} \\[10pt]
=\dfrac{
    (2\mathbf{K}\cdot (t_0^2-t_1^2)+2\mathbf{N}(t_0-t_1))-(\mathbf{K}\cdot (t_0^2-t_1^2)+2\mathbf{N}\cdot (t_0 - t_1))}{2\mathbf{K}\cdot (t_0-t_1)} \\[10pt]
=\dfrac{
    \mathbf{K}\cdot (t_0^2-t_1^2)}{2\mathbf{K}\cdot (t_0-t_1)} =\boxed{\dfrac{t_0+t_1}{2}}
\end{array}
$$

# Метод задании кривой Безье по существующей формулы параболы

Для задания квадратичной кривой Безье от части исходной параболы $y(x)=ax^2+bx+c$ необходимо:
1. Определить начальные и конечные точки отрисовки:
$$\mathbf{P_0} = \begin{pmatrix} x_0 \\ y(x_0) \end{pmatrix}, \mathbf{P_2}=\begin{pmatrix} x_1 \\ y(x_1) \end{pmatrix}$$ 
1. Средняя точка Безье определяется как пересечение касательных в точках аргумента $x_0$ и $x_1$: 
$$\mathbf{P_1}=\begin{pmatrix} \frac{x_1+x_2}{2} \\ y'(x_0)(\frac{x_1+x_2}{2}-x_0)+y(x_0)\end{pmatrix}$$ 

# Метод задании кривой Безье по существующей формулы кривой Безье

Для задания квадратичной кривой Безье от части исходной кривой Безье $\mathbf{B}(t) = \mathbf{P_0}(1-t)^2 + \mathbf{P_1}(2t-2t^2) + \mathbf{P_2}t^2$ необходимо:
1. Определить начальные и конечные точки отрисовки:
$$\mathbf{P_0} = \mathbf{B}(t_0), \mathbf{P_2}=\mathbf{B}(t_1)$$ 
2. Средняя точка Безье определяется как пересечение касательных в точках аргумента $t_0$ и $t_1$: 
$$\mathbf{P_1}= \mathbf{B}'(t_0)\left(\dfrac{t_0+t_1}{2}-t_0\right)+\mathbf{B}(t_0)$$