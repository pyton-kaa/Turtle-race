import random
from turtle import Turtle, Screen
from math import pi
from time import sleep

def step_straight(turtle_list, turtle_number, stadium, turtle_positions):
    v = random.randint(1,5)
    x = turtle_list[turtle_number].xcor()
    if int(x) in range(int(stadium.straight/2 - v), int(stadium.straight/2)) and turtle_list[turtle_number].heading() == 0:
        turtle_list[turtle_number].setx(stadium.straight/2)
        turtle_positions[turtle_number] += turtle_list[turtle_number].xcor() - x
    elif int(x) in range(int(-stadium.straight/2 + 1), int(-stadium.straight/2 + v + 1)) and turtle_list[turtle_number].heading() == 180:
        turtle_list[turtle_number].setx(-stadium.straight/2)
        turtle_positions[turtle_number] += x - turtle_list[turtle_number].xcor()
    elif int(x) in range(int(stadium.straight/2 - 16 - v), int(stadium.straight/2 - 16)) and turtle_list[turtle_number].heading() == 0:
        turtle_list[turtle_number].setx(stadium.straight/2 - 16)
        turtle_positions[turtle_number] += turtle_list[turtle_number].xcor() - x
    else:
        turtle_list[turtle_number].fd(v)
        turtle_positions[turtle_number] += v

def radii(stadium):
    list = []
    for n in range(int(stadium.radius / stadium.lane_width)):
        list.append(stadium.radius - (n + 0.5) * stadium.lane_width)
    return(list)

def angle(turtle_number, stadium):
    r = radii(stadium)[turtle_number]
    return(180 / (pi * r))

def step_arc(turtle_list, turtle_number, stadium, turtle_positions):
    v = random.randint(1,5)
    r = radii(stadium)[turtle_number]
    angle = 180 * v / (pi * r)
    head = turtle_list[turtle_number].heading()
    if head >= 180 - angle and head < 180:
        turtle_list[turtle_number].setpos(stadium.straight/2, stadium.radius - (turtle_number + 0.5) * stadium.lane_width)
        turtle_list[turtle_number].seth(180)
        turtle_positions[turtle_number] += (180 - head) * r * pi / 180
    elif head >= 360 - angle:
        turtle_list[turtle_number].setpos(-stadium.straight/2, -stadium.radius + (turtle_number + 0.5) * stadium.lane_width)
        turtle_list[turtle_number].seth(0)
        turtle_positions[turtle_number] += (360 - head) * r * pi /180
    else:
        turtle_list[turtle_number].circle(r, angle)
        turtle_positions[turtle_number] += v
    

def race(turtle_list, stadium, screen, bet):
    turtle_positions = [0] * len(turtle_list)
    screen.tracer(0)
    bookmaker = Turtle()
    bookmaker.ht()
    bookmaker.penup()
    bookmaker.pencolor(turtle_list[bet-1].pencolor())
    bookmaker.sety(25)
    bookmaker.write(f"You bet on the {turtle_list[bet-1].pencolor()} turtle.", font=("Arial", 14, "bold"), align="center")
    counter = Turtle()
    counter.ht()
    counter.penup()
    counter.pencolor("beige")
    counter.sety(-50)
    referee = Turtle()
    referee.penup()
    referee.ht()
    meter = Turtle()
    meter.ht()
    meter.penup()
    meter.pencolor("beige")
    meter.goto(-80, -15)
    for n in range(3):
        counter.write(f"The race starts in {3-n} seconds!", font=("Arial", 20, "bold"), align="center")
        screen.update()
        sleep(1)
        counter.clear()
    counter.write("Run, turtles, run!", font=("Arial", 20, "bold"), align="center")
    counter.goto(37, 5)
    counter.write("Current leader:", font=("Arial", 14, "bold"), align="right")
    counter.goto(-80, -15)
    counter.write(" px ahead of ", font=("Arial", 14, "bold"), align="left", move=True)
    referee_pos = counter.pos()
    laps = [0] * len(turtle_list)
    leader = bet
    second = bet
    while max(laps) < 2:
        for n in range(len(turtle_list)):
            lower_straight = turtle_list[n].heading() == 0 and turtle_list[n].xcor() < stadium.straight/2
            upper_straight = turtle_list[n].heading() == 180 and turtle_list[n].xcor() > -stadium.straight/2
            if  lower_straight or upper_straight:
                step_straight(turtle_list, n, stadium, turtle_positions)
            else:
                step_arc(turtle_list, n, stadium, turtle_positions)
            if turtle_list[n].heading() == 0 and turtle_list[n].xcor() == stadium.straight/2 - 16:
                laps[n] += 1
        max_pos = max(turtle_positions)
        former_leader = leader
        leader = turtle_positions.index(max_pos)
        turtle_positions[leader] = 0
        second_pos = max(turtle_positions)
        turtle_positions[leader] = max_pos
        former_second = second
        second = turtle_positions.index(second_pos)
        meter.clear()
        meter.write(int(turtle_positions[leader] - turtle_positions[second]), font=("Arial", 14, "bold"), align="right")
        if former_leader != leader or former_second != second:
            referee.clear()
            referee.goto(37, 5)
            referee.pencolor(turtle_list[leader].pencolor())
            referee.write(f" {turtle_list[leader].pencolor()}", font=("Arial", 14, "bold"), align="left")
            referee.goto(referee_pos)
            referee.pencolor(turtle_list[second].pencolor())
            referee.write(f" {turtle_list[second].pencolor()}", font=("Arial", 14, "bold"), align="left")
        screen.update()
        sleep(0.03)
    winner = laps.index(2)
    turtle_list[winner].write("Winner", font=("Arial", 20, "bold"), align="left")
    counter.clear()
    counter.goto(0, -50)
    counter.write("Finish!", font=("Arial", 20, "bold"), align="center")
    referee.clear()
    meter.clear()
    bookmaker.sety(-5)
    bookmaker.pencolor(turtle_list[winner].pencolor())
    bookmaker.write(f"The {turtle_list[winner].pencolor()} turtle won the race.", font=("Arial", 16, "bold"), align="center")
    screen.update()
    return(winner)

