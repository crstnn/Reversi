# Cristian Corrado | 29666716

# Please note that the spec asked for turns to be skipped when
# there are no more valid moves for any one given player
# but this is actually a rule of Othello not Reversi.
# The solution followed as the spec asked.
import copy

FIELD_STATE_EMPTY = 0
FIELD_STATE_BLACK = 1
FIELD_STATE_WHITE = 2
PLAYER_1 = 1
PLAYER_2 = 2
BOARD_SIZE = 8
DIRECTIONS = ((0, 1), (1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, -1))
FIELD_COLOUR_NAMES = (None, 'Black', 'White')
FIELD_CHARS = ('-', 'B', 'W')


def get_field_state_for_player(player):
    # Possible to rewrite this function if we ever want to allow the players to swap colours
    if player == PLAYER_1:
        return FIELD_STATE_BLACK
    return FIELD_STATE_WHITE


def get_opposite_player(player):
    if player == PLAYER_1:
        return PLAYER_2
    return PLAYER_1


def get_field_state_for_opposite_player(player):
    return get_field_state_for_player(get_opposite_player(player))


def get_opposite_field_state(field_state):
    if field_state == FIELD_STATE_BLACK:
        return FIELD_STATE_WHITE
    return FIELD_STATE_BLACK


def new_board():
    # The board is list of rows each of which is also a list
    # Note - it is critical to create a new instance for each row
    fresh_board = [[1] * BOARD_SIZE for i in range(BOARD_SIZE)]

    fresh_board[3][3] = FIELD_STATE_WHITE
    fresh_board[4][4] = FIELD_STATE_WHITE
    fresh_board[3][4] = 0
    fresh_board[4][3] = 0

    return fresh_board


def print_board(board):
    underline_on = "\033[4m"
    underline_off = "\033[0m"

    print("%s | A B C D E F G H%s" % (underline_on, underline_off))
    for row_idx, row in enumerate(board):
        print("%d| %s" % (row_idx + 1, " ".join(FIELD_CHARS[f] for f in row)))


def count_fields_of_state(board, field_state):
    sum_for_state = 0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == field_state:
                sum_for_state += 1

    return sum_for_state


def score(board):
    """Returns a 2-tuple of integers (s1, s2) where s1 represents
    the number of stones of Player 1 in the given board configuration
    and s2 represents the number of stones of Player 2.
    """
    return (
        count_fields_of_state(board, get_field_state_for_player(PLAYER_1)),
        count_fields_of_state(board, get_field_state_for_player(PLAYER_2)))


def will_sequence_flip(player, field_states):
    """Field_states: a sequence of field states along a straight line emanating from a proposed new piece position,
    AND that the proposed new piece is not included
    """

    new_piece_field_state = get_field_state_for_player(player)
    other_field_state = get_field_state_for_opposite_player(player)

    first = field_states[0]
    if first != other_field_state:
        return False
    for s in field_states:
        if s == FIELD_STATE_EMPTY:
            return False
        if s == new_piece_field_state:
            return True
    return False


def is_within_board_boundaries(pos):
    def is_dimension_within_board_size(dimension):
        return 0 <= dimension < BOARD_SIZE

    return (is_dimension_within_board_size(pos[0])
            and is_dimension_within_board_size(pos[1]))


def add_vectors(next_pos, dir):
    if len(next_pos) != 2:
        raise Exception("Bad pos")
    if len(dir) != 2:
        raise Exception("Bad dir")
    return (next_pos[0] + dir[0], next_pos[1] + dir[1])


def will_flip_pieces_in_direction(board, player, pos, dir):
    """
    board: a 2D list of field state values
    player: denotes the player that would play the proposed move.
    pos: the position of the proposed piece to be added. This is
    a 2-tuple of (row_index, column_index)
    dir: the direction in which to check for enclosed pieces of the
    opposing player. This is a 2-tuple of (x, y) whose elements
    are either 0 or 1.

    Returns True if in the direction specified the board contains an
    uninterrupted sequence of the opposing players' pieces followed
    by one of the current player's pieces.
    """

    next_pos = add_vectors(pos, dir)
    field_states = []

    while is_within_board_boundaries(next_pos):
        field_states.append(get_field_state(board, next_pos))
        next_pos = add_vectors(next_pos, dir)

    if not field_states:
        return False

    return will_sequence_flip(player, field_states)


def enclosing(board, player, pos, dir):
    return will_flip_pieces_in_direction(board, player, pos, dir)


def get_field_state(board, pos):
    return board[pos[0]][pos[1]]


def valid_moves(board, player):
    """
    Returns a list of valid moves for the particular player chosen.
    It returns a set of tuples (to avoid duplicate 2-tuples)
    """

    adjacent_to_played = set()

    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            rc = (row, column)
            if get_field_state(board, rc) != FIELD_STATE_EMPTY:
                for d in DIRECTIONS:
                    pos = add_vectors((row, column), d)
                    if is_within_board_boundaries(pos) and get_field_state(board, pos) == FIELD_STATE_EMPTY:
                        adjacent_to_played.add(pos)

    result = set()
    for b in adjacent_to_played:
        for d in DIRECTIONS:
            if enclosing(board, player, b, d):
                result.add(b)

    return result


