#!/usr/bin/env python3

import sys

def screen_setup(width = 100, height = 15, color_mode = 0):
    return [1, 3, width, height, color_mode]

def draw_character(x_coord = 1, y_coord = 1, color_index = 1, char_to_display = '+'):
    return [2, 4, x_coord, y_coord, color_index, ord(char_to_display)]

def draw_line(x1_coord = 2, y1_coord = 1, x2_coord = 48, y2_coord = 1, color_index = 1, char_to_use = '+'):
    return [3, 6, x1_coord, y1_coord, x2_coord, y2_coord, color_index, ord(char_to_use)]

def render_text(x_coord = 3, y_coord = 3, color_index = 1, text = "Hello"):
    text_data = [ord(char) for char in text]
    return [4, 3 + len(text_data), x_coord, y_coord, color_index] + text_data

def move_cursor(x_coord = 5, y_coord = 5):
    return [5, 2, x_coord, y_coord]

def sleep(sleep_time = 3):
    return [6, 1, sleep_time]

def text_type(text, y_coord, x_coord):
    result = []
    x = x_coord
    y = y_coord
    for c in text:
        result.append(sleep(1))
        result.append(render_text(y, x, 1, c))
        result.append(move_cursor(y, x + 1))

        x += 1
    breakpoint()

    return result
        

def clear_screen():
    return [255, 0] # Resolves to 0xFF

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
    if len(sys.argv) != 2:
        print("Usage: ./create_binary_file.py <your_name>")
        sys.exit(1)

    # Extract command-line arguments
    name = sys.argv[1]
    text = f"Hello {name},"
    message = 'I hope you are doing great'

    try:
        actions = [
            screen_setup(),
            move_cursor(2, 2),
            draw_character(1, 1, 1, '+'),
            draw_line(2, 1, 48, 1, 1, '-'),
            draw_character(1, 48, 1, '+'),
            draw_line(48, 2, 48, 13, 1, '|'),
            draw_character(13, 1, 1, '+'),
            draw_line(2, 13, 48, 13, 1, '-'),
            draw_character(13, 48, 1, '+'),
            draw_line(1, 2, 1, 13, 1, '|'),
            render_text(3, 3, 1, text),
            move_cursor(3, 3 + len(text)),
            sleep(1),
            move_cursor(5, 3),
            render_text(5, 3, 1, message),
            move_cursor(5, 3 + len(message)),
            sleep(1),
            render_text(11, 3, 1, "Press Enter to exit"),
            sleep(2),
            clear_screen()
        ]

        binary_data = get_binary_data(actions)
    except ValueError:
        print("Error: An error occurred.")
        sys.exit(1)

    # Call the function to create the binary file
    create_binary_file('./commands.bin', binary_data)
