import random
from turtle import *
from cmath import pi
from stadium import Stadium
from runner import race

stadium = Stadium()
painter = stadium.painter()
win = stadium.screen()
stadium.paint_stadium(painter, win)

radius = 250
straight = 200
lanes = 6
lane_width = 20

changed = False
change_lanes = "n"
change_size = "n"

def lanes_prompt():
    answer = win.textinput(
        title = "Number of lanes",
        prompt = "Do you wish to change the number of lanes on the stadium? (y / n)"
    ).lower()
    return(answer)
def size_prompt():
    answer = win.textinput(
        title = "Change size of stadium",
        prompt = "Do you wish to change the size of the stadium? (y / n)"
    ).lower()
    return(answer)

change_lanes = lanes_prompt()
if change_lanes != "y":
    change_size = size_prompt()

while change_lanes == "y" or change_size == "y":
    if change_lanes == "y":
        lanes = int(win.numinput(
            title = "New number of lanes",
            prompt = f"""Please choose the number of lanes (between 2 and 10):
            default = 6, current value = {lanes}.""",
            minval = 2,
            maxval = 10
        ))
        changed = True
        change_lanes = "n"
    if change_size != "y":
        change_size = size_prompt()
    if change_size == "y":
        radius = win.numinput(
            title = "Radius of the arc",
            prompt = f"""Please choose the radius of the arc of the stadium:
            default = 250, current value = {radius}.
            Should be less than a half of your screen Y-resolution):""",
            minval = 100,
            maxval = 400
        )
        straight = win.numinput(
            title = "Straight length",
            prompt = f"""Please choose the length of the straight:
            default = 200, current value = {straight}
            Should be less than your screen width minus double radius.""",
            minval = 0,
            maxval = 1200 - 2 * radius
        )
        lane_width = win.numinput(
            title = "Lane width",
            prompt = f"""Please choose the width of a single lane:
            default = 20, current value = {lane_width}.
            Should be between 10 and 40.""",
            minval = 10,
            maxval = 40
        )
        changed = True
        change_size = "n"
    inner_radius = radius - lanes * lane_width
    max_lanes = int(straight / (2 * pi * lane_width)) + int((pi * inner_radius + straight) / (2 * pi * lane_width)) + 1
    if inner_radius < 50:
        change_lanes = win.textinput(
            title = "Error!",
            prompt = f"""Sorry, your stadium is too narrow to fit all the lanes!
            The arc radius of the inner-most lane should be at least 50.
            Current value: {inner_radius}
            Do you wish to change the number of lanes? (y / n):"""
        ).lower()
        change_size = "y"
    elif max_lanes < lanes:
        change_lanes = win.textinput(
            title = "Error!",
            prompt = f"""Sorry, your stadium is too small to fit all starting positions before the second arc.
            With its current size, it could fit at most {max_lanes} lanes.
            Current value: {lanes}
            Do you wish to change the number of lanes? (y / n):"""
        ).lower()
        change_size = "y"
    elif changed:
        stadium.radius = radius
        stadium.straight = straight
        stadium.lanes = lanes
        stadium.lane_width = lane_width
        stadium.paint_stadium(painter, win)
        change_lanes = lanes_prompt()
        change_size = size_prompt()

stadium.start_lines(painter)


colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'black', 'brown', 'pink', 'grey']

runners_number = int(win.numinput(
    title = 'Number of turtles',
    prompt = f'Choose the number of turtles taking part in the race (between 2 and {stadium.lanes}):',
    minval = 2,
    maxval = stadium.lanes
))

turtle_list = []
for n in range(runners_number):
    turtle_list.append(Turtle(shape = 'turtle'))
    turtle_list[n].color(colors[n])
    turtle_list[n].penup()
    turtle_list[n].goto(stadium.start_positions[n])
    turtle_list[n].seth(stadium.start_angles[n])
    turtle_list[n].speed(0)

turtle_colors = "1. " + turtle_list[0].pencolor()
if runners_number == 2:
    turtle_colors += " and 2. " + turtle_list[1].pencolor()
else:
    for n in range(1,runners_number - 1):
        turtle_colors += f", {n+1}. " + turtle_list[n].pencolor()
    turtle_colors += f" and {runners_number}. " + turtle_list[-1].pencolor()

bet = int(win.numinput(
    title = "Bet the winner",
    prompt = f"Choose the number of the turtle you bet on.\nTurtles running: {turtle_colors}.",
    minval = 1,
    maxval = runners_number
))

winner = race(turtle_list, stadium, win, bet)
print(f"The {turtle_list[winner].pencolor()} turtle wins!")
if winner == bet - 1:
    print("Your bet was correct. You win.")
else:
    print("Your bet was wrong. You lose.")


win.exitonclick()