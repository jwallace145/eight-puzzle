# import necessary modules
from priority_queue import PriorityQueue  # data structure of the fringe for A* search
from collections import deque  # data structure of the fringe for bfs
from numpy import random  # random module used to generate permutations of lists for randomizing the puzzle

# board state represented as a list
# 0 represents the empty tile and -1 represents the boundaries of the puzzle
board_state = [0, 1, 2, 3, 4, 5, 6, 7, 8, -1]

# dictionary to represent coordinate positions as the indices of the board state array
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
    9: (-1, -1)
}

# dictionary to represent indices of the board state array as coordinates of the eight puzzle
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
    for i in range(len(state)):  # generate a list with only the order of the tiles excluding the empty tile
        if state[i] != 0 and state[i] != -1:  # exclude 0 and -1 because these are not "tiles"
            tiles.append(state[i])

    # count the number of inversions, one inversion is one instance of a larger number preceding order read left to
    # right, top to bottom
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    return inversions  # an even number of inversions implies that the board state is solvable


# randomize the board ensuring the new random state is solvable
def randomize_board(state):
    # continue generating random board states until the number of inversions in the given board state is even which
    # implies a solvable permutation of the board state
    while True:
        tiles = random.permutation(9)  # generate a random permutation of the numbers 0-8

        # place the random permutation of the numbers 0-8 in the first 8 positions of the board state array
        for i in range(len(state) - 1):
            board_state[i] = tiles[i]

        board_state[9] = -1  # the last element of the board state array represents the boundaries of the board

        if count_inversions(state) % 2 == 0:
            break


# move a tile to the empty tile using board state array indices
def move_index(state, empty_index, index):
    state[empty_index] = state[index]
    state[index] = 0


# move a tile into a coordinate position
def move_tile(state, tile):
    adjacent = adjacent_to_empty(state, tile)  # determine the adjacency of the given tile to the empty tile

    if adjacent is not 'not':  # if tile is not adjacent to the empty tile, the tile may not move
        tile_index = state.index(tile)
        row, column = index_to_coordinates.get(tile_index)

        # determine which direction the given tile is adjacent to the empty tile and consequently move the tile to the
        # empty tile
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


# move tiles in a sequence
def move_tile_sequence(state, sequence):
    for i in range(len(sequence)):
        move_tile(state, sequence[i])


# check to see if a tile is adjacent to the empty tile
def adjacent_to_empty(state, tile):
    tile_index = state.index(tile)  # determine the board state array index of the given tile

    if tile_index != 9:  # if the give location is not a boundary
        row, column = index_to_coordinates.get(tile_index)  # assign the row and column values of the tile

        # determine which direction the given tile is adjacent to the empty tile
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
    # loop through all the tiles and determine if a tile is adjacent to the empty tile and if so add the tile to the
    # list adjacent to be returned
    adjacent = []
    for i in range(len(state)):
        # if the tile is adjacent and not a boundary tile
        if adjacent_to_empty(state, state[i]) is not 'not' and state[i] != -1:
            adjacent.append(state[i])

    return adjacent


# get the successors of a state
def get_successors(state):
    adjacent = all_adjacent_to_empty(state)  # get all adjacent tiles to the empty tile

    # loop through the adjacent tiles and move the tile to the empty tile to represent a successor to the given state
    successors = []
    for tile in adjacent:
        state_copy = state.copy()
        move_tile(state_copy, tile)

        successors.append((state_copy, tile))

    return successors  # return a list of the successor states


# bfs search to find the next best move
def bfs(initial_state):
    nodes_expanded = 0

    fringe = deque()  # data structure used to implement bfs
    parents = {}  # parent dictionary containing the parent of each state and the move taken to get to that state
    visited = set()  # visited set to store the visited states to aid in avoiding unnecessary cylces

    fringe.append(initial_state)  # append the starting state
    parents[tuple(initial_state)] = None  # the starting state has no parents
    visited.add(tuple(initial_state))  # add the starting state to the visited set
    while len(fringe) != 0:
        state = fringe.popleft()  # pop a state from the fringe

        if count_inversions(state) == 0:  # if a goal state is achieved
            print('we found a goal state!!!')

            # backtrack through the parents array to determine the sequence of moves taken to arrive at the goal state
            # and then return the reverse of that sequence
            tiles = []
            while parents[tuple(state)] is not None:
                tiles.append(parents[tuple(state)][1])
                state = parents[tuple(state)][0]

            print('nodes expanded: ' + str(nodes_expanded))
            return tiles[::-1]

        # expand the nodes of every successor
        for successor in get_successors(state):
            successor_state, tile = successor[0], successor[1]

            nodes_expanded += 1

            # if the successor state has not been visited, add it to the fringe, parents dictionary, and visited set
            if tuple(successor_state) not in visited:
                fringe.append(successor_state)
                parents[tuple(successor_state)] = (tuple(state), tile)
                visited.add(tuple(successor_state))


