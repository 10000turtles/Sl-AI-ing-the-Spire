import itertools
import datetime
import sys
import json

from spirecomm.communication.coordinator import Coordinator
from spirecomm.ai.newAgent import CoolRadicalAgent
from spirecomm.ai.agent import SimpleAgent
from spirecomm.spire.character import PlayerClass
from spirecomm.spire.game import Game
import os
import glob

if __name__ == "__main__":

    agent = CoolRadicalAgent()
    coordinator = Coordinator()

    # try:
    #     files = glob.glob('json_fight_data/*.json')
    # except:
    #     files = glob.glob('json_fight_data\\*.json')

    # for f in files:
    #     print("removing file: " + str(f))
    #     os.remove(f)

    coordinator.signal_ready()
    coordinator.register_command_error_callback(agent.handle_error)
    coordinator.register_state_change_callback(agent.get_next_action_in_game)
    coordinator.register_out_of_game_callback(
        agent.get_next_action_out_of_game)


    f = open('error.json')
    # f = open('json_fight_data/floor_1_turn_2_action_0.json')

    communication_state = json.load(f)

    agent.get_next_action_in_game(Game.from_json(communication_state.get(
        "game_state"), communication_state.get("available_commands"),communication_state), True)
