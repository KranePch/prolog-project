:- dynamic at/2, win/2.
:- discontiguous snake/2.

% ------------------------------ Rule ------------------------------

% Destination
goal(dest, 100).
start_point(dest, 1).

% Actor start position
at(1, player_pos).
at(1, ai_pos).

% Ladder position ---- Actor will increase their progress ----
ladder(6, 14).
ladder(11, 28).
ladder(15, 34).
ladder(17, 74).
ladder(22, 37).
ladder(38, 59).
ladder(49, 67).
ladder(57, 76).
ladder(61, 78).
ladder(73, 86).
ladder(81, 98).

% Snakes position  ---- At this point, actor will decreased their progress ----
snake(26, 10).
snake(39, 5).
snake(44, 18).
snake(54 36).
snake(60, 23).
snake(75, 28).
snake(83, 45).
snake(90, 48).
snake(92, 25).
snake(97, 63).


% Card position ---- Random event that affect to the actor movement ----
card(13).
card(21).
card(30).
card(33).
card(58).
card(62).
card(85).
card(94).

% Cards type in List
game_hold(card_set, [
    move_fw_3, 
    move_bw_2, 
    snake_or_ladder
]).

% Random number between 1-6 for dice && 0-2 for a card
roll_dice(R):-
    random(1,7,X),
    R is X.

roll_card(R):-
    random(0,3,X),
    R is X.
% --------------------------------------- Position System ------------------------------

% Check if Player or AI is at "Ladder" grid or not -> return boolean
at_ladder(X) :-
(
    X == 0
    ->
    at(P, player_pos),
    ladder(P, _);

    at(P, ai_pos),
    ladder(P, _)
).

% Check if Player is at "Snake" grid or not -> return boolean
at_snake(X) :-
(
    X == 0
    ->
    at(P, player_pos),
    snake(P, _);
    
    at(P, ai_pos),
    snake(P, _)
).

% Check if Player or AI is at "Card" grid or not -> return boolean
at_card(X) :-
    (
        X == 0
        ->
        at(P, player_pos),
        card(P);
    
        at(P, ai_pos),
        card(P)
    ).

add_pos(X, V, Pos) :-
    X == 0
    ->
    at(P, player_pos),
    NewPos is P + V,
    cut_to_hundred(NewPos, Pos)
    ;
    at(A, ai_pos),
    NewPos is A + V,
    cut_to_hundred(NewPos, Pos).

cut_to_hundred(V, O) :-     % If position is above 100 -> changed to 100.
    V > 100
    ->
    goal(dest, O);
    cut_to_zero(V, O).

cut_to_zero(V, O) :-        % If position is below 1 -> changed to 1.
    V < 1
    ->
    start_point(dest, O);
    O is V.

% --------------------------------------- Card System ------------------------------

get_random_card(Card) :-
    roll_card(C),
    game_hold(card_set, S),
    nth0(C, S, Card). 

find_nearest_snake(X, V) :-           
    X == 1              % If X is 1, then find nearest snake for AI                         
    ->
    at(A, ai_pos),
    find_nearest_event([26, 39, 44, 54, 60, 75, 83, 90, 92, 97], A, V), !
    ;    
    at(P, player_pos),      
    find_nearest_event([26, 39, 44, 54, 60, 75, 83, 90, 92, 97], P, V).  

find_nearest_ladder(X, V) :-           
    X == 1              % If X is 1, then find nearest ladder for AI                        
    ->
    at(A, ai_pos),
    find_nearest_event([6, 11, 15, 17, 22, 38, 49, 57, 61, 73, 81], A, V), !
    ;    
    at(P, player_pos),      
    find_nearest_event([6, 11, 15, 17, 22, 38, 49, 57, 61, 73, 81], P, V).          

% find a value from list and return the smallest value which more than V
find_nearest_event([H|T], V, R) :-
    H < V
    ->
    find_nearest_event(T, V, R);
    R is H, !.
    
% ---------------------------- AI System ----------------------------

% AI make decision
decide_to(0, player).
decide_to(1, ai).
decide_to(2, discard).

% Call this function after  AI is at Card grid.
make_decision(ai, Card, Decide) :-
    Card == move_fw_3
    ->
    make_decision_on_fw(ai, Decide), !;
    (
        Card == move_bw_2
        ->
        make_decision_on_bw(ai, Decide), !;
        make_decision_on_ls(ai, Decide)
    ).
    
    
