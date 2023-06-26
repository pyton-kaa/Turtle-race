from turtle import Turtle, Screen, colormode
from math import pi



class Stadium:
    def __init__(self, radius = 250, straight = 200, lanes = 6, lane_width = 20):
        self.radius = radius
        self.straight = straight
        self.lanes = lanes
        self.lane_width = lane_width
        self.start_positions = []
        self.start_angles = []

    def painter(self):
        """Create a turtle that will paint the stadium."""
        painter = Turtle()
        painter.ht()
        painter.penup()
        painter.speed(0)
        painter.pensize(3)
        return(painter)

    def screen(self):
        """Create a screen on which the run will take place."""
        win = Screen()
        win.title("The Turtle Run")
        win.bgcolor("darkolivegreen2")
        return(win)

    def paint_stadium(self, painter, win):
        """Paint the stadium.
        The painter argument should be a Turtle object.
        The win argument should be a TurtlScreen object.
        Recommended to use with results of painter() and screen() methods as arguments."""
        if self.lanes * self.lane_width > self.radius or (2 * self.straight + pi * self.radius) / (2 * pi * self.lane_width) < self.lanes:
            print("Sorry, your stadium is too small to fit this number of lanes")
        else:
            # Change the size of the screen so that the stadium fits best:
            win.setup(width = 2 * self.radius + self.straight + 40, height = 2 * self.radius + 40)
            # Paint the stadium outline and fill it with color:
            painter.color("beige", "coral")
            painter.goto(-self.straight/2, -self.radius)
            painter.seth(0)
            painter.pendown()
            painter.begin_fill()
            painter.fd(self.straight)
            painter.circle(self.radius, 180)
            painter.fd(self.straight)
            painter.circle(self.radius, 180)
            painter.end_fill()
            # Paint lanes:
            for n in range(self.lanes):
                painter.penup()
                r = self.radius - self.lane_width * (n + 1)
                painter.goto(-self.straight/2, -r)
                painter.pendown()
                if n == self.lanes - 1:
                    painter.fillcolor('darkolivegreen2')
                    painter.begin_fill()
                painter.fd(self.straight)
                painter.circle(r, 180)
                painter.fd(self.straight)
                painter.circle(r, 180)
                painter.end_fill()
            # Paint the finishing line:
            painter.penup()
            painter.goto(self.straight/2, -self.radius)
            painter.seth(90)
            painter.pensize(5)
            painter.pendown()
            painter.fd(self.lanes * self.lane_width)
            painter.penup()
            painter.pensize(3)

    def start_lines(self, painter):
        """Prepare starting points. Requires using paint_stadium() method first."""
        # fit as many starting lines as possible on the last straight:
        lanes_straight = int(self.straight / (pi * 2 * self.lane_width))
        # fit starting lines on the arc:
        lanes_arc = int(self.radius / (2 *self.lane_width))
        # Draw starting lines on the lower straight:
        painter.speed(0)
        painter.penup()
        painter.goto(-self.straight/2 + (lanes_straight) * 2 * pi * self.lane_width, -self.radius)
        for n in range(lanes_straight + 1):
            painter.seth(90)
            painter.pendown()
            painter.fd(self.lane_width/2)
            painter.penup()
            painter.right(90)
            painter.back(18)
            self.start_positions.append(painter.position())
            self.start_angles.append(painter.heading())
            painter.fd(18)
            painter.left(90)
            painter.pendown()
            painter.fd(self.lane_width/2)
            painter.penup()
            painter.left(90)
            painter.fd(2 * pi * self.lane_width)
        # Draw starting lines on the left arc:
        painter.penup()
        n = lanes_straight + 1
        r = self.radius - self.lane_width * (n + 0.5)
        shift = 2 * pi * (n - lanes_straight) * self.lane_width
        angle = 180 * shift / (pi * r)
        while angle < 180:
            turtle_angle = 180 * 18 / (pi * r)
            painter.penup()
            painter.goto(-self.straight/2, -r)
            painter.seth(180)
            painter.circle(-r, angle + turtle_angle)
            painter.right(180)
            self.start_positions.append(painter.position())
            self.start_angles.append(painter.heading())
            painter.circle(r, turtle_angle)
            painter.left(90)
            painter.fd(self.lane_width/2)
            painter.pendown()
            painter.left(180)
            painter.fd(self.lane_width)
            painter.penup()
            n += 1
            r = self.radius - self.lane_width * (n + 0.5)
            shift = 2 * pi * (n - lanes_straight) * self.lane_width
            angle = 180 * shift / (pi * r)
        # Draw starting lines on the upper straight:
        distance = shift - pi * r
        while n < self.lanes:
            painter.goto(-self.straight/2 + distance + 18, r)
            painter.seth(180)
            self.start_angles.append(painter.heading())
            self.start_positions.append(painter.position())
            painter.fd(18)
            painter.right(90)
            painter.fd(self.lane_width/2)
            painter.left(180)
            painter.pendown()
            painter.fd(self.lane_width)
            painter.penup()
            n += 1
            r = self.radius - self.lane_width * (n + 0.5)
            shift = 2 * pi * (n - lanes_straight) * self.lane_width
            distance = shift - pi * r