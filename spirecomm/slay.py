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
    # files = glob.glob('json_fight_data\\*.json')
   
    # for f in files:
    #     os.remove(f)

    coordinator.signal_ready()
    coordinator.register_command_error_callback(agent.handle_error)
    coordinator.register_state_change_callback(agent.get_next_action_in_game)
    coordinator.register_out_of_game_callback(agent.get_next_action_out_of_game)


    for i in range(100):
        result = coordinator.play_one_game(PlayerClass.IRONCLAD)
