#!/usr/bin/env python3


import subprocess
import sys
import curses
import os

def screen_setup(my_window, width, height, color_mode):
    my_window = curses.newwin(height, width, 0, 0)
    my_window.border()
    return my_window

def draw_character(my_window, x_coord, y_coord, color_index, char_to_display):
    my_window.addch(x_coord, y_coord, char_to_display)
    return my_window

def draw_line(my_window, x1_coord, y1_coord, x2_coord, y2_coord, color_index, char_to_use):
    gradient = None
    if y2_coord == y1_coord:
        gradient = 'horizontal'
    elif x2_coord == x1_coord:
        gradient = 'vertical'
    else:
        gradient = (y2_coord - y1_coord) / (x2_coord - x1_coord)
    
    if gradient == 'horizontal':
        for x in range(x1_coord, x2_coord):
            my_window.addch(y1_coord, x, char_to_use)
    elif gradient == 'vertical':
        for y in range(y1_coord, y2_coord):
            my_window.addch(y, x1_coord, char_to_use)
    else:
        for x in range(x1_coord, x2_coord):
            y = (x * gradient) + y1_coord # y = mx + c
            my_window.addch(round(y), x, char_to_use)
        
    return my_window

def render_text(my_window, x_coord, y_coord, color_index, text):
    my_window.addstr(x_coord, y_coord, text)
    return my_window

def move_cursor(my_window, x_coord, y_coord):
    my_window.move(x_coord, y_coord)
    return my_window

def draw_at_cursor(my_window, char_to_draw = '|', color_index = 1):
    return [6, 2, ord(char_to_draw), color_index]

def clear_screen():
    return [255] # Resolves to 0xFF

def run_command(screen, my_window, command, command_args):
    if command == 1:
        width, height, color_mode = command_args
        return screen_setup(
            my_window = None,
            width = width,
            height = height,
            color_mode = color_mode
        )
    elif command == 2:
        x_coord, y_coord, color_index, char_to_display = command_args
        return draw_character(
            my_window = my_window,
            x_coord = x_coord,
            y_coord = y_coord,
            color_index = color_index,
            char_to_display = chr(char_to_display)
        )
    elif command == 3:
        x1_coord, y1_coord, x2_coord, y2_coord, color_index, char_to_use = command_args
        return draw_line(
            my_window = my_window,
            x1_coord = x1_coord,
            y1_coord = y1_coord,
            x2_coord = x2_coord,
            y2_coord = y2_coord,
            color_index = color_index,
            char_to_use = chr(char_to_use)
        )
    elif command == 4:
        x_coord, y_coord, color_index, *text = command_args
        return render_text(
            my_window = my_window,
            x_coord = x_coord,
            y_coord = y_coord,
            color_index = color_index,
            text = ''.join([chr(c) for c in text])
        )
    elif command == 5:
        x_coord, y_coord = command_args
        return move_cursor(
            my_window = my_window,
            x_coord = x_coord,
            y_coord = y_coord
        )
    elif command == 6:
        char_to_draw, color_index = command_args
        return draw_at_cursor(
            my_window = my_window,
            char_to_draw = char_to_draw,
            color_index = color_index
        )
    elif command == 255:
        return clear_screen()

def paint_screen(screen, binary_data):
    # my_window.clear()
    # breakpoint()

    index = 0
    count = 1
    command = binary_data[index]
    my_window = None
    while(index < len(binary_data)):
        # breakpoint()
        command_byte_length = binary_data[index + 1]

        start = index + 2
        end = start + command_byte_length
        command_args = binary_data[start:end]

        if count <= 10:
            my_window = run_command(screen, my_window, command, command_args) 
        else:
            break   

        index = end
        command = binary_data[index]
        count += 1

        my_window.refresh()
        screen.refresh()
        # breakpoint()

if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: ./terminal_screen.py")
        sys.exit(1)

    file_path = './utils/command.bin'

    try:
        with open(file_path, 'rb') as file:
            # Initialize curses
            screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            screen.keypad(True)

            binary_data_raw = file.read()
            binary_data = [int(b) for b in binary_data_raw]

            paint_screen(screen, binary_data)

            # Clean up curses
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()

            # Pause for a moment to show the message
            screen.getch()

            # Clear the screen before exiting
            screen.clear()
            screen.addstr(0, 0, "Goodbye!\n")
            screen.refresh()

            curses.endwin()

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")