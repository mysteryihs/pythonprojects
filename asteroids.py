# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
rock_group = set([])
missile_group = set([])
explosion_group = set([])
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.5)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        global forward
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] *= .98
        self.vel[1] *= .98
        forward = angle_to_vector(self.angle)
        if self.thrust == True:
            self.vel[0] += forward[0] * 0.3
            self.vel[1] += forward[1] * 0.3
            self.image_center[0] = 135
            ship_thrust_sound.play()
        else:
            self.image_center[0] = 45
            ship_thrust_sound.rewind()
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH
        if self.pos[1] > HEIGHT:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
            
    def shoot(self):
        global a_missile, missile_group
        forward = angle_to_vector(self.angle)
        a_missile = Sprite([my_ship.pos[0] + forward[0] * my_ship.radius, my_ship.pos[1] + forward[1] * my_ship.radius], [forward[0] * 7 + my_ship.vel[0], forward[1] * 7  + my_ship.vel[1]], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):         
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        self.pos[0] += self.vel[0]       
        self.pos[1] += self.vel[1]  
        self.angle += self.angle_vel
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH
        if self.pos[1] > HEIGHT:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
            
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius()

def draw(canvas):
    global time, lives, started, rock_group, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives: ' + str(lives), (20, 50), 50, 'White')
    canvas.draw_text('Score: ' + str(score), (575, 50), 50, 'White')

    # draw ship and sprites
    my_ship.draw(canvas)
    #rock_group.draw(canvas)
    #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    #rock_group.update()
    #a_missile.update()
    process_sprite_group(rock_group, canvas)
    group_collide(rock_group, my_ship)
    process_sprite_group(missile_group, canvas)
    group_group_collide(missile_group, rock_group)
    if lives == 0:
        started = False
        rock_group = set([])
        soundtrack.pause()
        soundtrack.rewind()
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
            
def key_up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel -= 0.1
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel += 0.1
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP['space']:
        timer2.start()
    
def key_down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel += 0.1
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel -= 0.1
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        timer2.stop()
        
def process_sprite_group(rock_group, canvas):
    a = set([])
    for rock in rock_group:
        canvas.draw_image(rock.image, rock.image_center, rock.image_size, rock.pos, rock.image_size, rock.angle)
        rock.update()
        rock.collide(my_ship)
        if rock.update() == True:
            a.add(rock)
            rock_group.difference_update(a)
        
def group_collide(group, other_object):
    global lives, score
    a = set([])
    for item in group:
        if item.collide(other_object) == True:
            if other_object == my_ship:
                lives -= 1
            a.add(item)
            group.difference_update(a)
            return True

def group_group_collide(group1, group2):
    global score
    a = set([])
    for item in list(group1):
        collision = group_collide(group2, item)
        if collision == True:
            group1.discard(item)
            score += 1

def shoot():
    my_ship.shoot()
        
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()
        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship, score
    c = 0.5
    if score >= 50:
        c = 2.5
    elif score >= 40:
        c = 2
    elif score >= 30:
        c = 1.5
    elif score >= 20:
        c = 1
    elif score >= 15:
        c = .75
    elif score >= 5:
        c = .5
    if started == True:
        if len(rock_group) < 12:
            randompos = [random.randrange(1, WIDTH), random.randrange(1, HEIGHT)]
            if dist(randompos, my_ship.pos) <= my_ship.get_radius() + 100:
                pass
            else:
                a_rock = Sprite(randompos, [random.randrange(-2, 2) * c, random.randrange(-2, 2) * c], 0, (random.randrange(-1, 2) * 0.1), asteroid_image, asteroid_info)
                rock_group.add(a_rock)

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([0,0], [0,0], 0, 0, debris_image, missile_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_up)
frame.set_keyup_handler(key_down)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)
timer2 = simplegui.create_timer(150.0, shoot)
timer2.stop()

# get things rolling
timer.start()
frame.start()
