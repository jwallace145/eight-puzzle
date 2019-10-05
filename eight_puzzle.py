from collections import deque
from numpy import random

# board state represented as a list
board_state = [3, 1, 2, 4, 0, 5, 6, 7, 8]

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
    8: (2, 2)
}


# print board
def print_board(board_state):
    for i in range(3):
        for j in range(3):
            print('|', end=' ')

            if board_state[j + 3 * i] == 0:
                print(' ', end=' ')
            else:
                print(board_state[j + 3 * i], end=' ')

            print('|', end=' ')
        print()


# count the number of inversions
def count_inversions(board_state):
    count = 0
    tiles = []
    for i in range(len(board_state)):
        if board_state[i] != 0:
            tiles.append(board_state[i])
            count += 1

    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1

    return inversions


# randomize the board ensuring the new random state is solvable
def randomize_board(board_state):
    while True:
        tiles = random.permutation(9)

        for i in range(len(board_state)):
            board_state[i] = tiles[i]

        if count_inversions(board_state) % 2 == 0:
            break


# find the next move to reach the goal state
def find_move(board_state):
    fringe = deque()

    fringe.append(board_state)
    while True:
        state = fringe.popleft()

        if count_inversions(state) == 0:
            print('goal state reached from inside find move')
            print(board_state)
            break

        # find the empty tile coordinates
        for i in range(len(state)):
            if state[i] == 0:
                empty_index = i
                empty_row, empty_column = index_to_coordinates.get(i)
                break

        for i in range(len(state)):

            if state[i] != 0:
                row, column = index_to_coordinates.get(i)

                if empty_row == row - 1 and empty_column == column:
                    copy_state = []
                    copy_states(state, copy_state)
                    move(copy_state, empty_index, i)
                    # print('state: ' + str(state))
                    # print('copy state: ' + str(copy_state))
                    fringe.append(copy_state)
                elif empty_row == row + 1 and empty_column == column:
                    copy_state = []
                    copy_states(state, copy_state)
                    move(copy_state, empty_index, i)
                    # print('state: ' + str(state))
                    # print('copy state: ' + str(copy_state))
                    fringe.append(copy_state)
                elif empty_row == row and empty_column == column - 1:
                    copy_state = []
                    copy_states(state, copy_state)
                    move(copy_state, empty_index, i)
                    # print('state: ' + str(state))
                    # print('copy state: ' + str(copy_state))
                    fringe.append(copy_state)
                elif empty_row == row and empty_column == column + 1:
                    copy_state = []
                    copy_states(state, copy_state)
                    move(copy_state, empty_index, i)
                    # print('state: ' + str(state))
                    # print('copy state: ' + str(copy_state))
                    fringe.append(copy_state)


# move a tile to the empty tile
def move(state, empty_index, index):
    state[empty_index] = state[index]
    state[index] = 0


# copy board state to another state
def copy_states(state, copy_state):
    for i in range(len(state)):
        copy_state.append(state[i])


# main
def main():
    randomize_board(board_state)
    print_board(board_state)
    print(count_inversions(board_state))

    # check for goal state
    if count_inversions(board_state) == 0:
        print('goal state reached')

    find_move(board_state)


if __name__ == "__main__":
    main()
