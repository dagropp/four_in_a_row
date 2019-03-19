from ..data import game_data as data
import random


class AI:
    """
    This classes creates the Artificial intelligence of the game: automatic choosing of the optimal move if any.
    """

    def __init__(self, game, player):
        """
        Init method for AI objects: Assigns Game object, this player number (1-2) and last found move var.
        :param game: (Game) object with this game logic.
        :param player: (int) in range (1-2) containing player number.
        """
        self.__game = game
        self.__player = player
        self.__last_found_move = None

    def find_legal_move(self, timeout=None):
        """
        This calculates with private method and returns the optimal column to go to, if exists.
        :param timeout: for AI testing, admitted by course staff.
        :return: (int) of column to go to.
        """
        # work on this exception
        if self.__game.get_current_player() != self.__player:
            raise Exception('Wrong Player.')
        # Creates a list of all vacant legal positions (row, col).
        options_list = self._vacant_spots_finder([], data.LAST_IDX_ROW, 0)
        # If legal positions list empty, no moves - raise Exception.
        if not options_list:
            raise Exception('No possible AI moves.')
        # In case of very short timeout, assign random col index to last found move.
        random_idx = AI._rand_idx(len(options_list))
        self.__last_found_move = options_list[random_idx][1]
        # Assign an initial position rating dictionary.
        rating = {'pos': None, 'score': -1}
        # Goes over each location in options_list.
        for row, col in options_list:
            # Assign position list for each direction (this position +- step of 3: to achieve combo of 4).
            pos_list = {
                'horizontal': self._create_pos_list(row, col - data.COMBO_STEP, 0, 1),
                'vertical': self._create_pos_list(row - data.COMBO_STEP, col, 1, 0),
                'diagonal_right': self._create_pos_list(row - data.COMBO_STEP, col - data.COMBO_STEP, 1, 1),
                'diagonal_left': self._create_pos_list(row - data.COMBO_STEP, col + data.COMBO_STEP, 1, -1),
            }
            # Assign next move on row list for each relevant direction (same as pos_list, 1 row above)
            next_move_list = {
                'horizontal': self._create_pos_list(row - 1, col - data.COMBO_STEP, 0, 1),
                'diagonal_right': self._create_pos_list((row - data.COMBO_STEP) - 1, col - data.COMBO_STEP, 1, 1),
                'diagonal_left': self._create_pos_list((row - data.COMBO_STEP) - 1, col + data.COMBO_STEP, 1, -1),
            }
            # Analyse those position list for chances of winning, blocking or just progressing in the game.
            # Subtracting from that the chances of giving the next player a chance to win next round.
            pos_score = self._pos_list_analyser(pos_list.values()) + self._next_move_analyser(next_move_list.values())
            # If current score is better than previous highest score, assigns position and score to rating dictionary.
            if pos_score > rating['score']:
                rating['pos'] = [col]
                rating['score'] = pos_score
                # In case timeout was done before all scores checked, assign this position to last found move.
                self.__last_found_move = col
            # If current score is same like previous highest score, appends position to rating dictionary.
            elif pos_score == rating['score'] and rating['pos'] is not None:
                rating['pos'].append(col)
        # Checks if rating[pos] contains a list of equally rated positions. If so, assign 1 randomly to last found move.
        if rating['pos'] is not None and len(rating['pos']) > 1:
            self.__last_found_move = rating['pos'][AI._rand_idx(len(rating['pos']))]
        # Returns the last found move, now that method is finished it stores the highest rated position (or random).
        return self.__last_found_move

    def get_last_found_move(self):
        """
        This method returns the last found move using find_legal_move() method.
        :return: (int) containing column of last found move.
        """
        if self.__last_found_move is not None:
            return self.__last_found_move

    def _pos_list_analyser(self, pos_list):
        """
        Assign score to each position based on its chances for winning or blocking in this position.
        :param pos_list: (list) of (lists) of players in all possible combinations in this position.
        :return: (int) containing score for this position.
        """
        other_player = (self.__player % 2) + 1
        # Score bank to assign scores for each combination, according to how good it is.
        good_move_level = {1: 1, 2: 5, 3: 10, 4: 1000, 5: 5000}
        scores = 0
        # Goes over each direction in position list.
        for direction in pos_list:
            for i in range(len(direction)):
                # Check all combinations of 4 in direction.
                if i + data.COMBO_STEP < len(direction):
                    temp_combo = direction[i:i + data.COMBINATION_NUM]
                    # If this player has 3 discs and 1 vacant (win), exits method with highest possible score.
                    if temp_combo.count(self.__player) == 3:
                        return good_move_level[5]
                    # If other player has 3 discs and 1 vacant (block win), adds relevant score.
                    if temp_combo.count(other_player) == 3:
                        scores += good_move_level[4]
                    # If this player has 2 discs and 2 vacant, adds relevant score.
                    if temp_combo.count(self.__player) == 2 and temp_combo.count(data.INITIAL_VAL) == 2:
                        scores += good_move_level[3]
                    # If other player has 2 discs and 2 vacant, adds relevant score.
                    if temp_combo.count(other_player) == 2 and temp_combo.count(data.INITIAL_VAL) == 2:
                        scores += good_move_level[2]
                    # If this player has 1 disc and 3 vacant, adds relevant score.
                    if temp_combo.count(self.__player) == 1 and temp_combo.count(data.INITIAL_VAL) == 3:
                        scores += good_move_level[1]
                    # If other player has 1 disc and 3 vacant, adds relevant score.
                    if temp_combo.count(other_player) == 1 and temp_combo.count(data.INITIAL_VAL) == 3:
                        scores += good_move_level[1]
        # Returns scores result
        return scores

    def _next_move_analyser(self, next_move_list):
        """
        Assign negative score to each next move based on its chances for giving other player a chance to win next round.
        :param next_move_list: (list) of (lists) of players in all possible combinations in next position.
        :return: (int) containing score for this next position.
        """
        other_player = (self.__player % 2) + 1
        # Score bank to assign scores for each combination, according to how bad it is.
        bad_move_level = {1: -10, 2: -100, 3: -500}
        scores = 0
        # Goes over each direction in next move list.
        for direction in next_move_list:
            for i in range(len(direction)):
                # Check all combinations of 4 in direction.
                if i + data.COMBO_STEP < len(direction):
                    temp_combo = direction[i:i + data.COMBINATION_NUM]
                    # Other player has 3 discs and 1 vacant (avoid win in next turn), adds relevant score.
                    if temp_combo.count(other_player) == 3:
                        scores += bad_move_level[3]
                    # This player has 3 discs and 1 vacant (avoid block in next turn), adds relevant score.
                    if temp_combo.count(self.__player) == 3:
                        scores += bad_move_level[2]
                    # Other player has 2 discs and 2 vacant (avoid progression in next turn), adds relevant score.
                    if temp_combo.count(other_player) == 2 and temp_combo.count(data.INITIAL_VAL) == 2:
                        scores += bad_move_level[1]
        # Returns scores result
        return scores

    def _create_pos_list(self, row, col, r_change, c_change):
        """
        Private method that creates positions list, of given position +- step of 3, to achieve combo of 4
        :param row: (int) of given position row.
        :param col: (int) of given position col.
        :param r_change: (int) of (-1, 0, 1) to determine change in row indexes (-1: up, 0: stay put, 1: down).
        :param c_change: (int) of (-1, 0, 1) to determine change in column indexes (-1: left, 0: stay put, 1: right).
        :return: (list) of (tuples) of (int) containing relevant positions.
        """
        pos_list = []
        # Creates list for max combo sequence (2 * step(3) + 1)
        for pos in range(data.MAX_COMBO_SEQ):
            this_idx = (row + pos * r_change, col + pos * c_change)
            # Checks if this index is in range of game board list. If so, appends to pos_list the player at position.
            if AI._pos_in_range(*this_idx, data.LAST_IDX_ROW, data.LAST_IDX_COL):
                pos_list.append(self.__game.get_player_at(*this_idx))
        # If the final pos_list is shorter the the combination num (4), deletes this list.
        if len(pos_list) < data.COMBINATION_NUM:
            return []
        return pos_list

    def _vacant_spots_finder(self, vacant_spots, row, col):
        """
        Private recursive method for find_legal_move() method that finds all vacant positions in board (row/col).
        :param vacant_spots: (list) of positions - initially empty.
        :param row: (int) of row to check (initially the last index in row).
        :param col: (int) of col to check (initially 0).
        :return: (list) of (tuples) of (int) containing (row, col) of vacant spots.
        """
        # Recursion base: col is out of board range, return vacant_spots list.
        if col > data.LAST_IDX_COL:
            return vacant_spots
        # Recursion steps:
        else:
            # Row is out of board range, call method again with last row index and col + 1.
            if row < 0:
                return self._vacant_spots_finder(vacant_spots, data.LAST_IDX_ROW, col + 1)
            # Position is same as initial val - position is vacant. Appends position tuple to vacant_spots list
            # and call method again with updated list, last row index and col + 1.
            elif self.__game.get_player_at(row, col) == data.INITIAL_VAL:
                vacant_spots.append((row, col))
                return self._vacant_spots_finder(vacant_spots, data.LAST_IDX_ROW, col + 1)
            # Position not vacant, call method again with row - 1 and same col.
            else:
                return self._vacant_spots_finder(vacant_spots, row - 1, col)

    @staticmethod
    def _rand_idx(list_length):
        """
        Private method that creates random index for a given list range.
        :param list_length: (int) of len(list) function.
        :return: (int) containing random index in list range.
        """
        return random.randint(0, list_length - 1)

    @staticmethod
    def _pos_in_range(row, col, max_row, max_col):
        """

        :param row:
        :param col:
        :param max_row:
        :param max_col:
        :return: (boolean) True if given position in range, False if otherwise.
        """
        if 0 <= row <= max_row and 0 <= col <= max_col:
            return True
        return False
