# template for "Stopwatch: The Game"
import simplegui

# define global variables
tenths = success = total = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    mins = secs = tens = ""
    
    seconds = (t / 10) if (t / 10) < 60 else (t / 10) % 60
    minutes = t / 600
    
    mins = str(minutes) if minutes else "0"
        
    if (seconds):
        if (seconds > 9):
            secs = str(seconds)
        else:
            secs = "0" + str(seconds)
    else:
        secs = "00"
        
    tens = t % 10
        
    return "%s:%s.%s" % (mins, secs, tens)
        
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global success, total
    if (timer.is_running()):
        timer.stop()
        if ((tenths % 10) == 0):
            success += 1
        total += 1

def reset():
    global tenths, success, total
    timer.stop()
    tenths = success = total = 0

def reflexes():
    reflex = "%s/%s" % (success, total)
    return reflex
    
# define event handler for timer with 0.1 sec interval
def tick():
    global tenths
    tenths += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(tenths), [85,115], 50, "White")
    canvas.draw_text(reflexes(), [250, 30], 30, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)


# register event handlers
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)

# start frame
frame.start()


# Please remember to review the grading rubric
