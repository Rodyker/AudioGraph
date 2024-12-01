import math
import turtle
import array
from output import Output

flip_x = False
flip_y = True

screen = turtle.Screen()
screen.setup(width=2000, height=2000)
canvas = screen.getcanvas()
t = turtle.Turtle("turtle")
t.speed(-1)
t.width(5)
t.hideturtle()
t.up()

output = Output(1, flip_x= flip_x, flip_y= flip_y)

is_left_clicked = False
def left_clicked(x, y):
    global is_left_clicked
    is_left_clicked = True
    t.setpos(x, y)
    t.color("black")
    t.width(5)
    t.down()

is_right_clicked = False
def right_clicked(x, y):
    global is_right_clicked
    is_right_clicked = True
    t.setpos(x, y)
    t.color("white")
    t.width(30)
    t.down()    

all_points = []
def released(e):
    global is_left_clicked
    global is_right_clicked

    is_left_clicked = False
    is_right_clicked = False
    t.up()
    t.color("black")
    
def mouse_position(e):
    global is_left_clicked
    global is_right_clicked
    global all_points
    
    x = e.x - screen.window_width() / 2.0
    y = screen.window_height() / 2.0 - e.y

    if is_left_clicked:
        for _ in range(5):
            all_points.append((-1 if flip_x else 1) * x/1000)
            all_points.append(-1 * (-1 if flip_y else 1) * y/1000)
        if len(all_points) > 0:
            output.sound_set(all_points)
            output.update_wave()

        t.setpos(x, y)

    if is_right_clicked:
        t.setpos(x, y)

        for i in range(0, len(all_points), 2):
            if abs(math.sqrt((all_points[i] - x/1000)**2 + (all_points[i + 1] - y/1000)**2)) < 15/1000:
                all_points[i] = ""
                all_points[i + 1] = ""
        all_points = [x for x in all_points if x != ""]

        output.sound_set(all_points)
        output.update_wave()
                

turtle.onscreenclick(fun = left_clicked)
turtle.onscreenclick(fun = right_clicked, btn = 3)
canvas.bind("<ButtonRelease>", released)
canvas.bind('<Motion>', mouse_position)

try:
    screen.mainloop()

finally:
    output.close()