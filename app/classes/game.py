from ..data import game_data as data
import random


class Game:
    """
    This classes creates the Game board and the logic of turns, moving players, winning or declare a tie.
    """

    def __init__(self):
        """
        Init method for Game objects: Assigns board list, turn counter, first player and last move.
        """
        self.__board = Game._create_board_list(data.BOARD_ROWS, data.BOARD_COLS)
        self.__turn_counter = 1
        # Randomly choosing first player
        self.__first_player = random.randint(1, 2)
        self.__last_move = None

    def make_move(self, column):
        """
        This method checks if column has vacant rows, and if so moves player to lowest row available.
        :param column: (int) of column to move to.
        :return: raise exception if not int in list range, or if no vacant row.
        """
        # Checks if column input is int in list range. If not, raise Exception.
        if not Game._int_in_range(column, 0, data.LAST_IDX_COL):
            raise Exception('Position not existent.')
        # Calls vacant_row() method to check if column has vacant row.
        vacant_row = self._vacancy_checker(data.LAST_IDX_ROW, column)
        # If no vacant rows, raise Exception.
        if vacant_row is None:
            raise Exception('Illegal move.')
        # There is vacant row: Assign player to lowest vacant row, and assigns last_move var these indexes.
        else:
            self.__board[vacant_row][column] = self.get_current_player()
            self.__last_move = (vacant_row, column)

    def get_winner(self):
        """
        Checks if there is a winner, and if so returns the relevant player.
        :return: player 1 or 2 if there is a winner / 0 if tie and board is full / None if not finished game.
        """
        # Calls _combination_checker() method to check if any combinations were made. If so return player number.
        if self.__last_move is None:
            return None
        elif self._combination_checker(*self.__last_move):
            return self.get_current_player()
        # Check is turns number match all available cells. If so, and no combinations were made, return 0.
        elif self.__turn_counter == data.BOARD_ROWS * data.BOARD_COLS:
            return 0
        # No combinations were made, board not full, game not over - return None.
        else:
            return None

    def get_player_at(self, row, col):
        """
        Returns player number in certain location.
        :param row: (int) of row to search.
        :param col: (int) of col to search
        :return: (int) of player num / None at this index. If row/col out of list range, raise Exception.
        """
        # Checks if row/col not in list range. If so, raise Exception.
        if not Game._int_in_range(row, 0, data.LAST_IDX_ROW) or not Game._int_in_range(col, 0, data.LAST_IDX_COL):
            raise Exception('Illegal location.')
        return self.__board[row][col]

    def get_current_player(self):
        """
        Return this turn player number.
        :return: (int) of current player number.
        """
        return ((self.__turn_counter + self.__first_player) % 2) + 1

    def add_turn(self):
        self.__turn_counter += 1

    def get_turn(self):
        return self.__turn_counter

    def get_board(self):
        return self.__board

    def _combination_checker(self, row, col):
        """
        Private method for get_winner(). Checks if any combinations were made - horizontal, vertical or diagonal.
        :param row: (int) of last move row.
        :param col: (int) of last move col.
        :return: (boolean) True if any combinations were found. False if not.
        """
        # Assign dictionary of possible directions, and its relevant params for _combination_checker_helper() method.
        possibilities = {
            'horizontal': ([], row, 0, 0, 1),
            'vertical': ([], 0, col, 1, 0),
            'diagonal_right': ([], *Game._get_initial_right_pos(row, col), 1, 1),
            'diagonal_left': ([], *Game._get_initial_left_pos(row, col), 1, -1)
        }
        for params in possibilities.values():
            if self._combination_checker_helper(*params):
                return True

    def _combination_checker_helper(self, combo_list, row, col, r_change, c_change):
        """
        Private recursive method for _combination_checker(). Checks if any combinations were made in given direction.
        :param combo_list: (list) containing the index positions of combinations found.
        :param row: (int) of row to start at.
        :param col: (int) of col to start at.
        :param r_change: (int) in range 0-1, of what change to do each recursion in row.
        :param c_change: (int) in range 0-1, of what change to do each recursion in column.
        :return: (boolean) True if found combination, False if not.
        """
        # Recursion base: If row/col out of range return None.
        if row > data.LAST_IDX_ROW or col > data.LAST_IDX_COL or col < 0:
            return
        else:
            # If index is the current player, appends to combo list.
            if self.get_player_at(row, col) == self.get_current_player():
                combo_list.append((row, col))
                # If combo list is the size of the combination number, return True.
                if len(combo_list) == data.COMBINATION_NUM:
                    return self._check_win(combo_list)
            # If index not current player, reset combo list.
            else:
                combo_list = []
            # Recursion step: Calls function again, and adds row and col its change params (0/1).
            return self._combination_checker_helper(combo_list, row + r_change, col + c_change, r_change, c_change)

    def _check_win(self, combo_list):
        for row, col in combo_list:
            self.__board[row][col] = data.WIN_VAL
        return True

    def _vacancy_checker(self, row, col):
        """
        Private recursive method that checks which is the lowest vacant row in selected column.
        :param row: (int) of row to check - starts from bottom to top (-1 in each recursion)
        :param col: (int) of selected col to check - doesn't change with recursive calls.
        :return: (int) of number of lowest vacant row in column. if no vacant row in col, returns (None).
        """
        # Recursion base 1: if no rows were found vacant for col, returns None.
        if row < 0:
            return None
        # Recursion base 2: found vacant row for col, returns its index.
        elif self.get_player_at(row, col) == data.INITIAL_VAL:
            return row
        # Recursion step: this row wasn't vacant. calls method again with (row - 1).
        else:
            return self._vacancy_checker(row - 1, col)

    @staticmethod
    def _create_board_list(rows, cols):
        """
        Private method creates board list with no cloning.
        :param rows: (int) number of board rows.
        :param cols: (int) number of board columns.
        :return: (list) of (lists) of (int) representing board.
        """
        board_list = []
        # Goes over all the rows and adds to each row a list of columns with initial value (0).
        for row in range(rows):
            board_list += [[data.INITIAL_VAL] * cols]
        return board_list

    @staticmethod
    def _get_initial_right_pos(row, col):
        """
        Private method that returns the base location for diagonal-right search, in rectangular 2-d list.
        The method checks the location of last move, and returns it highest starting point in it right-diagonal line.
        :param row: (int) of row to start at.
        :param col: (int) of column to start at.
        :return: (tuple) of (int) containing base row, column.
        """
        # If row smaller than col, return (row=0, col=col-row).
        if row < col:
            return 0, col - row
        # Else, return (row=row-col, col=0).
        else:
            return row - col, 0

    @staticmethod
    def _get_initial_left_pos(row, col):
        """
        Private method that returns the base location for diagonal-left search, in rectangular 2-d list.
        The method checks the location of last move, and returns it highest starting point in it left-diagonal line.
        :param row: (int) of row to start at.
        :param col: (int) of column to start at.
        :return: (tuple) of (int) containing base row, column.
        """
        # If row+col smaller than last index in col list, return (row=0, col=row+col).
        if row + col <= data.LAST_IDX_COL:
            return 0, row + col
        # Else, return (row=row+col-col last index, col=col last index).
        else:
            return (row + col) - data.LAST_IDX_COL, data.LAST_IDX_COL

    @staticmethod
    def _int_in_range(num, min_num, max_num):
        """
        Private method that checks if given num is int in range between min and max nums.
        :param num: (int) of input to check.
        :param min_num: (int) of min in range.
        :param max_num: (int) of max in range.
        :return: (boolean) True if is int and in range, False if otherwise.
        """
        if isinstance(num, int):
            if min_num <= num <= max_num:
                return True
            return False
