#!/usr/bin/env python3

import sys

def screen_setup(width = 200, height = 50, color_mode = 0):
    return [1, 3, width, height, color_mode]

def draw_character(x_coord = 20, y_coord = 20, color_index = 1, char_to_display = '|'):
    return [2, 4, x_coord, y_coord, color_index, ord(char_to_display)]

def draw_line(x1_coord = 5, y1_coord = 5, x2_coord = 195, y2_coord = 45, color_index = 1, char_to_use = '='):
    return [3, 6, x1_coord, y1_coord, x2_coord, y2_coord, color_index, ord(char_to_use)]

def render_text(x_coord = 15, y_coord = 15, color_index = 1, text = 'Hey'):
    text_data = [ord(char) for char in text]
    return [4, 3 + len(text_data), x_coord, y_coord, color_index] + text_data

def move_cursor(x_coord = 25, y_coord = 25):
    return [5, 2, x_coord, y_coord]

def draw_at_cursor(char_to_draw = '|', color_index = 1):
    return [6, 2, ord(char_to_draw), color_index]

def clear_screen():
    return [255] # Resolves to 0xFF

def get_binary_data(commands):
    '''
    Takes in an array of commands each of which is expected to be an array of integers in 
    the following format;
    +--------------+-------------+-------------+-------------+--- ··· ---+----------------+
    | Command Byte | Length Byte | Data Byte 0 | Data Byte 1 |    ···    |  Data Byte n-1 |
    +--------------+-------------+-------------+-------------+--- ··· ---+----------------+

    An example would be;
    [
        [1, 3, 200, 50, 1], 
        [255]
    ]

    Calling this method with the above arguments will return b'\x01\x03\xc82\x01\xff'
    '''

    result = []
    for command in commands:
        result += command

    return bytes(result)

    
def create_binary_file(file_name, data):
    """
    Create a binary file and write the given data to it.

    :param file_name: The name of the binary file to create.
    :param data: The binary data to write to the file.
    """
    try:
        with open(file_name, 'wb') as binary_file:
            binary_file.write(data)
        print(f"Binary file '{file_name}' created successfully.")
    except IOError as e:
        print(f"An error occurred while creating the binary file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./create_binary_file.py <file_name> <text>")
        sys.exit(1)

    # Extract command-line arguments
    file_name = sys.argv[1]
    text = sys.argv[2]

    try:
        actions = [
            screen_setup(),
            draw_character(),
            draw_line(),
            render_text(15, 15, 1, text),
            move_cursor(),
            draw_at_cursor(),
            clear_screen()
        ]

        binary_data = get_binary_data(actions)
    except ValueError:
        print("Error: An error occurred.")
        sys.exit(1)

    # Call the function to create the binary file
    create_binary_file(file_name, binary_data)
