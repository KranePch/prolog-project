from pyswip import Prolog

prolog = Prolog()
prolog.consult("snakeNladder.pl")

def get_player_position():
    return list(prolog.query("at(Pos, player_pos)"))[0]['Pos']
    
def get_ai_position():
    return list(prolog.query("at(Pos, ai_pos)"))[0]['Pos']

def get_all_card_types():
    return list(prolog.query("card_type(Card)"))

def is_player_winner():
    player_pos = get_player_position()
    is_win = len(list(prolog.query("goal(dest, " + str(player_pos) + ")")))
    if (is_win == 1):
        return True
    return False

def is_ai_winner():
    ai_pos = get_ai_position()
    is_win = len(list(prolog.query("goal(dest, " + str(ai_pos) + ")")))
    if (is_win == 1):
        return True
    return False

def roll_dice():
    return list(prolog.query("roll_dice(Value)"))[0]['Value']

def roll_card():
    return list(prolog.query("roll_card(Value)"))[0]['Value']
     
def at_ladder(who: int):                                        # use integer 0 for checking if player is on the ladder grid 
    at_ladder = len(list(prolog.query("at_ladder(" + str(who) + ")")))   # use integer 1 (or others) for checking AI
    if (at_ladder == 0):
        return False
    return True

def at_snake(who: int):                                        # use integer 0 for checking if player is on the ladder grid 
    at_snake = len(list(prolog.query("at_snake(" + str(who) + ")")))   # use integer 1 (or others) for checking AI
    if (at_snake == 0):
        return False
    return True

def at_card(who: int):                                        # use integer 0 for checking if player is on the ladder grid 
    at_card = len(list(prolog.query("at_card(" + str(who) + ")")))   # use integer 1 (or others) for checking AI
    if (at_card == 0):
        return False
    return True

def get_random_card():
    return list(prolog.query("get_random_card(Card)"))[0]['Card']

def add_pos(who: int, value: int):      # Return the addition of the current position with value
    return list(prolog.query("add_pos(" + str(who) + ", " + str(value) + ", NewPos)"))[0]['NewPos']

def update_pos(who: int, value: int):   # Update new postion to prolog database 
    if (who == 0):                          # Call this function after using ( add_pos() or use_ts_card() )
        prolog.assertz("at(" + str(value) + ", player_pos)")
        player_pos = get_player_position()
        prolog.retract("at(" + str(player_pos) + ", player_pos)")
    else:
        prolog.assertz("at(" + str(value) + ", ai_pos)")
        ai_pos = get_ai_position()
        prolog.retract("at(" + str(ai_pos) + ", ai_pos)")
    return

def find_nearest_snake(who: int):          # If who = 1 -> use find the nearest snake from AI, otherwise player
    if (who == 1):
        nearest_snake = list(prolog.query("find_nearest_snake(" + str(who) + ", Value)"))
        if (len(nearest_snake) == 0):
            return get_ai_position()
        return nearest_snake[0]['Value']
    else:
        nearest_snake = list(prolog.query("find_nearest_snake(" + str(who) + ", Value)"))
        if (len(nearest_snake) == 0):
            return get_player_position()
        return nearest_snake[0]['Value']

def find_nearest_ladder(who: int):          
    if (who == 1):
        nearest_snake = list(prolog.query("find_nearest_ladder(" + str(who) + ", Value)"))
        if (len(nearest_snake) == 0):
            return get_ai_position()
        return nearest_snake[0]['Value']
    else:
        nearest_snake = list(prolog.query("find_nearest_ladder(" + str(who) + ", Value)"))
        if (len(nearest_snake) == 0):
            return get_player_position()
        return nearest_snake[0]['Value']

def make_decision(card: str):
    return list(prolog.query("make_decision(ai, " + card + ", Decide)"))[0]['Decide']
