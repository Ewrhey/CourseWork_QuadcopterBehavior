from djitellopy import Tello # Import the Tello class from the djitellopy library

def main():
    tello = Tello()  # Create a Tello object to control the drone
    tello.connect()  # Establish a connection with the drone
    # Initialize variables
    start_pad_ID, default_height, default_battery_lvl, default_dist, cnt_iter = 1, 40, 30, 20, 0
    finish_pad_ID = int(input("Input finish pad ID:"))  # Enter the finish pad ID
    battery_lvl = tello.get_battery()  # Get the drone's battery level
    tello.enable_mission_pads()  # Enable the use of mission pads
    tello.set_mission_pad_detection_direction(2)  # Set the pad detection direction

    # Check battery level before takeoff
    if battery_lvl > default_battery_lvl:
        print("\033[0;32mBattery level: \033[0;37m", battery_lvl, "%", sep='')
        tello.takeoff()  # Take off the drone
        while True:  # Main drone control loop
            if move_forward(tello=tello, dist=default_dist) == 0:  # Move forward and check for errors
                break
            if tello.get_mission_pad_id() == finish_pad_ID:  # Check if the finish pad is reached
                finish(tello = tello, finish_pad_ID= finish_pad_ID)  # Call the finish function
                print("\033[0;32m finish complete\033[0;0m ")
                break
            if tello.get_mission_pad_id() == -1:  # Check for pad detection error
                print("\033[0;31mError:\033[0m pad not found in main")
                break
            if cnt_iter >= 7:  # Check if the number of movements exceeds the limit
                print("\033[0;31mError:\033[0m too much move")
                break
            cnt_iter += 1  # Increment iteration counter
        tello.land()  # Land the drone
    else:
        # Display an error message if the battery level is insufficient
        print("\033[0;31mError: battery level is insufficient\033[0;37m ", battery_lvl, "%", sep='')

def alignment(tello):  # Function to align the drone relative to the pad
    dy = tello.get_mission_pad_distance_y()  # Get the distance to the pad along the Y-axis
    # Align the drone left or right depending on its position
    if dy < -20 and tello.get_mission_pad_id() > -1:
        tello.move_left(abs(dy))
    elif dy > 20 and tello.get_mission_pad_id() > -1:
        tello.move_right(dy)

    if tello.get_mission_pad_id() == -1:  # If the pad is not found, display an error message
        print("\033[0;31mError\033[0;37m: pad not found in alignment")
        return 0


def move_forward(tello, dist):  # Function to move the drone forward
    if tello.get_mission_pad_id() == -1:
        print("\033[0;31mError\033[0;37m: pad not found in move")
        return 0
    tello.move_forward(dist)  # Move the drone forward
    if alignment(tello = tello) == 0:  # Call the alignment function and check for errors
        return 0
    return 1


def finish(tello, finish_pad_ID):  # Function to complete the mission
    # Get the distance to the finish pad
    dz = tello.get_mission_pad_distance_z()
    # Move the drone to the finish pad while decreasing altitude
    for i in range(dz // 20 - 1):
        tello.go_xyz_speed_mid(0, 0, dz - 20, 20, finish_pad_ID)
        dz -= 20


if __name__ == "__main__":
    main()

