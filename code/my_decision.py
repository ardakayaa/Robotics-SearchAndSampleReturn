import numpy as np
#from drive_rover import Rover
from my_states import NavState
from my_states import Collect_Gold_State

# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):
    print (np.mean(Rover.samples_pos[1]))
    if Rover.nav_angles is not None:
        if Rover.near_sample and not Rover.picking_up:
            Collect_Gold_State(Rover)
            #NavState(Rover)
            print ('GoldStateON')
        else:
            NavState(Rover)
            print ('NavStateON')


    return Rover
