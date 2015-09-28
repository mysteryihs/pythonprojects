# template for "Stopwatch: The Game"
import simplegui
import random
# define global variables
interval = 0
x = 0
y = 0
D = 0
timertest = False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global D
    A = t // 600
    B = ((t // 10) % 60) // 10
    C = ((t // 10) % 60) % 10
    D = ((t % 60) % 10)
    return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def button_start():
    global timertest
    timertest = True
    timer.start()
def button_stop():
    global timertest, x, y
    timer.stop()
    if D == 0 and timertest == True:
        x = x + 1
    if timertest == True:
        y = y + 1
    timertest = False
def button_restart():
    global interval, x, y
    interval = 0
    x = 0
    y = 0

# define event handler for timer with 0.1 sec interval
def timer():
    global interval
    interval = interval + 1

# define draw handler
def draw(canvas):
    canvas.draw_text(str(format(interval)), (110, 110), 30, "White")
    canvas.draw_text(str(str(x) + "/" + str(y)), (250, 50), 30, "Green")
    
# create frame
frame = simplegui.create_frame("Timer", 300, 200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer)
button1 = frame.add_button("Start", button_start, 100)
button2 = frame.add_button("Stop", button_stop, 100)
button3 = frame.add_button("Restart", button_restart, 100)
# start frame
frame.start()
# Please remember to review the grading rubric
