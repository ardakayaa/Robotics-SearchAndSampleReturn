import numpy as np
import time

# Start of our states
def NavState(Rover):
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # If Rover has seen Gold, skips NavState
        if Rover.sample_found is False:
            print('Nav State On!')
            # Check for Rover.mode status
            if Rover.mode == 'forward':
                # Check the extent of navigable terrain
                if len(Rover.nav_angles) >= Rover.stop_forward:
                    # If mode is forward, navigable terrain looks good
                    # and velocity is below max, then throttle
                    if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                        Rover.throttle = Rover.throttle_set
                    else: # Else coast
                        Rover.throttle = 0
                    Rover.brake = 0
                    # Set steering to average angle clipped to the range +/- 15
                    # To stick driving next to wall, added max value of angles
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + (np.max(Rover.nav_angles * 180/np.pi) * 0.4), -15, 15)
                # If there's a lack of navigable terrain pixels then go to 'stop' mode
                elif len(Rover.nav_angles) < Rover.stop_forward:
                        # Set mode to "stop" and hit the brakes!
                        Rover.throttle = 0
                        # Set brake to stored brake value
                        Rover.brake = Rover.brake_set
                        Rover.steer = 0
                        Rover.mode = 'stop'

            # If we're already in "stop" mode then make different decisions
            elif Rover.mode == 'stop':
                # If we're in stop mode but still moving keep braking
                if Rover.vel > 0.2:
                    Rover.throttle = 0
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                # If we're not moving (vel < 0.2) then do something else
                elif Rover.vel <= 0.2:
                    # Now we're stopped and we have vision data to see if there's a path forward
                    if len(Rover.nav_angles) < Rover.go_forward:
                        Rover.throttle = 0
                        # Release the brake to allow turning
                        Rover.brake = 0
                        # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                        Rover.steer = -15 # Could be more clever here about which way to turn
                    # If we're stopped but see sufficient navigable terrain in front then go!
                    if len(Rover.nav_angles) >= Rover.go_forward:
                        # Set throttle back to stored value
                        Rover.throttle = Rover.throttle_set
                        # Release the brake
                        Rover.brake = 0
                        # Set steer to mean angle
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + (np.min(Rover.nav_angles * 180/np.pi)*0.4), -15, 15)
                        Rover.mode = 'forward'

    if Rover.sample_found:
        Collect_Gold_State(Rover)
        print('Gold State On!')

    ##########################################################################
    #State controller
    ##########################################################################
    if Rover.near_sample and not Rover.picking_up:
        Rover.sample_found = True

    return Rover




def Collect_Gold_State(Rover):
    
    # Check for Rover.mode status
    if Rover.mode == 'forward':
        # Check the extent of navigable terrain
        if np.mean(Rover.samples_pos[1]) >= 15 :
            # If mode is forward, navigable terrain looks good
            # and velocity is below max, then throttle
            if Rover.vel < Rover.max_vel / 2:
                # Set throttle value to throttle setting
                Rover.throttle = Rover.throttle_set
            else: # Else coast
                Rover.throttle = 0
            # Set steering to Gold
            Rover.steer = np.clip(np.mean(Rover.samples_pos[0] * 180/np.pi), -15, 15)
    # Stop the Rover to get Gold
    if np.mean(Rover.samples_pos[1]) < 12:
                # Set mode to "stop" and hit the brakes!
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_set
                Rover.steer = 0
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True

    if Rover.picking_up:
        Rover.sample_found = False
        Rover.mode = 'stop'

    return Rover
