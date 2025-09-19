from game import Moves
import matplotlib.pyplot as plt
import numpy as np
import os


def mac_decides_your_fate(round, level, player_shoots, mac_shoots, player_live_rounds, mac_live_rounds, player_move_history):
    '''
    round (int), player_shoots (int), mac_shoots (int), player_live_rounds (int), mac_live_rounds (int), player_move_history (list) -> Mac's next move (Moves), Mac's prediction of player's next move (Moves)
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
                return Moves.STAND, Moves.DUCK # garentee that next round is a shoot
            else:
                return Moves.DUCK, Moves.SHOOT # garentee that next round is a shoot
            
        # if it's the last bullet left, shoot
        # either way you win
        if mac_shoots == 5:
            return Moves.SHOOT, Moves.SHOOT
        if player_shoots == 5:
            return Moves.SHOOT, Moves.SHOOT

        if player_chance > 0.7:
            return Moves.DUCK, Moves.SHOOT # garentee that next round is a shoot

        # done with absolutes
        # time to look at trends


        


        # if player tends to duck -- remain standing

        # if player tends to remain standing -- shoot

        # if player tends to shoot -- duck until odds are in your favor, then agressive play



        


    pass

def generate_mac_performance(mac_correct_predictions, level, player_shoots, mac_shoots, player_live_rounds, mac_live_rounds, player_move_history):
    '''
    creates a performance graph for mac's predictions, and extrapolation lines for predicting player's next move, with indications of correct predictions during the game on the graph
    
    mac_correct_predictions (json)
    {
        'round': int,
        'level': int,
        'mac_prediction_of_player_action': Moves,
        'mac_action': Moves,
        'player_action': Moves
    }
    '''
    # extract data
    rounds = [entry['round'] for entry in mac_correct_predictions]
    player_predictions = [entry['mac_prediction_of_player_action'] for entry in mac_correct_predictions]
    mac_actions = [entry['mac_action'] for entry in mac_correct_predictions]
    player_actions = [entry['player_action'] for entry in mac_correct_predictions]
    correct_predictions = [entry['mac_prediction_of_player_action'] == entry['player_action'] for entry in mac_correct_predictions]
    correct_rounds = [entry['round'] for entry in mac_correct_predictions if entry['mac_prediction_of_player_action'] == entry['player_action']]
    incorrect_rounds = [entry['round'] for entry in mac_correct_predictions if entry['mac_prediction_of_player_action'] != entry['player_action']]
    correct_predictions_bool = [entry['mac_prediction_of_player_action'] == entry['player_action'] for entry in mac_correct_predictions]
    incorrect_predictions_bool = [entry['mac_prediction_of_player_action'] != entry['player_action'] for entry in mac_correct_predictions]
    correct_predictions_y = [1 if entry else 0 for entry in correct_predictions_bool]

    plt.figure(figsize=(10, 6))
    plt.scatter(rounds, player_actions, c='blue', label='Player Actions', alpha=0.6)
    plt.scatter(rounds, player_predictions, c='orange', label='Mac Predictions', alpha=0.6)
    plt.scatter(correct_rounds, [player_actions[rounds.index(r)] for r in correct_rounds], c='green', label='Correct Predictions', marker='o', s=100)
    plt.scatter(incorrect_rounds, [player_actions[rounds.index(r)] for r in incorrect_rounds], c='red', label='Incorrect Predictions', marker='x', s=100)
    plt.yticks([Moves.DUCK, Moves.STAND, Moves.SHOOT], ['DUCK', 'STAND', 'SHOOT'])

    z = np.polyfit(rounds, player_actions, 1)
    p = np.poly1d(z)
    plt.plot(rounds, p(rounds), "r--", label='Extrapolation Line')

    plt.scatter(rounds, correct_predictions_y, c='green', label='Correct Predictions on Line', marker='o', s=100)

    # labels and legend
    plt.xlabel('Round')
    plt.ylabel('Player Actions')
    plt.title('Mac vs Player Actions')
    plt.legend()
    plt.grid()
    plt.show()

    # save the figure to a file
    plt.savefig(f'data/images/mac_performance.png')
