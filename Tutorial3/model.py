import arcade.key
from random import randint

DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
 
DIR_OFFSET = { DIR_UP: (0,1),
               DIR_RIGHT: (1,0),
               DIR_DOWN: (0,-1),
               DIR_LEFT: (-1,0) }

KEY = {arcade.key.UP:(DIR_UP),arcade.key.DOWN:(DIR_DOWN),arcade.key.LEFT:(DIR_LEFT),arcade.key.RIGHT:(DIR_RIGHT)}

class Snake:
    MOVE_WAIT = 0.2
    BLOCK_SIZE = 16

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
 
        self.body = [(x,y),
                     (x-Snake.BLOCK_SIZE, y),
                     (x-2*Snake.BLOCK_SIZE, y)]
        self.length = 3
        self.wait_time = 0
        self.direction = DIR_RIGHT
        self.has_eaten = False
 
    def update(self, delta):
        self.wait_time += delta
 
        if self.wait_time < Snake.MOVE_WAIT:
            return
 
        if self.x > self.world.width:
            self.x = 0
        self.x += DIR_OFFSET[self.direction][0]*self.BLOCK_SIZE
        if self.y > self.world.height:
            self.y = 0 
        self.y += DIR_OFFSET[self.direction][1]*self.BLOCK_SIZE

        self.body.insert(0,(self.x,self.y))
        self.body.pop()
        self.wait_time = 0

        if self.has_eaten:
            self.length += 1
            self.body.insert(self.length-1,(self.x,self.y))
            self.has_eaten = False

    
    def can_eat(self, heart):
        if self.x==heart.x and self.y == heart.y:
            return True

class SnakeSprite:
    def __init__(self, snake):
        self.snake = snake
        self.block_sprite = arcade.Sprite('images/block.png')
 
    def draw(self):
        for x,y in self.snake.body:
            self.block_sprite.set_position(x,y)
            self.block_sprite.draw()

class Heart:
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
 
    def random_position(self):
        centerx = self.world.width // 2
        centery = self.world.height // 2
        
        self.x = centerx + randint(-15,15) * Snake.BLOCK_SIZE
        self.y = centerx + randint(-15,15) * Snake.BLOCK_SIZE

        while self.x==self.world.snake.x and self.y == self.world.snake.y:
            self.x = centerx + randint(-15,15) * Snake.BLOCK_SIZE
            self.y = centerx + randint(-15,15) * Snake.BLOCK_SIZE

class HeartSprite:
    def __init__(self, heart):
        self.heart = heart
        self.block_sprite = arcade.Sprite('images/heart.png')
 
    def draw(self):
        self.block_sprite.set_position(self.heart.x,self.heart.y)
        self.block_sprite.draw()
 
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heart = Heart(self)
        self.snake = Snake(self, width // 2, height // 2)
        self.heart.random_position()
        self.snake.has_eaten = False        
 
 
    def on_key_press(self, key, key_modifiers):
     self.snake.direction=KEY[key]



    def update(self, delta):
        self.snake.update(delta)
 
        if self.snake.can_eat(self.heart):
            self.heart.random_position()
            self.snake.has_eaten = True