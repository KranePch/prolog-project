import random
import time
import sys

from SpriteModel import *
from PrologFunction import *
from AudioMixer import *

display_width = 1200
display_height = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STEP = 20                # TO-DO Changes to 200 ---------------

isWinner = -1

#Initialize Object
dice_st = Dice(165, 100)
dice_nd = Dice(245, 100)

dice_group = pygame.sprite.Group()
dice_group.add(dice_st)
dice_group.add(dice_nd)

game_map = MapGame(800, 400)

game_map_group = pygame.sprite.Group()
game_map_group.add(game_map) 

button = Button(200, 700)

button_group = pygame.sprite.Group()
button_group.add(button)

button1 = Button_choice(100, 650, 'ladder2.png')
button2 = Button_choice(300, 650, 'snake2.png')

button_selector_group = pygame.sprite.Group()
button_selector_group.add(button1) 
button_selector_group.add(button2)  

santa = Santa(435, 750)

santa_group = pygame.sprite.Group()
santa_group.add(santa)

card = Card(200, 400)

card_group = pygame.sprite.Group()
card_group.add(card)

ai = AI(435, 750)

ai_group = pygame.sprite.Group()
ai_group.add(ai)

#Initialize Grid Coordinate
grid_coordinate = [[0, 0] for i in range(100)]
for i in range (10):
    for j in range (10):
        if (i % 2 == 0):
            grid_coordinate[(i * 10) + j] = [435 + (80 * j), 750 - (80 * i)]
        else:
            grid_coordinate[(i * 10) + j] = [1155 - (80 * j), 750 - (80 * i)]

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Rollog")
clock = pygame.time.Clock()
pygame.mixer.music.play(-1)

#Function
def activate_to(who: int, obj, used_by: str):
    global isSelectingCard
    isSelectingCard = False
    
    global isActivated
    isActivated = True
    
    if (who == 2):      # Discard the card
        return
    
    if (card.animated == 'move_fw_3'):
        obj.new_grid = add_pos(who, 3)
    elif (card.animated == 'move_bw_2'):
        obj.new_grid = add_pos(who, -2)
    else:
        if (used_by == 'ai'):
            if (who == 1):
                nearest_ladder = find_nearest_ladder(who)
                obj.new_grid = nearest_ladder
            else:
                nearest_snake = find_nearest_snake(who)
                obj.new_grid = nearest_snake
        else:
            player_decision = select_snake_or_ladder()
            if (player_decision == 0):
                nearest_ladder = find_nearest_ladder(who)
                obj.new_grid = nearest_ladder
            else:
                nearest_snake = find_nearest_snake(who)
                obj.new_grid = nearest_snake
     
    obj.current_grid = obj.new_grid
    obj.x = grid_coordinate[obj.new_grid - 1][0]
    obj.y = grid_coordinate[obj.new_grid - 1][1]
    update_pos(who, obj.new_grid)

    if (who == 1):
        move_ai_from_snake()
        move_ai_from_ladder()
    else:
        move_player_from_snake()
        move_player_from_ladder()

def move_to_selected_event(who: int, nearest_event: int):
    if (who == 1):  # moves AI
        ai.new_grid = update_pos(1, nearest_event)
    else:
        santa.new_grid = update_pos(0, nearest_event)

def player_move():
    if (santa.x != grid_coordinate[santa.new_grid - 1][0]
        or santa.y != grid_coordinate[santa.new_grid - 1][1]):
        santa.current_grid += 1
        walk_sound[random.randint(0, 1)].play()
        santa.x = grid_coordinate[santa.current_grid ][0]
        santa.y = grid_coordinate[santa.current_grid ][1]
        
        if(santa.current_grid == santa.new_grid - 1):
            return True
        return False

def ai_move():
    if (ai.x != grid_coordinate[ai.new_grid - 1][0]
        or ai.y != grid_coordinate[ai.new_grid - 1][1]):
        ai.current_grid += 1
        walk_sound[random.randint(0, 1)].play()
        ai.x = grid_coordinate[ai.current_grid ][0]
        ai.y = grid_coordinate[ai.current_grid ][1]
        
        if(ai.current_grid == ai.new_grid - 1):
            return True
        return False

