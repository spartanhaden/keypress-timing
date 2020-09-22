#!/usr/bin/env python3

import getpass
import pprint
import time

import pynput

# Using a dict to keep track of multiple keys independently
start_times = {}
average_times = {}


def update_key_averages(key, key_press_time):
    """
    Updates the average keypress time
    :param key: The key to update
    :param key_press_time: The duration of the last keypress
    """

    global average_times

    # Check if the key has been pressed before
    if key not in average_times:
        # The key has not been pressed before
        average_times[key] = [1, key_press_time]
    else:
        # Update the keypress average
        previous_entries, previous_time = average_times[key]
        new_entries = previous_entries + 1
        new_time = (previous_entries / new_entries) * previous_time
        new_time += key_press_time / new_entries
        average_times[key] = [new_entries, new_time]


def key_press_callback(key):
    """
    Handles keypress
    :param key: The key to handle
    """

    # Capture start time first
    start_time = time.perf_counter()

    global start_times

    # Check if the key is already held down
    if key not in start_times:
        start_times[key] = start_time


def key_release_callback(key):
    """
    Handles key release
    :param key:
    """

    # Capture end time first
    end_time = time.perf_counter()

    # Calculate the time the key was held
    global start_times
    start_time = start_times.pop(key)
    key_press_time = end_time - start_time
    key_press_time *= 1000

    print(key, 'pressed for', '{:.1f}'.format(key_press_time), 'ms')
    update_key_averages(key, key_press_time)


if __name__ == '__main__':
    # Create the keyboard listener
    listener = pynput.keyboard.Listener(on_press=key_press_callback, on_release=key_release_callback)
    listener.start()

    # Keep running until user exits 'ctrl + c'
    try:
        while True:
            # Hide the user input
            getpass.getpass('')
    except KeyboardInterrupt:
        print()
        print('Number of key presses and average key press time in milliseconds')
        print()
        # Cleanup the average times and output
        for key, value in average_times.items():
            average_times[key] = [value[0], round(value[1], 1)]
        pprint.pprint(average_times)
