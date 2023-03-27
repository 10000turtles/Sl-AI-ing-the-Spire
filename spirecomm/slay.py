import itertools
import datetime
import sys
import json

from spirecomm.communication.coordinator import Coordinator
from spirecomm.ai.newAgent import CoolRadicalAgent
from spirecomm.ai.agent import SimpleAgent
from spirecomm.spire.character import PlayerClass
from spirecomm.spire.game import Game

if __name__ == "__main__":
        
    agent = CoolRadicalAgent()
    coordinator = Coordinator()

    coordinator.signal_ready()
    coordinator.register_command_error_callback(agent.handle_error)
    coordinator.register_state_change_callback(agent.get_next_action_in_game)
    coordinator.register_out_of_game_callback(agent.get_next_action_out_of_game)

    # f = open('jawWorm1hp.json')
    # f = open('jaw_worm_strength.json')
    f = open('jawWorm.json')
    communication_state = json.load(f)

    agent.get_next_action_in_game(Game.from_json(communication_state.get("game_state"), communication_state.get("available_commands")))


# if __name__ == "__main__":
        
#     agent = SimpleAgent()
#     coordinator = Coordinator()

#     coordinator.signal_ready()
#     coordinator.register_command_error_callback(agent.handle_error)
#     coordinator.register_state_change_callback(agent.get_next_action_in_game)
#     coordinator.register_out_of_game_callback(agent.get_next_action_out_of_game)

#     result = coordinator.play_one_game(PlayerClass.IRONCLAD)
   


 