def move_player_from_snake():
    if (at_snake(0)):
        snake_tail = list(prolog.query("snake(" + str(get_player_position()) + ", X)"))[0]['X']
        santa.new_grid = snake_tail
        santa.current_grid = santa.new_grid
        santa.x = grid_coordinate[snake_tail - 1][0]
        santa.y = grid_coordinate[snake_tail - 1][1]
        update_pos(0, santa.new_grid)
        return True
    return False

def move_ai_from_snake():
    if (at_snake(1)):
        snake_tail = list(prolog.query("snake(" + str(get_ai_position()) + ", X)"))[0]['X']
        santa.new_grid = snake_tail
        ai.current_grid = ai.new_grid
        ai.x = grid_coordinate[snake_tail - 1][0]
        ai.y = grid_coordinate[snake_tail - 1][1]
        update_pos(1, ai.new_grid)
        return True
    return False

def move_player_from_ladder():
    if (at_ladder(0)):
        ladder_dest = list(prolog.query("ladder(" + str(get_player_position()) + ", X)"))[0]['X']
        santa.new_grid = ladder_dest
        santa.current_grid = santa.new_grid
        santa.x = grid_coordinate[ladder_dest - 1][0]
        santa.y = grid_coordinate[ladder_dest - 1][1]
        update_pos(0, santa.new_grid)
        return True
    return False

def move_ai_from_ladder():
    if (at_ladder(1)):
        ladder_dest = list(prolog.query("ladder(" + str(get_ai_position()) + ", X)"))[0]['X']
        ai.new_grid = ladder_dest
        ai.current_grid = ai.new_grid
        ai.x = grid_coordinate[ladder_dest - 1][0]
        ai.y = grid_coordinate[ladder_dest - 1][1]
        update_pos(1, ai.new_grid)
        return True
    return False

def select_snake_or_ladder():
    selected_choice = -1
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (button1.rect.collidepoint(x,y)):
                    button1.kill()
                    button2.kill()
                    button_click.play()
                    return 0
                        
                if (button2.rect.collidepoint(x,y)):
                    button1.kill()
                    button2.kill()
                    button_click.play()
                    return 1
                
        screen.fill(BLACK)
      
        dice_group.draw(screen)
        dice_group.update()

        button_group.draw(screen)
        button_group.update()
       
        game_map_group.draw(screen)
        game_map_group.update()

        santa_group.draw(screen)
        santa_group.update()

        ai_group.draw(screen)
        ai_group.update()

        card_group.draw(screen)
        card_group.update()

        button_selector_group.draw(screen)
        button_selector_group.update()

        clock.tick(FPS)
        pygame.display.flip()
        
# Graphic Driver
def update_all():
    screen.fill(BLACK)
    
    dice_group.draw(screen)
    dice_group.update()

    button_group.draw(screen)
    button_group.update()
       
    game_map_group.draw(screen)
    game_map_group.update()

    santa_group.draw(screen)
    santa_group.update()

    ai_group.draw(screen)
    ai_group.update()

    card_group.draw(screen)
    card_group.update()

    clock.tick(FPS)
    pygame.display.flip()

# Main Driver
def player_turn():
    isRolled = False
    isWalking = False
    total_value = 0
    driver_last_update = 0
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (button.rect.collidepoint(x,y) and not isRolled):
                    isRolled = True
                    roll_sound.play()
                    dice_st.frame = 0
                    dice_st.animated = "roll"

                    dice_nd.frame = 0
                    dice_nd.animated = "roll"

                    dice_st.random_value = roll_dice()
                    dice_nd.random_value = roll_dice()

                    total_value = dice_st.random_value + dice_nd.random_value
                    # ---------------- Make a test here -------------------
                    #total_value = 40
                    
                    santa.current_grid = get_player_position()
                    santa.new_grid = add_pos(0, total_value)

                    update_pos(0, santa.new_grid)

        if (dice_st.animated == "face" and dice_nd.animated == "face"
            and isRolled):
            driver_now = pygame.time.get_ticks()
            if (driver_now - driver_last_update > (FPS + STEP)):
                driver_last_update = driver_now

                # Update Animation
                if (player_move()):
                    break
        
        update_all()

