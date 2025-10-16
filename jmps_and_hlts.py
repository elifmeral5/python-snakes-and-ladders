"""
File: jmps_and_hlts.py
Author: Elif Meral
Date: 03/29/24
Section: 24
E-mail: elifm1@umbc.edu
Description: User inputs map length and seed to play a version of
            snakes and ladders.
"""
# FUNCTIONS TO MAKE MAP
import random

# Constant Variables
QUIT_STRING = 'quit'
END_GAME = 'hlt'
NO_CHANGE = 'nop'
ADD = 'add'
SUB = 'sub'
MUL = 'mul'
JUMP = 'jmp'
GRID_WIDTH = 8
GRID_HEIGHT = 3
DICE_SIDES = 6


def generate_random_map(length, the_seed=0):
    """
        :param length - the length of the map
        :param the_seed - the seed of the map
        :return: a randomly generated map based on a specific seed, and length.
    """
    if the_seed:
        random.seed(the_seed)
    map_list = []
    for _ in range(length - 2):
        random_points = random.randint(1, 100)
        random_position = random.randint(0, length - 1)
        map_list.append(random.choices(['nop', f'add {random_points}', f'sub {random_points}',
                                        f'mul {random_points}', f'jmp {random_position}', 'hlt'],
                                       weights=[5, 2, 2, 2, 3, 1], k=1)[0])

    return ['nop'] + map_list + ['hlt']


def make_grid(table_size):
    """
    :param table_size: this needs to be the length of the map
    :return: returns a display grid that you can then modify with fill_grid_square (it's a 2d-grid of characters)
    """
    floating_square_root = table_size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_height = int_square_root
    if int_square_root * (int_square_root - 1) >= table_size:
        table_height -= 1

    the_display_grid = [[' ' if j % GRID_WIDTH else '*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        if i % GRID_HEIGHT else ['*' for j in range(GRID_WIDTH * int_square_root + 1)]
                        for i in range(table_height * GRID_HEIGHT + 1)]
    return the_display_grid


def fill_grid_square(display_grid, size, index, message):
    """
    :param display_grid:  the grid that was made from make_grid
    :param size:  this needs to be the length of the total map, otherwise you may not be able to place things correctly.
    :param index: the index of the position where you want to display the message
    :param message: the message to display in the square at position index, separated by line returns.
    """
    floating_square_root = size ** (1 / 2)
    int_square_root = int(floating_square_root) + (1 if floating_square_root % 1 else 0)
    table_row = index // int_square_root
    table_col = index % int_square_root

    if table_row % 2 == 0:
        column_start = GRID_WIDTH * table_col
    else:
        column_start = GRID_WIDTH * (int_square_root - table_col - 1)

    for r, message_line in enumerate(message.split('\n')):
        for k, c in enumerate(message_line):
            display_grid[GRID_HEIGHT * table_row + 2 + r][column_start + 1 + k] = c


def play_game(game_map):
    """
    :param game_map: gets the information from previous functions
    :return: displays grid with random_map
    """
    length_seed = game_map.split()
    map_length = int(length_seed[0])
    map_seed = int(length_seed[1])
    # makes a 2d list of the squares
    random_map = generate_random_map(map_length, map_seed)
    # 2d list of the spaces and borders needed
    the_grid = make_grid(map_length)
    # fills the grid
    the_index = 0
    while the_index < len(random_map):
        for x in random_map:
            fill_grid_square(the_grid, map_length, the_index, random_map[the_index])
            the_index += 1
        # prints out the grid and makes a "game board"
    for g in range(len(the_grid)):
        print(''.join(the_grid[g]))

    return random_map


def change_score(instruction, score, new_point):
    """
    :param instruction: gets the instruction for the map
    :param score: gets the most recent score
    :param new_point: gets the needed point to change score
    :return: the new score
    """
    if instruction == ADD:
        score += new_point
    elif instruction == SUB:
        score -= new_point
    elif instruction == MUL:
        score *= new_point

    return score


def jumping(position, score, instruction, dice):
    """
    :param position: gets the position on the grid
    :param score: gets last calculated score
    :param instruction: gets instruction from the move that just ended
    :param dice: gets the number from the dice
    :return: the instruction
    """
    print('Pos:', position, 'Score:', score, 'Instruction:', instruction, 'Rolled:', dice)
    jump_list = instruction.split()
    jump_amount = int(jump_list[1])
    position = jump_amount
    instruction = random_map[position]
    return instruction


def roll_dice():
    """
        DO NOT CHANGE THIS FUNCTION
        Call this function once per turn.

        :return: returns the dice roll
    """
    return random.randint(1, DICE_SIDES)


if __name__ == '__main__':
    # Asking user for board input
    map_length_seed = input('Board Size and Seed: ')
    # making the board until said otherwise
    while map_length_seed != QUIT_STRING:
        # play_game(map_length_seed)
        random_map = play_game(map_length_seed)
        map_length = int(map_length_seed.split()[0])
        # The first play
        score = 0
        position = 0
        dice = roll_dice()
        position += dice
        instruction = random_map[position]
        print('Pos:', position, 'Score:', score, 'Instruction:', instruction, 'Rolled:', dice)

        while instruction != END_GAME:
            # Looped Rounds
            dice = roll_dice()
            position += dice
            if position >= map_length:
                position %= map_length

            instruction = random_map[position]

            the_instruction = instruction.split()
            final_instruction = the_instruction[0]

            # Board Instructions
            if final_instruction == NO_CHANGE:
                pass
            elif final_instruction == ADD or final_instruction == SUB or final_instruction == MUL:
                if len(the_instruction) >= 2:
                    number = int(the_instruction[1])
                    # print(number)
                    score = change_score(final_instruction, score, number)
                else:
                    pass
            elif final_instruction == JUMP:
                jumping(position, score, instruction, dice)
                if final_instruction == NO_CHANGE:
                    pass
                else:
                    if len(the_instruction) >= 2:
                        number = int(the_instruction[1])
                        score = change_score(final_instruction, score, number)
                    else:
                        pass
                dice = dice
            print('Pos:', position, 'Score:', score, 'Instruction:', instruction, 'Rolled:', dice)
        if final_instruction == 'hlt':
            print('Final Pos:', position, 'Final Score:', score, ',', 'Instruction hlt')
        # NEW GAME
        map_length_seed = input('Board Size and Seed: ')
