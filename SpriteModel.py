import pygame
from os import path

#Define
BLACK =  (0, 0, 0)

img_dir = path.join(path.dirname(__file__), 'assets')
img_dir = path.join(img_dir, 'images')

dice_dir = path.join(img_dir, 'dices')
button_dir = path.join(img_dir, 'buttons')
santa_dir = path.join(img_dir, 'santa')
ai_dir = path.join(img_dir, 'ai')
card_dir = path.join(img_dir, 'cards')

map_image = None
scene = []

dice_img_ani = {}
dice_img_ani["roll"] = []
dice_img_ani["face"] = []

button_img_ani = {}
button_img_ani["idle"] = []
button_img_ani["hover"] = []
button_img_ani["click"] = []

santa_img_ani = {}
santa_img_ani["east"] = []
santa_img_ani["west"] = []

ai_img_ani = {}
ai_img_ani["east"] = []
ai_img_ani["west"] = []

card_img_ani = {}
card_img_ani["idle"] = []
card_img_ani["move_fw_3"] = []
card_img_ani["move_bw_2"] = []
card_img_ani['snake_or_ladder'] = []

# Load Dice Images
try:
    for i in range (1, 25): #Dice roll animation upload.
        filename = ""
        
        if (i < 10):
            filename = '000{}.png'.format(i)
        else:
            filename = '00{}.png'.format(i)
            
        roll_img = pygame.image.load(path.join(dice_dir, filename))
        roll_img.set_colorkey(BLACK)
        dice_img_ani["roll"].append(roll_img)
    
    for i in range (25, 31):
        filename = '00{}.png'.format(i)
        face_img = pygame.image.load(path.join(dice_dir, filename))
        face_img.set_colorkey(BLACK)
        dice_img_ani["face"].append(face_img)
   
    print("Loading " + str(filename) + " done.")
        
except:
    print("Dice images upload failed.")
    
# Load map image
try:
    map_img = pygame.image.load(path.join(img_dir, 'map.jpg'))
    map_img.set_colorkey(BLACK)
    print("Loading map.jpg done.")
except:
    print("Map download failed.")

# Load button images
try:
    for i in range (1, 27):
        filename = 'button_{}.png'.format(i)
        button_img = pygame.image.load(path.join(button_dir, filename))
        button_img.set_colorkey(BLACK)
        button_img_ani["idle"].append(button_img)
   
    print("Loading " + str(filename) + " done.")
except:
    print("Button download failed.")

# Load Santa images
try:
    filename = ['santa_east_1.png', 'santa_west_1.png']
    santa_img = pygame.image.load(path.join(santa_dir, filename[0]))
    santa_img.set_colorkey(BLACK)
    santa_img_ani["east"].append(santa_img)

    santa_img = pygame.image.load(path.join(santa_dir, filename[1]))
    santa_img.set_colorkey(BLACK)
    santa_img_ani["west"].append(santa_img)

    print("Loading " + str(filename) + " done.")
except:
    print("Santa download fail.")

# Load AI images
try:
    filename = ['ai_east.png', 'ai_west.png']
    ai_img = pygame.image.load(path.join(ai_dir, filename[0]))
    ai_img.set_colorkey(BLACK)
    ai_img_ani["east"].append(ai_img)

    ai_img = pygame.image.load(path.join(ai_dir, filename[1]))
    ai_img.set_colorkey(BLACK)
    ai_img_ani["west"].append(ai_img)

    print("Loading " + str(filename) + " done.")
except:
    print("Santa download fail.")

