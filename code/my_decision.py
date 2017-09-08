import numpy as np
#from drive_rover import Rover
from my_states import NavState
from my_states import Collect_Gold_Sate

# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):

    if Rover.nav_angles is not None:
        if Rover.near_sample and not Rover.picking_up:
            Collect_Gold_Sate(Rover)
            print ('GoldStateON')
        else:
            NavState(Rover)
            print ('NavStateON')


    return Rover
