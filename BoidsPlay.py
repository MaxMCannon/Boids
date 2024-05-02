# Example file showing a circle moving on screen
import pygame
import random
import math

class Boid:
    def __init__(self):
        self.pos = pygame.Vector2(random.random()*screen.get_width(), random.random()*screen.get_height())
        self.vel = pygame.Vector2(random.choice([-1, 1]) * random.random()*150, random.choice([-1, 1]) * random.random()*150)

    def draw(self):
        # tip_point = (self.pos.x+(20*math.cos(self.dir)), self.pos.y-(20*math.cos(self.dir)))
        # left_wing = (self.pos.x-10, self.pos.y-10)
        # right_wing = (self.pos.x-10, self.pos.y+10)
        # points = [tip_point, left_wing, right_wing]
        # pygame.draw.polygon(screen, "grey",  points)
        # pygame.draw.circle(screen, "red", tip_point, 2)
        pygame.draw.circle(screen, "black", self.pos, 5)
    
    def rotate(self):
        self.pos.rotate_rad(math.pi/16)

    def move(self):
        XMin = 0
        XMax = screen.get_width()
        YMin = 0
        YMax = screen.get_height()
        margin = 200
        rebound = 3
        self.pos.x += self.vel.x * dt
        self.pos.y += self.vel.y * dt
        if self.pos.x >= XMax:
            self.pos.x = XMin
        elif self.pos.x <= XMin:
            self.pos.x = XMax

        if self.pos.y >= YMax:
            self.pos.y = YMin
        elif self.pos.y <= YMin:
            self.pos.y = YMax

        # NOT WORKING
        # if self.pos.x - margin >= XMax:
        #     self.vel.x -= rebound
        # elif self.pos.x + margin <= XMin:
        #     self.vel.x += XMax

        # if self.pos.y >= YMax-margin:
        #     self.vel.y -= rebound
        # elif self.pos.y <= YMin+margin:
        #     self.vel.y += YMax
        
        maxspeed = 200
        minspeed = 150
        self.vel.clamp_magnitude_ip(minspeed, maxspeed)

def Rule1(boid):
    c = pygame.Vector2(0, 0)
    view = 150
    count = 0
    for b in boidlist:
        if boid.pos.distance_to(b.pos) <= view:
            count += 1
            c = c + b.pos
    if count >= 1:
        c = c / count
    return (c - boid.pos)/100


def Rule2(boid):
    c = pygame.Vector2(0, 0)
    view = 25
    for b in boidlist:
        if b != boid:
            if math.fabs(b.pos.distance_to(boid.pos)) < view:
                c = c - (b.pos - boid.pos)
    return c

def Rule3(boid):
    v = pygame.Vector2(0, 0)
    view = 150
    count = 0
    for b in boidlist:
        if boid.pos.distance_to(b.pos) <= view:
            # print(boid.pos.distance_to(b.pos))
            count += 1
            v += b.vel
    if count > 1:   
        # print(v)
        v = v / count
        # print(v)
    return (v - boid.vel)/8


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

points = [(player_pos.y + 20, player_pos.x), (player_pos.y-10, player_pos.x-10), (player_pos.y-10, player_pos.x+10)]
start_dir = 0
#player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

boidlist = []
for i in range(150):
    boidlist.append(Boid())

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")
    if pygame.mouse.get_pressed()[0] == True:
        for b in boidlist:
            b.draw()
            clickv = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) - b.pos
            b.vel += clickv
            b.move()

    for b in boidlist:
        b.draw()
        clickv = pygame.Vector2(0, 0)
        b.vel += Rule1(b) + Rule2(b) + Rule3(b)
        b.move()
    # points = [(player_pos.y + 20, player_pos.x), (player_pos.y-10, player_pos.x-10), (player_pos.y-10, player_pos.x+10)]
    # pygame.draw.polygon(screen, "grey",  points)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        for i in range(1):
            boidlist.append(Boid())
    if keys[pygame.K_s]:
        for i in range(len(boidlist)):
            boidlist.pop()
    if keys[pygame.K_d]:
        pass



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
