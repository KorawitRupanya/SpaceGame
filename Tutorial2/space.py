import arcade
from random import randint
from models import World,Ship,Circle

 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

circles = []
n = 10


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
 
    def draw(self):
        self.sync_with_model()
        super().draw()
 
class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(width, height) 
        self.ship_sprite = ModelSprite('images/sword.png',model=self.world.ship)
        self.gold_sprite = ModelSprite('images/monster.png',model=self.world.gold)

        for i in range(n):
            circle = Circle(self.world,randint(100, SCREEN_WIDTH-100),
                        randint(100, SCREEN_HEIGHT-100),
                        randint(-5,5),
                        randint(-5,5),
                        randint(10,20))
            circles.append(circle)
 
 
    def on_draw(self):
        arcade.start_render()
        self.gold_sprite.draw()
        self.ship_sprite.draw()

        
        for c in circles:
            c.move()
            c.draw()
            if self.world.ship.is_hit(c):
                 self.world.ship.restart()
 
        arcade.draw_text(str(self.world.score),
                         self.width - 30, self.height - 30,
                         arcade.color.WHITE, 20)

    def update(self, delta):
        self.world.update(delta)
    
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()