def ai_turn():
    isRolled = False
    driver_last_update = 0
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        if not isRolled:
            dice_st.frame = 0
            dice_st.animated = "roll"

            dice_nd.frame = 0
            dice_nd.animated = "roll"
            
            dice_st.random_value = roll_dice()
            dice_nd.random_value = roll_dice()

            total_value = dice_st.random_value + dice_nd.random_value
            # --------------- Make a test here -------------------
            #total_value = 20

            ai.current_grid = get_ai_position()
            ai.new_grid = add_pos(1, total_value)

            update_pos(1, ai.new_grid)
            roll_sound.play()
            isRolled = True

        if (dice_st.animated == "face" and dice_nd.animated == "face"
            and isRolled):
            driver_now = pygame.time.get_ticks()
            if (driver_now - driver_last_update > (FPS + STEP)):
                driver_last_update = driver_now

                # Update Animation
                if (ai_move()):
                    break
        
        update_all()

            
                    
def check_player_state():
    global isSelectEventCard
    isSelectEventCard = False

    isDone = False
    driver_last_update = 0
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and isSelectEventCard:
                x, y = event.pos
                if (santa.rect.collidepoint(x, y)):
                    activate_to(0, santa, 'player')
                    return
                        
                elif (ai.rect.collidepoint(x, y)):
                    activate_to(1, ai, 'player')
                    return
                    
                
                    
        if (move_player_from_snake()):
            break
            
        if (move_player_from_ladder()):
            break

        if (at_card(0) and not isSelectEventCard):
            player_random_card = get_random_card()
            # --------------- Make a test here ----------------------
                # move_fw_3, move_bw_2, snake_or_ladder
            #player_random_card = 'snake_or_ladder'
            
            card.animated = player_random_card
            
            isSelectEventCard = True
            
        if (not at_card(0) and not isSelectEventCard):
            break
        update_all()

def check_ai_state():
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (move_ai_from_snake()):
            break
            
        if (move_ai_from_ladder()):
            break

        if (at_card(1)):
            ai_random_card = get_random_card()
            # --------------- Make a test here ----------------------
                # move_fw_3, move_bw_2, snake_or_ladder
            #ai_random_card = 'snake_or_ladder'
            
            card.animated = ai_random_card

            decide = make_decision(card.animated)
            
            if (decide == 0):
                activate_to(decide, santa, 'ai')
            else:
                activate_to(decide, ai, 'ai')
            break
        
        if (not at_card(1)):
            break
            
        update_all()
def main():
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        update_all()
    
        player_turn()
        check_player_state()
        if (is_player_winner()):
            isWinner = 0
            victory.play()
            break
    
        ai_turn()
        check_ai_state()
        if (is_ai_winner()):
            isWinner = 1
            lose.play()
            break
    
    ending_scene(isWinner)
        
def ending_scene(status):
    bg = None
    if (status == 0):
        bg = EndScene(600, 400, 'Victory_1.png')
    else:
        bg = EndScene(600, 400, 'lose.png')

    bg_group = pygame.sprite.Group()
    bg_group.add(bg)
    
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bg.kill()
                update_pos(0, 1)
                update_pos(1, 1)

                santa.current_grid = 1
                santa.new_grid = 1
                santa.x = grid_coordinate[0][0]
                santa.y = grid_coordinate[0][1]

                ai.current_grid = 1
                ai.current_grid = 1
                ai.x = grid_coordinate[0][0]
                ai.y = grid_coordinate[0][1]
                
                accept.play()
                return
    
        screen.fill(BLACK)
      
        bg_group.draw(screen)
        bg_group.update()

        clock.tick(FPS)
        pygame.display.flip()

while(1):
    main()




    


