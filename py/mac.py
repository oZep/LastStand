import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tempfile
from enum import Enum

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
from moves import Moves

def mac_decides_your_fate(round, level, player_shoots, mac_shoots, player_live_rounds, mac_live_rounds, player_move_history):
    '''
    round (int), player_shoots (int), mac_shoots (int), player_live_rounds (int), mac_live_rounds (int), player_move_history (list) -> Mac's next move (Moves), Mac's prediction of player's next move (Moves)
    '''
    # if it is the first round, mac will always opt to shoot
    if round == 1:
        return [Moves.SHOOT, Moves.SHOOT]
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
                return [Moves.STAND, Moves.DUCK] # garentee that next round is a shoot
            else:
                return [Moves.DUCK, Moves.SHOOT] # garentee that next round is a shoot
            
        # if it's the last bullet left, shoot
        # either way you win
        if mac_shoots == 5:
            return [Moves.SHOOT, Moves.SHOOT]
        if player_shoots == 5:
            return [Moves.SHOOT, Moves.SHOOT]

        if player_chance > 0.7:
            return [Moves.DUCK, Moves.SHOOT] # garentee that next round is a shoot

        # done with absolutes
        # time to look at trends
        if duck_count > stand_count:
            return [Moves.STAND, Moves.DUCK] # if player tends to duck -- remain standing
        elif stand_count > duck_count:
            return [Moves.SHOOT, Moves.STAND] # if player tends to remain standing -- shoot
        else:
            return [Moves.DUCK, Moves.SHOOT] # if player tends to shoot -- duck until odds are in your favor, then agressive play

        # if player tends to duck -- remain standing

        # if player tends to remain standing -- shoot

        # if player tends to shoot -- duck until odds are in your favor, then agressive play

def generate_mac_performance(mac_correct_predictions, level, player_shoots, mac_shoots, player_live_rounds, mac_live_rounds, player_move_history):
    '''
    Creates a simple performance graph for mac's predictions when mac_correct_predictions is an int.
    The int represents the number of correct predictions made by Mac.
    '''
    # Use temp directory for writing files in PyInstaller bundle
    temp_dir = tempfile.gettempdir()
    performance_path = os.path.join(temp_dir, 'mac_performance.png')
    if os.path.exists(performance_path):
        os.remove(performance_path)
    if not isinstance(mac_correct_predictions, int):
        raise TypeError("mac_correct_predictions must be an int when using this version.")

    total_rounds = len(player_move_history)
    correct = mac_correct_predictions
    incorrect = total_rounds - correct

    labels = ['Correct', 'Incorrect']
    values = [correct, incorrect]
    colors = ['green', 'red']

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Mac Prediction Accuracy')
    plt.axis('equal')

    # save the figure to a file
    plt.savefig(performance_path, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return performance_path
