import pygame
from os import path

snd_dir = path.join(path.dirname(__file__), 'assets')
snd_dir = path.join(snd_dir, 'audio')

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

walk_sound = []

try:
    pygame.mixer.music.load(path.join(snd_dir, 'bgm.wav'))
    victory = pygame.mixer.Sound(path.join(snd_dir, 'winner.wav'))
    accept = pygame.mixer.Sound(path.join(snd_dir, 'button_click.wav'))
    roll_sound = pygame.mixer.Sound(path.join(snd_dir, 'roll_sound.wav'))
    card_flip = pygame.mixer.Sound(path.join(snd_dir, 'card_flip.wav'))
    walk_sound.append(pygame.mixer.Sound(path.join(snd_dir, 'foot1.wav')))
    walk_sound.append(pygame.mixer.Sound(path.join(snd_dir, 'foot2.wav')))
    button_click = pygame.mixer.Sound(path.join(snd_dir, 'button_click.wav'))
    lose = pygame.mixer.Sound(path.join(snd_dir, 'lose.wav'))
    
except:
    print("Sound loaded error")
