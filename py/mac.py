from game import Moves
import matplotlib.pyplot as plt
import numpy as np
import os


def mac_decides_your_fate(round, level, player_shoots, mac_shoots, player_live_rounds, mac_live_rounds, player_move_history):
    '''
    round (int), player_shoots (int), mac_shoots (int), player_live_rounds (int), mac_live_rounds (int), player_move_history (list)
    '''
    # if it is the first round, mac will always opt to shoot
    if round == 1:
        return Moves.STAND
    else:
        # main logic
        # first calculation: How many bullets does player have in chamber
        player_chance = (level - player_live_rounds) / (6 - player_shoots)
        mac_chance = (level - mac_live_rounds) / (6 - mac_shoots)
        duck_count = player_move_history.count(Moves.DUCK)
        stand_count = player_move_history.count(Moves.STAND)

        # absolutes
        if mac_chance == 1:
            if player_chance <= 0.6:
                return Moves.STAND # garentee that next round is a shoot
            else:
                return Moves.DUCK # garentee that next round is a shoot
            
        # if it's the last bullet left, shoot
        # either way you win
        if mac_shoots == 5:
            return Moves.SHOOT
        
        if player_chance > 0.7:
            return Moves.DUCK # garentee that next round is a shoot


        if mac_chance > 0.7:
            # look at player history, if they tend to duck, stand, else shoot
            if duck_count > stand_count:
                return Moves.STAND
            else:
                return Moves.SHOOT

        if player_chance > 0.7: # this means out of 6 bullets, player has more than 4 bullets in chamber
            return Moves.DUCK
        
        if player_chance < 0.5:
            # look at player history
            pass

        if player_chance < 0.3:


            if duck_count > stand_count:
                return Moves.STAND
            else:
                return Moves.DUCK
        


        # if player tends to duck -- remain standing

        # if player tends to remain standing -- shoot

        # if player tends to shoot -- duck until odds are in your favor, then agressive play



        


    pass