def get_board_state_after_playing_piece(board, player, pos):
    next_board = copy.deepcopy(board)
    opposite_field_state = get_field_state_for_opposite_player(player)
    field_state_for_player = get_field_state_for_player(player)

    for d in DIRECTIONS:
        if enclosing(next_board, player, pos, d):
            next_pos = add_vectors(pos, d)
            while get_field_state(next_board, next_pos) == opposite_field_state:
                next_board[next_pos[0]][next_pos[1]] = field_state_for_player
                next_pos = add_vectors(d, next_pos)
    # play the proposed new piece
    next_board[pos[0]][pos[1]] = field_state_for_player

    return next_board


def next_state(board, player, pos):
    """Method assumes move is valid as caller validates user input
    Output: Returns the next board state as well as the next player state"""

    next_board = get_board_state_after_playing_piece(board, player, pos)
    opposite_player = get_opposite_player(player)

    if len(valid_moves(next_board, opposite_player)) > 0:
        return next_board, opposite_player
    elif len(valid_moves(next_board, player)) > 0:
        return next_board, player
    else:
        return next_board, None


def position(pos_text):
    column_chars = "abcdefgh"
    row_chars = "12345678"
    if len(pos_text) == 2:
        # note - column comes before row in two-character (letter, digit) format
        column_char = pos_text[0]
        row_char = pos_text[1]
        if column_char in column_chars and row_char in row_chars:
            return (row_chars.index(row_char), column_chars.index(column_char))
    return None


def process_player_input(current_board, player):
    while True:
        user_input = input("Player " + str(player) + " please enter your next move co-ordinates: ")
        user_input = user_input.lower()

        # If a player decides to quit the game
        if user_input == "q":
            print("you have decided to quit the game! The following board is the final board state:")
            print_board(current_board)
            return None, None

        user_position = position(user_input)
        if user_position is None:
            print("The move you entered '%s' is not formatted correctly! Please enter a valid move" % user_input)
            # Ask for input again
            continue

        if get_field_state(current_board, user_position) != FIELD_STATE_EMPTY:
            print("Ooops! The move you entered is on an existing board piece! ")
            # Ask for input again
            continue

        if user_position not in valid_moves(current_board, player):
            print("The move you entered '%s' does not flip any pieces!" % user_input)
            # Ask for input again
            continue
        current_board, player = next_state(current_board, player, user_position)

        return current_board, player


def print_end_of_game(current_board):
    # If no more valid moves for any player
    player_one_score, player_two_score = score(current_board)
    print("No more valid moves for either player")
    print("The game ended with Player 1 on", player_one_score, "points and Player 2 on", player_two_score, "points.")
    if player_one_score > player_two_score:
        winner = "Player 1"
    elif player_one_score < player_two_score:
        winner = "Player 2"
    else:
        print("The game ends in a draw")
        return

    print("Therefore the winner is:", winner, "!")
    return


def run_two_players():
    current_board = new_board()
    player = 1
    print("Brief Instructions: You are in 2 Player mode.")
    for p in [PLAYER_1, PLAYER_2]:
        f = get_field_state_for_player(p)
        print("Player %s is %s represented by %s on the board." % (p, FIELD_COLOUR_NAMES[f], FIELD_CHARS[f]))

    while True:
        print_board(current_board)
        current_board, player = process_player_input(current_board, player)

        if current_board is None and player is None:
            # Player chose to quit
            break
        elif player is None and current_board is not None:
            # If no more valid moves for any player
            print_end_of_game(current_board)
            break


def run_single_player():
    current_board = new_board()
    player = 1
    print("Brief Instructions: You are in single Player mode.")
    print("Player 1 is represented by " + FIELD_CHARS[PLAYER_1] + " on the board.")
    print("The Computer (Player 2) is represented by " + FIELD_CHARS[PLAYER_2] + " on the board.")

    while True:

        if player == PLAYER_1:
            print_board(current_board)
            current_board, player = process_player_input(current_board, player)
            if not current_board and not player:
                break
            continue

        if player == PLAYER_2:
            best_move_score = 0
            for valid_m in valid_moves(current_board, player):
                current_move_score = count_fields_of_state(
                    get_board_state_after_playing_piece(current_board, player, valid_m),
                    get_field_state_for_player(player))
                if current_move_score > best_move_score:
                    best_move_score = current_move_score
                    best_move = valid_m
            current_board, player = next_state(current_board, player, best_move)

        # If no more valid moves for current player
        if current_board is None and player is None:
            # Player chose to quit
            break
        elif current_board is not None and player is None:
            # If no more valid moves for any player
            print_board(current_board)
            print_end_of_game(current_board)
            break


# run_single_player()
run_two_players()

#print_board(new_board())
