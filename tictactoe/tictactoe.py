"""
Tic Tac Toe Player
"""

import math
import copy
from random import choice
from math import inf as infinity

X = "X"
O = "O"
EMPTY = None

player_turn = X
starter = True


class InvalidActionException(Exception):
    pass


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on the board.
    """
    global player_turn
    global starter
    count_x = 0
    count_o = 0

    if starter is True:
        starter = False
        return player_turn
    else:
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == X:
                    count_x += 1
                elif board[i][j] == O:
                    count_o += 1

        if count_x > count_o:
            player_turn = O
        else:
            player_turn = X

        return player_turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = []
    if not terminal(board):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell is None:
                    action_set.append([i, j])
        return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        b = copy.deepcopy(board)
        i, j = action[0], action[1]
        b[i][j] = player(board)
        return b
    except InvalidActionException:
        if action not in actions(board):
            raise


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_moves = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [X, X, X] in winning_moves:
        return X
    elif [O, O, O] in winning_moves:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if the game is over, False otherwise.
    """
    if (winner(board) is not None) or (not any(EMPTY in sublist for
                                               sublist in board) and winner(board) is None):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            score = 1
        elif winner(board) == O:
            score = -1
        else:
            score = 0

        return score


def shadow_player(board, length, player_selected):
    """
    Return the optimal move for the AI
    """
    if player_selected == X:
        optimal_move = [-1, -1, -infinity]
    elif player_selected == O:
        optimal_move = [-1, -1, +infinity]

    if length == 0 or terminal(board):
        score = utility(board)
        return [-1, -1, score]

    for cell in actions(board):
        x, y = cell[0], cell[1]
        board[x][y] = player_selected
        score = shadow_player(board, length - 1, player(board))
        board[x][y] = EMPTY
        score[0], score[1] = x, y

        if player_selected == X:
            if score[2] > optimal_move[2]:
                optimal_move = score  # Max value
        else:
            if score[2] < optimal_move[2]:
                optimal_move = score  # Min value

    return optimal_move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    length = len(actions(board))
    if length == 0 or terminal(board):
        return None

    if length == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = shadow_player(board, length, player_turn)
        x, y = move[0], move[1]

    return [x, y]