% AI thinking process before using card
make_decision_on_fw(ai, Decide) :-
    goal(dest, D),
    at(P, player_pos),
    at(A, ai_pos),
    PN is P + 3,
    AN is A + 3,         % Position value after if activate the card

    (call(snake(PN, PlayerPositionLeftAfterSnake)), 
        PlayerPositionLeftAfterSnake = D - PlayerPositionLeftAfterSnake;
        PlayerPositionLeftAfterSnake = -1
    ),
    
    (call(ladder(AN, AiPositionLeftAfterLadder)), 
    AiPositionLeftAfterLadder = D - AiPositionLeftAfterLadder;
    AiPositionLeftAfterLadder = -1
    ),

    PlayerPositionLeftAfterSnake =\= -1         % If the next 3 grid for player is snake
    ->
    (
        AiPositionLeftAfterLadder =\= -1                % If the next 3 grid for player is snake and for ai is ladder
        ->
        (
            PlayerPositionLeftAfterSnake > AiPositionLeftAfterLadder    
            ->                                      % If heuristic value for player is more than ai heuristic value
                decide_to(Decide, player), !;           % use card on player,       ( Case 2a )
                decide_to(Decide, ai), !                % otherwise use card on AI  ( Case 2b )
        );
        (
            decide_to(Decide, player), !    % ( +3 Player grid ) will be on a snake but ( +3 AI grid ) is normal
        )                                   % ( Case 1 ) 
    );
    check_if_snake(ai, Decide).

check_if_snake(ai, Decide) :-
    at(A, ai_pos),
    AN is A + 3,

    (call(snake(AN, AiGridIsSnake)), 
    AiGridIsSnake = AiGridIsSnake;
    AiGridIsSnake = -1
    ),

    AiGridIsSnake =\= -1
    ->
    decide_to(Decide, discard);         % If the next 3 grid for AI is snake, then discard. ( Case 3 )
    decide_to(Decide, ai).                   % Normal grid -> move AI ( Case 4 )

    
make_decision_on_bw(ai, Decide) :-
    goal(dest, D),
    at(P, player_pos),
    at(A, ai_pos),
    PN is P - 2,
    AN is A - 2,         % Position after activate the card

    (call(snake(PN, PlayerPositionLeftAfterSnake)), 
    PlayerPositionLeftAfterSnake = D - PlayerPositionLeftAfterSnake;
    PlayerPositionLeftAfterSnake = -1
    ),
    
    (call(ladder(AN, AiPositionLeftAfterLadder)), 
    AiPositionLeftAfterLadder = D - AiPositionLeftAfterLadder;
    AiPositionLeftAfterLadder = -1
    ),

    PlayerPositionLeftAfterSnake =\= -1         % If the previous 2 grid for player is snake
    ->
    (
        AiPositionLeftAfterLadder =\= -1                % If the previous 2 grid for player is snake and for ai is ladder
        ->
        (
            PlayerPositionLeftAfterSnake > AiPositionLeftAfterLadder    
            ->                                      % If player snake destination is less than ai ladder destination
                decide_to(Decide, player), !;           % use card on player,       ( Case 2a )
                decide_to(Decide, ai), !                % otherwise use card on AI  ( Case 2b )
        );
        (
            decide_to(Decide, player), !    % ( -2 Player grid ) will be on a snake but ( -2 AI grid ) is normal
        )                                   % ( Case 1 ) 
    );
    check_if_ladder(ai, Decide).

check_if_ladder(ai, Decide) :-
    at(A, ai_pos),
    AN is A - 2,

    (call(snake(AN, AiGridIsSnake)), 
    AiGridIsSnake = AiGridIsSnake;
    AiGridIsSnake = -1
    ),

    AiGridIsSnake =\= -1
    ->
    decide_to(Decide, discard);         % If the next 3 grid for AI is snake, then discard. ( Case 3 )
    decide_to(Decide, player).                   % Normal grid -> move player ( Case 4 )

make_decision_on_ls(ai, Decide) :-
    goal(dest, D),
    at(P, player_pos),
    at(A, ai_pos),

    find_nearest_ladder(1, A_ladder),
    find_nearest_snake(0, P_snake),

    A_left is D - A,
    P_left is D - P,
    
    ladder(A_ladder, L_Dest),
    snake(P_snake, S_Dest),

    P_heuristic_after_snake is D - S_Dest,
    A_heuristic_after_ladder is D - L_Dest,

    P_diff is P_heuristic_after_snake - P_left,
    A_diff is A_left - A_heuristic_after_ladder ,

    P_diff > A_diff
    ->
    decide_to(Decide, player);
    decide_to(Decide, ai).

    
