import pygame
from random import randint
from math import sqrt, atan2, sin, cos, pi 

#WINDOW SIZE
WIDTH = 1200
HEIGHT = 900

#SIMULATION
G = 1e-2 #G = 6.67428e-11
OBJECTS_NUM = 10
DENSITY = 20

objects_list = []

class Vector2D(object):

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_length(self):
        return sqrt(self.x**2+self.y**2)
    
    def get_distance(self, other):
        return sqrt((other.x - self.x)**2+(other.y - self.y)**2)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        return Vector2D(self.x*other, self.y*other)
    
    def __truediv__(self, other):
        return Vector2D(self.x/other, self.y/other)
    
    def __lt__(self, other):
        return self.get_length() < other.get_length()


class Object:
    mass = 10
    radius = 10
    position = Vector2D(0, 0)
    velocity = Vector2D(0, 0)

    def __init__(self):
        #Set starting random position
        padding = 20
        self.position = Vector2D(randint(padding, WIDTH-padding), randint(padding, HEIGHT-padding))
        self.set_mass(randint(1e3, 1e4))

    def set_mass(self, nmass):
        self.mass = nmass
        #Update radius from mass
        self.radius = sqrt(self.mass/DENSITY/pi)

    def add_velocity(self, velocity: Vector2D):
        self.velocity += (velocity / self.mass)

    def update_velocity(self):
        for other_object in objects_list:
            if other_object is self: continue
            #Get distance between objects
            distance = self.position.get_distance(other_object.position)

            force = G * self.mass * other_object.mass / (distance**2)
            # Calculate angle between planets
            dx = other_object.position.x - self.position.x
            dy = other_object.position.y - self.position.y
            angle = atan2(dy, dx)  

            gravity_force = Vector2D(force*cos(angle), force*sin(angle))

            self.add_velocity(gravity_force)
    
    def update_position(self):
        self.position += self.velocity


class Window():

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Gravity Simulation')
        self.screen.fill((0, 0, 0))

    def clear(self):
        self.screen.fill((0, 0, 0))

    def draw_object(self, obj):
        COORD = (obj.position.x, obj.position.y)
        pygame.draw.circle(self.screen, (255,255,255), COORD, obj.radius)

#SIMULATION
def update_object(obj):
    obj.update_velocity()
    obj.update_position()

    #Check for collision
    for obj_other in objects_list:
        if obj_other is obj: continue
        #Get distance between
        distance = obj.position.get_distance(obj_other.position)

        if distance < obj.radius+obj_other.radius:
           on_collision(obj, obj_other)

    
    #Bounds
    if obj.position.x-obj.radius <= 0 and obj.velocity.x < 0:
        obj.velocity.x = -obj.velocity.x
    elif obj.position.x+obj.radius >= WIDTH and obj.velocity.x > 0:
        obj.velocity.x = -obj.velocity.x
    elif obj.position.y-obj.radius <= 0 and obj.velocity.y < 0:
        obj.velocity.y = -obj.velocity.y
    elif obj.position.y+obj.radius >= HEIGHT and obj.velocity.y > 0:
        obj.velocity.y = -obj.velocity.y

    return False

def on_collision(obj1, obj2):
    if  obj1.mass >= obj2.mass:
        obj1.add_velocity(obj2.velocity)
        obj1.set_mass(obj1.mass + obj2.mass)
        objects_list.remove(obj2)

#MAIN LOOP
from time import sleep
if __name__ == '__main__':
    running = True

    window = Window()
    #
    for i in range(0, OBJECTS_NUM):
            #Create new object
            new_object = Object()

            #Store the object
            objects_list.append(new_object)
    
    deltatime = 1/60

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        window.clear()

        #Update all objects positions
        for obj in objects_list:
            update_object(obj)

            window.draw_object(obj)

        pygame.display.update()
        sleep(deltatime)
    pygame.quit()