# Load Card images
try:
    filename = ['card0.png', 'card1.png', 'card2.png', 'card3.png']
    card_img = pygame.image.load(path.join(card_dir, filename[0]))
    card_img.set_colorkey(BLACK)
    card_img_ani["idle"].append(card_img)

    card_img = pygame.image.load(path.join(card_dir, filename[1]))
    card_img.set_colorkey(BLACK)
    card_img_ani["move_fw_3"].append(card_img)

    card_img = pygame.image.load(path.join(card_dir, filename[2]))
    card_img.set_colorkey(BLACK)
    card_img_ani["move_bw_2"].append(card_img)

    card_img = pygame.image.load(path.join(card_dir, filename[3]))
    card_img.set_colorkey(BLACK)
    card_img_ani["snake_or_ladder"].append(card_img)

    print("Loading " + str(filename[-1]) + " done.")
except:
    print("Card download fail.")

print("--------------------------\n\n")


class Dice(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):   # Parameter for specifing Dice position
        super().__init__()
        self.animated = "face"
        self.image = dice_img_ani[self.animated][0]
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.center = [self.x, self.y]
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
        self.random_value = 1

    def update(self):
        if (self.animated == "face"):
            self.image = dice_img_ani[self.animated][self.random_value - 1]
            return                      # no animation run for showing dice face
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.frame += 1
            if self.frame < len(dice_img_ani[self.animated]) : #Frame First - Last
                self.image = dice_img_ani[self.animated][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = [self.x, self.y]
            if (self.frame == (len(dice_img_ani[self.animated])) - 1):
                self.animated = "face"


class MapGame(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.animated = "idle"
        self.image = map_img
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.animated = "idle"
        self.image = button_img_ani[self.animated][0]
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.center = [self.x, self.y]
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30
        

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.frame += 1
            if self.frame < len(button_img_ani[self.animated]) : #Frame First - Last
                self.image = button_img_ani[self.animated][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = [self.x, self.y]
            if (self.frame == (len(button_img_ani[self.animated])) - 1):
                self.frame = 0

class Santa(pygame.sprite.Sprite) :
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.animated = "east"
        self.image = santa_img_ani[self.animated][0]
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.center = [self.x, self.y]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.current_grid = 1
        self.new_grid = 1


    def update(self) : #Change frame and animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now
            #self.rect = self.image.get_rect()
            self.rect.center = [self.x, self.y]
            if ((self.current_grid >= 11 and self.current_grid < 21) or
                (self.current_grid >= 31 and self.current_grid < 41) or
                (self.current_grid >= 51 and self.current_grid < 61) or
                (self.current_grid >= 71 and self.current_grid < 81) or
                (self.current_grid >= 91 and self.current_grid < 101)):

                self.animated = 'west'
                self.image = santa_img_ani[self.animated][0]
            else:
                self.animated = 'east'
                self.image = santa_img_ani[self.animated][0]
            

class Card(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.frame = 0
        self.animated = 'idle'
        self.image = card_img_ani[self.animated][self.frame]
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.center = [self.x, self.y]

    def update(self):
        self.image = card_img_ani[self.animated][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

class AI(pygame.sprite.Sprite) :
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.animated = "east"
        self.image = ai_img_ani[self.animated][0]
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.center = [self.x, self.y]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.current_grid = 1
        self.new_grid = 1


    def update(self) : #Change frame and animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate :
            self.last_update = now
            self.rect = self.image.get_rect()
            self.rect.center = [self.x, self.y]
            if ((self.current_grid >= 11 and self.current_grid < 21) or
                (self.current_grid >= 31 and self.current_grid < 41) or
                (self.current_grid >= 51 and self.current_grid < 61) or
                (self.current_grid >= 71 and self.current_grid < 81) or
                (self.current_grid >= 91 and self.current_grid < 101)):

                self.animated = 'west'
                self.image = ai_img_ani[self.animated][0]
            else:
                self.animated = 'east'
                self.image = ai_img_ani[self.animated][0]
            
class Button_choice(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, pic_name):
        super().__init__()
        self.image = pygame.image.load(path.join(button_dir, pic_name))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

class EndScene(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, pic_name):
        super().__init__()
        self.image = pygame.image.load(path.join(img_dir, pic_name))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
  
