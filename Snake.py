import math
import pygame


def circle_v_circle_collision(circle1, circle2):
    distance = (circle1.x - circle2.x)**2+(circle1.y - circle2.y)**2
    if distance < (circle1.radius + circle2.radius)**2:
        return True
    else:
        return False

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def render(self, screen):
        pygame.gfxdraw.filled_circle(screen, round(self.x), round(self.y), self.radius, (0,0,255))

class Snake:
    def __init__(self, name, controlls, x, y, angle, color):
        self.name = name
        self.score = 0
        self.controlls = controlls

        self.x = x
        self.y = y
        self.angle = angle
        self.color = color

        self.angleVelocity = math.pi/48
        self.velocity = 2
        self.thickness = 3

        self.polygon_list = [[(self.x + self.thickness*math.sin(self.angle + math.pi/2), self.y + self.thickness*math.cos(self.angle + math.pi/2)), (self.x + self.thickness*math.sin(self.angle - math.pi/2), self.y + self.thickness*math.cos(self.angle - math.pi/2)), (self.x + self.thickness*math.sin(self.angle + math.pi/2), self.y + self.thickness*math.cos(self.angle + math.pi/2)), (self.x + self.thickness*math.sin(self.angle - math.pi/2), self.y + self.thickness*math.cos(self.angle - math.pi/2))]]

        self.circle_list = []
        self.create_circle()
        #0 for forward, 1 for acw, -1 for cw
        self.moving = 0

    def update_score(self, placing):
        self.score += math.ceil(10/placing)

    def get_new_points(self):
        x1 = self.x + self.thickness*math.sin(self.angle + math.pi/2)
        y1 = self.y + self.thickness*math.cos(self.angle + math.pi/2)

        x2 = self.x + self.thickness*math.sin(self.angle - math.pi/2)
        y2 = self.y + self.thickness*math.cos(self.angle - math.pi/2)

        index = int(len(self.polygon_list[-1])/2)

        self.polygon_list[-1].insert(index, (x2,y2))
        self.polygon_list[-1].insert(index, (x1,y1))

    def update_current_point(self):
        x1 = self.x + self.thickness*math.sin(self.angle + math.pi/2)
        y1 = self.y + self.thickness*math.cos(self.angle + math.pi/2)

        x2 = self.x + self.thickness*math.sin(self.angle - math.pi/2)
        y2 = self.y + self.thickness*math.cos(self.angle - math.pi/2)

        index = int(len(self.polygon_list[-1])/2)
        self.polygon_list[-1][index] = (x2, y2)
        self.polygon_list[-1][index-1] = (x1, y1)

    def set_moving(self, dir):
        self.moving = dir

    def turn_cw(self):
        self.angle += self.angleVelocity

    def turn_acw(self):
        self.angle -= self.angleVelocity

    def update_position(self):
        if self.moving == -1:
            self.turn_acw()
            self.get_new_points()
        elif self.moving == 1:
            self.turn_cw()
            self.get_new_points()
        else:
            self.update_current_point()

        self.x += self.velocity * math.sin(self.angle)
        self.y += self.velocity * math.cos(self.angle)

    def cut_polygon(self):
        self.polygon_list.append([(self.x + self.thickness*math.sin(self.angle + math.pi/2), self.y + self.thickness*math.cos(self.angle + math.pi/2)), (self.x + self.thickness*math.sin(self.angle - math.pi/2), self.y + self.thickness*math.cos(self.angle - math.pi/2)), (self.x + self.thickness*math.sin(self.angle + math.pi/2), self.y + self.thickness*math.cos(self.angle + math.pi/2)), (self.x + self.thickness*math.sin(self.angle - math.pi/2), self.y + self.thickness*math.cos(self.angle - math.pi/2))])


    def render(self, screen):
        for polygon in self.polygon_list:
            pygame.gfxdraw.filled_polygon(screen, polygon, self.color)
        pygame.gfxdraw.filled_circle(screen, round(self.x), round(self.y), self.thickness, self.color)
        #for circle in self.circle_list:
        #    circle.render(screen)

    def render_dir_vector(self, screen):
        x_end = round(self.x + 10*self.velocity * math.sin(self.angle))
        y_end = round(self.y + 10*self.velocity * math.cos(self.angle))
        pygame.gfxdraw.line(screen, self.x, self.y, x_end, y_end, (255,255,255))


    def create_circle(self):
        circle = Circle(self.x, self.y, self.thickness)
        self.circle_list.append(circle)

    def get_circle_list(self):
        return self.circle_list

    def get_snake_circle(self):
        return Circle(self.x, self.y, self.thickness)

    def check_out_of_bounds(self):
        if self.x > 900:
            self.x = 0
            self.cut_polygon()

        elif self.x < 0:
            self.x = 900
            self.cut_polygon()

        if self.y > 600:
            self.y = 0
            self.cut_polygon()

        elif self.y < 0:
            self.y = 600
            self.cut_polygon()

    def check_out_of_bounds_kill(self):
        if self.x > 900:
            return True

        elif self.x < 0:
            return True

        elif self.y > 600:
            return True

        elif self.y < 0:
            return True

        else:
            return False
