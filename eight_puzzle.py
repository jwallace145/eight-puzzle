# import necessary modules
from collections import deque  # data structure of the fringe for bfs
from numpy import random  # random module used to generate permutations of lists for randomizing the puzzle

# board state represented as a list
# 0 represents the empty tile and -1 represents the boundaries of the puzzle
board_state = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1]

# dictionary to represent coordinate positions of the index of the board state array
index_to_coordinates = {
    0: (0, 0),
    1: (0, 1),
    2: (0, 2),
    3: (1, 0),
    4: (1, 1),
    5: (1, 2),
    6: (2, 0),
    7: (2, 1),
    8: (2, 2),
}

# dictionary to represent indices of the board state array of the coordinates of the board
coordinates_to_index = {
    (-1, 0): 9,
    (-1, 1): 9,
    (-1, 2): 9,
    (0, -1): 9,
    (0, 0): 0,
    (0, 1): 1,
    (0, 2): 2,
    (0, 3): 9,
    (1, -1): 9,
    (1, 0): 3,
    (1, 1): 4,
    (1, 2): 5,
    (1, 3): 9,
    (2, -1): 9,
    (2, 0): 6,
    (2, 1): 7,
    (2, 2): 8,
    (2, 3): 9,
    (3, 0): 9,
    (3, 1): 9,
    (3, 2): 9
}


# print board
def print_board(state):
    for i in range(3):
        for j in range(3):
            print('|', end=' ')

            if state[j + 3 * i] == 0:
                print(' ', end=' ')
            else:
                print(state[j + 3 * i], end=' ')

            print('|', end=' ')
        print()


# count the number of inversions
def count_inversions(state):
    tiles = []
    for i in range(len(state)):
        if state[i] != 0 and state[i] != -1:  # exclude 0 and -1 because these are not "tiles"
            tiles.append(state[i])

    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    return inversions


# randomize the board ensuring the new random state is solvable
def randomize_board(state):
    while True:
        tiles = random.permutation(9)

        for i in range(len(state) - 1):
            board_state[i] = tiles[i]

        board_state[9] = -1  # the last element of the board state array represents the boundaries of the board

        if count_inversions(state) % 2 == 0:
            break


# move a tile to the empty tile using array indices
def move_index(state, empty_index, index):
    state[empty_index] = state[index]
    state[index] = 0


# move a tile into a coordinate position
def move_tile(state, tile):
    adjacent = adjacent_to_empty(state, tile)

    if adjacent is not 'not':
        tile_index = state.index(tile)
        row, column = index_to_coordinates.get(tile_index)

        if adjacent is 'above':
            empty_index = coordinates_to_index.get((row + 1, column))
            move_index(state, empty_index, tile_index)
        elif adjacent is 'below':
            empty_index = coordinates_to_index.get((row - 1, column))
            move_index(state, empty_index, tile_index)
        elif adjacent is 'left':
            empty_index = coordinates_to_index.get((row, column + 1))
            move_index(state, empty_index, tile_index)
        elif adjacent is 'right':
            empty_index = coordinates_to_index.get((row, column - 1))
            move_index(state, empty_index, tile_index)
    else:
        print('illegal move')


# check to see if a tile is adjacent to the empty tile
def adjacent_to_empty(state, tile):
    tile_index = state.index(tile)

    if tile_index != 9:
        row, column = index_to_coordinates.get(tile_index)

        if state[coordinates_to_index.get((row + 1, column))] == 0:
            return 'above'
        elif state[coordinates_to_index.get((row - 1, column))] == 0:
            return 'below'
        elif state[coordinates_to_index.get((row, column + 1))] == 0:
            return 'left'
        elif state[coordinates_to_index.get((row, column - 1))] == 0:
            return 'right'
        else:
            return 'not'


# return all the tiles adjacent to the empty tile
def all_adjacent_to_empty(state):
    adjacent = []
    for i in range(len(state)):
        if adjacent_to_empty(state, state[i]) is not 'not' and state[i] != -1:
            adjacent.append(state[i])

    return adjacent


# get the successors of a state
def get_successors(state):
    adjacents = all_adjacent_to_empty(state)

    successors = []
    for tile in adjacents:
        state_copy = state.copy()
        move_tile(state_copy, tile)

        successors.append((state_copy, tile))

    return successors


# bfs search to find the next best move
def bfs(state):
    fringe = deque()
    parents = {}
    visited = set()

    fringe.append(state)
    parents[tuple(state)] = None
    visited.add(tuple(state))
    while len(fringe) != 0:
        s = fringe.popleft()

        if count_inversions(s) == 0:
            print('we found a goal state!!!!')

            tiles = []
            while parents[tuple(s)] is not None:
                tiles.append(parents[tuple(s)][1])
                s = parents[tuple(s)][0]

            return tiles[::-1]

            break

        for successor in get_successors(s):
            ss, tile = successor[0], successor[1]

            if tuple(ss) not in visited:
                fringe.append(ss)
                parents[tuple(ss)] = (tuple(s), tile)
                visited.add(tuple(ss))

    return 1


# main
def main():
    print('EIGHT PUZZLE AI')
    print('---------------')
    print('developed by: Jimmy Wallace')
    #
    # print_board(board_state)
    # print(count_inversions(board_state))
    #
    # randomize_board(board_state)
    #
    # print_board(board_state)
    # print(count_inversions(board_state))
    #
    # print(bfs(board_state))

    print('\ninstructions:')
    print('enter in a tile number to move that tile number into the empty space')
    print('enter in \"ai help\" to have the ai return the tile sequence to solve the puzzle')
    print('enter in \"randomize\" to randomize the puzzle')

    randomize_board(board_state)
    while True:
        print_board(board_state)

        if count_inversions(board_state) == 0:
            print('puzzle solved!')
            break

        user_input = input('input: ')

        try:
            tile = int(user_input)
            move_tile(board_state, tile)
        except ValueError:
            if user_input == 'ai help':
                print('ai help: enter the sequence of tiles below to solve the puzzle')
                print(bfs(board_state))
            elif user_input == 'randomize':
                randomize_board(board_state)
            else:
                print('invalid input')





if __name__ == "__main__":
    main()
