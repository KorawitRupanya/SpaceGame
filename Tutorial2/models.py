import arcade.key,math
from random import randint

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0
    
    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class Circle(Model):
    def __init__(self,world, x, y, vx, vy, r=20):
        self.world = world
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
 
    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x > self.world.width - self.r  \
                or self.x < self.r : 
            self.vx *= -1
        if self.y > self.world.height - self.r \
                or self.y < self.r :
            self.vy *= -1

    def stop(self):
        arcade.draw_circle_outline(self.x, self.y,
                                   self.r, arcade.color.WHITE)
        
    def draw(self):
        arcade.draw_circle_outline(self.x, self.y,
                                   self.r, arcade.color.WHITE)

class Ship(Model):
    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1
    
 
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
 
        self.direction = Ship.DIR_VERTICAL
 
 
    def switch_direction(self):
        if self.direction == Ship.DIR_HORIZONTAL:
            self.direction = Ship.DIR_VERTICAL
            self.angle = 0
        else:
            self.direction = Ship.DIR_HORIZONTAL
            self.angle = -90 
 
 
    def update(self, delta):
        if self.direction == Ship.DIR_VERTICAL:
            if self.y > self.world.height:
                self.y = 0
            self.y += 5
        else:
            if self.x > self.world.width:
                self.x = 0
            self.x += 5

    def restart(self):
        self.x = 0 
        self.y = 0

    def is_hit(self, circle):
        a = self.x - circle.x 
        b = self.y - circle.y
        c = math.sqrt(((a**2)+(b**2)))
        if c < 10+circle.r:
            return True
        return False

class Gold(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height - 1)

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
 
        self.ship = Ship(self,100, 100)
        self.gold = Gold(self, 400, 400)
 
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()
 
    def update(self, delta):
        self.ship.update(delta)
 
        if self.ship.hit(self.gold, 10):
            self.gold.random_location()
            self.score += 1