# heuristic function to be used with A* search
def heuristic(state):
    s = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != -9:
            s += abs(state[i] - i)

    return s


# get depth of the current node
def get_depth(state, parents):
    depth = 0
    while parents[tuple(state)] is not None:
        state = parents[tuple(state)][0]
        depth += 1

    return depth

# A* search
def a_star(initial_state):
    nodes_expanded = 0

    li = []
    fringe = PriorityQueue()  # data structure used to implement a* search
    parents = {}  # parent dictionary containing the parent of each state and the move taken to get to that state
    visited = set()  # visited set to store the visited states to aid in avoiding unnecessary cycles

    # append the starting state as a tuple with the cost of the move as the first element
    fringe.push((0, initial_state))
    parents[tuple(initial_state)] = None  # the starting state has no parents
    visited.add(tuple(initial_state))  # add the starting state to the visited set
    while not fringe.is_empty():
        cost, state = fringe.pop()  # pop a cost and state from the fringe

        if count_inversions(state) == 0:  # if a goal state is achieved
            print('we found a goal state!!!')

            # backtrack through the parents array to determine the sequence of moves taken to arrive at the goal state
            # and then return the reverse of that sequence
            tiles = []
            while parents[tuple(state)] is not None:
                tiles.append(parents[tuple(state)][1])
                state = parents[tuple(state)][0]

            print('nodes expanded: ' + str(nodes_expanded))
            return tiles[::-1]

        # expand the nodes of every successor
        for successor in get_successors(state):
            successor_state, tile = successor[0], successor[1]

            nodes_expanded += 1

            # if the successor state has not been visited, add it to the fringe, parents dictionary, and visited set
            if tuple(successor_state) not in visited:
                parents[tuple(successor_state)] = (tuple(state), tile)
                visited.add(tuple(successor_state))

                # the priority of the state = depth of the state + heuristic value of the state
                # this priority queue is implemented as a minimum priority queue so low value heuristics are desirable
                fringe.push((get_depth(successor_state, parents) + heuristic(successor_state), successor_state))


# main
def main():
    # print introduction and instructions
    print('EIGHT PUZZLE AI')
    print('---------------')
    print('developed by: Jimmy Wallace')
    print('\ninstructions:')
    print('enter in a tile number to move that tile number into the empty space')
    print('enter in \"sequence\" to enter in a sequence of tile moves')
    print('enter in \"ai help\" to have the ai return the tile sequence to solve the puzzle')
    print('enter in \"randomize\" to randomize the puzzle\n')

    # initially randomize the give board state
    randomize_board(board_state)

    while True:
        print_board(board_state)  # print the board state

        # if the number of inversions is equal to 0, a goal state has been reached
        if count_inversions(board_state) == 0:
            print('puzzle solved!')
            break

        # get user input
        user_input = input('input: ')

        try:  # try to parse the input as a string
            tile = int(user_input)
            move_tile(board_state, tile)
        except ValueError:  # catch the error if the user input cannot be parsed as a string
            if user_input == 'ai help':  # if user wants ai help

                search_alg = input('search algorithm \"a_star\" or \"bfs\": ')
                if search_alg == 'a_star':
                    print('ai help: enter the sequence of tiles below to solve the puzzle')
                    print(a_star(board_state))
                elif search_alg == 'bfs':
                    print('ai help: enter the sequence of tiles below to solve the puzzle')
                    print(bfs(board_state))
            elif user_input == 'randomize':  # if user wants to randomize the board
                randomize_board(board_state)
            elif user_input == 'sequence':  # if the user wants to enter a sequence of moves at once
                tiles = []
                n = int(input('enter in the number of tiles in the sequence: '))

                for i in range(n):
                    tile = int(input())
                    tiles.append(tile)

                move_tile_sequence(board_state, tiles)
            else:  # else invalid string input
                print('invalid input')


# main function
if __name__ == "__main__":
    main()
