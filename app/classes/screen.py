from ..data import game_data as data
import tkinter as tk
from .game import Game
from .ai import AI
from .static.style import Style


class Screen:
    """
    This classes creates the base screen, a blank full screen.
    """

    def __init__(self):
        """
        Init method for Screen. Starts tkinter widget (a blank full screen) and creates ScreenMenu instance.
        """
        self.__root = tk.Tk()
        self._blank_full_screen()
        self._game_title()
        ScreenMenu(self.__root)
        self.__root.mainloop()

    def _blank_full_screen(self):
        """
        This method creates a blank full screen.
        """
        # Defines the screen to be full screen in black.
        self.__root.overrideredirect(True)
        self.__root.geometry('{0}x{1}+0+0'.format(self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()))
        # Changes focus to this widget
        self.__root.focus_set()
        self.__root.configure(bg=Style.COLOR['BG_DEFAULT'])
        # Keyboard shortcuts - <Escape> to quit program,
        self.__root.bind('<Escape>', lambda event: self.__root.destroy())

    def _game_title(self):
        """
        This method creates game titles, visible on all screens, considering screen height.
        """
        screen_height = self.__root.winfo_screenheight()
        # The border for guide message, defined by screen height.
        msg_border = Style.BORDER['NONE'] if screen_height < Style.LG_SCREEN else Style.BORDER['M']
        Style.create_text_label(self.__root, Style.MESSAGE['GUIDE_UP'], Style.FONT['S'], Style.COLOR['MESSAGE'],
                                msg_border).pack()
        # If screen is large, creates game title image, so it is visible on all screens.
        if screen_height >= Style.LG_SCREEN:
            Style.create_image_label(self.__root, Style.IMAGES['TITLE'], Style.BORDER['M']).pack()


class ScreenMenu:
    """
    This classes creates the Main Menu screen, in which the user chooses between player types (human or AI),
    starts the game, or quits.
    """

    def __init__(self, root):
        """
        Init method for ScreenMenu.
        :param root: Tkinter widget root created in Screen classes.
        """
        self.__root = root
        # Player's type. Default=1: Human, 0: AI. Changed with specific method by the user.
        self.__player = {1: 1, 2: 1}
        # Creates main menu frame according to screen height.
        screen_height = self.__root.winfo_screenheight()
        # Assign boolean var if screen is small, than needs to fit.
        fit_screen = screen_height < Style.LG_SCREEN
        # Assign the correct adjustment for case of small or large screen.
        screen_adjust = {'expand': True if fit_screen else False,
                         'bd': Style.BORDER['NONE'] if fit_screen else Style.BORDER['XL'],
                         'func': self._create_title if fit_screen else None}
        # Creates adjusted main menu frame.
        self.__frame = tk.Frame(self.__root, bg=Style.COLOR['BG_DEFAULT'], bd=screen_adjust['bd'])
        self.__frame.pack(expand=screen_adjust['expand'])
        # If small screen, calls _create_title() method that creates small title frame.
        screen_adjust['func']() if screen_adjust['func'] else None
        # Changes focus to this frame
        self.__frame.focus_set()
        # Calls private method to create actual menu.
        self._create_menu()

    def _create_title(self):
        """
        Private method that creates small title frame, if screen is small.
        """
        title_frame = tk.Frame(self.__frame, bg=Style.COLOR['BG_DEFAULT'])
        title_frame.grid(row=0, column=1, rowspan=2, columnspan=2)
        Style.create_image_label(title_frame, Style.IMAGES['TITLE'], Style.BORDER['M']).pack()

    def _create_menu(self):
        """
        Private method that creates the menu items in the menu frame widget.
        """
        # Creates text label with message to the user on how to switch between HUMAN / COMPUTER (AI).
        guide = Style.create_text_label(self.__frame, Style.MESSAGE['GUIDE_MENU'], Style.FONT['S'],
                                        Style.COLOR['NOTICE'], Style.BORDER['S'])
        guide.configure(wraplength=600)
        guide.grid(row=2, column=1, columnspan=2)
        # Creates image label with current avatar representation of each player (default=human).
        player_avatar = {
            1: Style.create_image_label(self.__frame, self._avatar_image(1), Style.BORDER['M']),
            2: Style.create_image_label(self.__frame, self._avatar_image(2), Style.BORDER['M'])
        }
        player_avatar[1].grid(row=4, column=1)
        player_avatar[2].grid(row=4, column=2)
        # Creates players' buttons, to change the player between human / computer.
        Style.create_menu_button(self.__frame, Style.TITLE['PLAYER'][1],
                                 lambda: self._change_player(player_avatar[1], 1),
                                 0.5, Style.COLOR['PLAYER'][1]).grid(row=3, column=1),
        Style.create_menu_button(self.__frame, Style.TITLE['PLAYER'][2],
                                 lambda: self._change_player(player_avatar[2], 2),
                                 0.5, Style.COLOR['PLAYER'][2]).grid(row=3, column=2)
        # Creates buttons to start game and quit.
        Style.create_menu_button(self.__frame, Style.TITLE['START'], self._go_to_game).grid(row=5, column=1,
                                                                                            columnspan=2)
        Style.create_menu_button(self.__frame, Style.TITLE['QUIT'], self.__root.destroy).grid(row=6, column=1,
                                                                                              columnspan=2)

    def _avatar_image(self, player):
        """
        Private method that returns image of specified player, according to its type - human / computer.
        :param player: (int) representing player number.
        :return: (str) containing image path of player avatar.
        """
        # if self.__player is 1 return human avatar, if 0 return computer avatar.
        return Style.IMG_PLAYER[False][player][self.__player[player]]

    def _change_player(self, label, player):
        """
        Private method that is called by clicking 'PLAYER' buttons in main menu,
        that toggles self.__player between 1-0 and changes the avatar picture accordingly.
        :param label: Tkinter (Label) object containing avatar pic to modify.
        :param player: (int) representing player number.
        """
        # Toggle player var between 1-0.
        self.__player[player] = (self.__player[player] + 1) % 2
        # Change the picture of the avatar.
        Style.configure_image_label(label, self._avatar_image(player))

    def _go_to_game(self):
        """
        Private method that destroys this screen main frame and creates new ScreenGame instance.
        """
        self.__frame.destroy()
        ScreenGame(self.__root, self.__player[1], self.__player[2])


class ScreenGame:
    """
    This classes Creates the Game screen, and runs the game according to the specified settings: Creates GUI for
    the user to see the game board, move to the requested column, and let the AI player (if specified) make its turns.
    (If only AI players are set, the user can watch the game with a slight delay between turns, for a natural feel).
    """

    def __init__(self, root, player1, player2, stats1=0, stats2=0):
        """
        Init method for ScreenGame.
        :param root: Tkinter widget root created in Screen classes.
        :param player1: (int) in range (1-0) regarding player 1 type - 1: human, 2: AI.
        :param player2: (int) in range (1-0) regarding player 2 type - 1: human, 2: AI.
        :param stats1: (int) of how many wins player 1 had. default=0.
        :param stats2: (int) of how many wins player 2 had. default=0.
        """
        self.__root = root
        self.__player = {1: player1, 2: player2}
        self.__stats = {1: stats1, 2: stats2}
        # Creates new Game instance.
        self.__game = Game()
        # Assigns to var the game board list from Game classes.
        self.__board = self.__game.get_board()
        # Assigns winner var. later if winner is found contains winning player number.
        self.__winner = None
        # Creates new AI instances (0-2) according to players identities.
        self.__ai = {
            1: AI(self.__game, 1) if not self.__player[1] else 0,
            2: AI(self.__game, 2) if not self.__player[2] else 0}
        # Main game frame
        self.__frame = tk.Frame(self.__root, bg=Style.COLOR['BG_DEFAULT'])
        self.__frame.pack()
        # Changes focus to this frame
        self.__frame.focus_set()
        # Calls private method to create actual game frames widgets.
        self._create_board()
        # Keyboard shortcut - backspace to return to main menu
        self.__frame.bind('<BackSpace>', lambda event: _go_to_menu(self.__frame, self.__root))

    def _create_board(self):
        """
        Private method that creates game screen widgets.
        """
        # Calls private method that creates side frames for each player.
        self._create_player_frame(1, 1)
        self._create_player_frame(2, 3)
        # Column controllers frame.
        ctrl_frame = tk.Frame(self.__frame, bg=Style.COLOR['BG_DEFAULT'], padx=10)
        ctrl_frame.grid(row=1, column=2)
        # Game actual board frame.
        board_frame = tk.Frame(self.__frame, bg=Style.COLOR['BOARD'], bd=Style.BORDER['S'], relief='ridge')
        board_frame.grid(row=2, column=2)
        # Using private method, creates in ctrl frame grid of buttons that moves disc to column.
        self._create_col_buttons(ctrl_frame, board_frame)
        # Using private method, creates in board frame grid of rows and columns of the game board.
        self._create_board_gfx(board_frame)
        # Calls AI move method - operates only when AI player turn.
        self._ai_move(board_frame)

    def _create_player_frame(self, player, col):
        """
        Private method that creates side frames for each player.
        :param player: (int) representing player number.
        :param col: (int) of column to assign to grid widget.
        """
        # Creates frame
        frame = tk.Frame(self.__frame, bg=Style.COLOR['BG_DEFAULT'], bd=Style.BORDER['M'])
        frame.grid(row=2, column=col)
        # Creates image label for player avatar - False for inactive (default), player num, and player type (human/AI).
        avatar_img = Style.create_image_label(frame, Style.IMG_PLAYER[False][player][self.__player[player]])
        avatar_img.pack()
        # Creates text label of players names and game statistics so far (originally 0).
        player_title = Style.create_text_label(frame, Style.TITLE['PLAYER'][player], Style.FONT['M'])
        player_title.pack()
        stats_title = Style.create_text_label(frame, (self.__stats[player], 'WINS'), Style.FONT['S'],
                                              Style.COLOR['TXT_DEFAULT'])
        stats_title.pack()
        # Call method to change player colors and image if active/inactive.
        self._signal_player_turn(avatar_img, player_title, stats_title, player)

    def _signal_player_turn(self, avatar_img, player_title, stats_title, player):
        """
        Private method that changes player colors and image if active/inactive.
        :param avatar_img: Tkinter (Label) object to modify with player image.
        :param player_title: Tkinter (Label) object to modify with player name.
        :param stats_title: Tkinter (Label) object to modify with player statistics.
        :param player: (int) representing player number.
        :return: None if winner is found.
        """
        if self.__winner is not None:
            return
        # Assign boolean var. True: if this player is the current player's turn in the game. False: if otherwise.
        player_turn = player == self.__game.get_current_player()
        # Change avatar label image. True/False if player turn or not, player num, player type (human/ai).
        Style.configure_image_label(avatar_img, Style.IMG_PLAYER[player_turn][player][self.__player[player]])
        # Change text color for active if player turn and for default if not.
        txt_color = Style.COLOR['PLAYER'][player] if player_turn else Style.COLOR['TXT_DEFAULT']
        player_title.configure(fg=txt_color)
        stats_title.configure(fg=txt_color)
        # Re-calls this same method over and over, to continually changing player's status.
        self.__frame.after(100, self._signal_player_turn, avatar_img, player_title, stats_title, player)

    def _create_col_buttons(self, ctrl_frame, board_frame):
        """
        Private method that creates in ctrl frame grid of buttons that moves disc to column.
        :param ctrl_frame: Tkinter (Frame) object to create the col buttons in.
        :param board_frame: Tkinter (Frame) to change if col button is clicked.
        """
        # Goes over all the columns of the game board, and:
        for col in range(len(self.__board[0])):
            # Creates an initial (and same) icon for all col buttons.
            col_button = Style.create_image_label(ctrl_frame, Style.IMG_PLAYER['CLICK']['NONE'])
            col_button.grid(row=0, column=col)
            # Binds action to left mouse clicker: call _col_click() method that moves disc to column.
            col_button.bind('<Button-1>', lambda event, b_f=board_frame, c=col: self._col_click(b_f, c))
            # Binds action to mouse hover (in and out): call _enter_col()/_leave_col() method that changes col icon.
            col_button.bind('<Enter>', lambda event, c_b=col_button: self._enter_col(c_b))
            col_button.bind('<Leave>', lambda event, c_b=col_button: self._leave_col(c_b))

    def _enter_col(self, col_button):
        """
        Private method that changes col button icon when mouse hovers over it.
        :param col_button: Tkinter (Button) object to modify.
        :return: None if winner is found.
        """

        # If winner was found changes the image to trophy.
        if self.__winner is not None:
            Style.configure_image_label(col_button, Style.IMG_PLAYER['CLICK']['WIN'][self.__winner])
            return
        this_player = self.__game.get_current_player()
        # Change col button image according to current player turn and type.
        Style.configure_image_label(col_button, Style.IMG_PLAYER['CLICK'][this_player][self.__player[this_player]])

    def _leave_col(self, col_button):
        """
        Private method that changes col button icon to initial icon when mouse hovers out of it.
        :param col_button: Tkinter (Button) object to modify.
        """
        # Upon mouse leave, changes col button image to initial icon.
        Style.configure_image_label(col_button, Style.IMG_PLAYER['CLICK']['NONE'])

    def _create_board_gfx(self, frame):
        """
        Private method that creates in board frame a grid of rows and columns of the Game board.
        :param frame: Tkinter (Frame) object to assign the grid to.
        """
        # Goes over all the board list (2d list of rows and cols), and:
        for row in range(len(self.__board)):
            for col in range(len(self.__board[row])):
                # Checks which val in each col (1, 2, initial val or winner val).
                pos_val = self.__board[row][col]
                # Creates image label for the appropriate val found, and assigns it to grid in same row and col.
                cell = Style.create_image_label(frame, Style.IMAGES['CELL'][pos_val])
                cell.grid(row=row, column=col)

    def _ai_move(self, board_frame):
        """
        Recurring method that operates only when AI player turn.
        :param board_frame: Tkinter (Frame) object to modify game board if necessary.
        :return: None if winner was found (or tie).
        """
        if self.__winner is not None:
            return
        # Checks if the current player is an AI player, and if so:
        if self.__ai[self.__game.get_current_player()]:
            # Calls find_legal_move() method from AI classes, that returns optimal column for player to go to.
            col = self.__ai[self.__game.get_current_player()].find_legal_move()
            # Delays action by 1 second for a natural feel for the game, and calls method that moves to specified col.
            board_frame.after(data.BASE_SPEED, self._move_to_col, board_frame, col)
        # Re-calls this same method each 1 second: It will check if current player is an AI player,
        # if not, will call method again and if so do the same actions described above.
        board_frame.after(data.BASE_SPEED, self._ai_move, board_frame)

    def _col_click(self, board_frame, col):
        """
        Private method that moves disc to column, if human clicked a col button.
        :param board_frame: Tkinter (Frame) object to modify game board if necessary.
        :param col: (int) representing col to go to.
        :return: None if current player turn is AI or winner was found.
        """
        if not self.__player[self.__game.get_current_player()] or self.__winner is not None:
            return
        # Calls method that moves to specified col.
        self._move_to_col(board_frame, col)

    def _move_to_col(self, board_frame, col):
        """
        Private method that moves to specified col, either by AI or by human players.
        :param board_frame: Tkinter (Frame) object to modify game board if possible.
        :param col: (int) representing col to go to.
        :return: None if (1) col was not vacant. (2) winner was found.
        """
        # Tries to make the specified move, if failed returns.
        try:
            self.__game.make_move(col)
        except:
            return
        # Calls get_winner() method from Game classes and assign it to winner var:
        self.__winner = self.__game.get_winner()
        # Recreates the board with updated icons.
        self._create_board_gfx(board_frame)
        # If winner var is not None, game is over and pops up winner frame after 1 second.
        if self.__winner is not None:
            self.__frame.after(data.BASE_SPEED, self._create_winner_frame)
        # Adds 1 turn to game.
        self.__game.add_turn()

    def _create_winner_frame(self):
        """
        Private method that creates pop up winner frame
        """
        # Creates the pop up banner frame and places it in middle of screen.
        banner_frame = tk.Frame(self.__root, bg=Style.COLOR['BG_DEFAULT'], relief='ridge', bd=Style.BORDER['M'])
        banner_frame.place(relx=0.5, rely=0.5, anchor='center')
        # Changes focus to this frame
        banner_frame.focus_set()
        # Creates text and image labels with message and winning icon (or tie).
        player_type = self.__player[self.__winner] if self.__winner else 0
        Style.create_image_label(banner_frame, Style.IMG_PLAYER['WIN'][self.__winner][player_type],
                                 Style.BORDER['L']).pack()
        Style.create_text_label(banner_frame, Style.MESSAGE['WINNER'][self.__winner], Style.FONT['M'],
                                Style.COLOR['NOTICE'], Style.BORDER['L']).pack()
        # Exits game board and creates new ScreenWin instance after 3.5 seconds.
        self.__frame.after(data.TRANSITION_SPEED, self._go_to_win_screen, banner_frame)
        return

    def _go_to_win_screen(self, banner_frame):
        """
        Private method that destroys this screen main frame and creates new ScreenWin instance.
        """
        banner_frame.destroy()
        self.__frame.destroy()
        ScreenWin(self.__root, self.__winner, self.__player[1], self.__player[2], self.__stats[1], self.__stats[2])


class ScreenWin:
    """
    This classes creates the winning screen, that displays this game's winner and offers additional actions:
    Play again with the same players settings and statistics. Go back to Main Menu and reset settings or Quit game.
    """

    def __init__(self, root, winner, player1, player2, stats1, stats2):
        """
        Init method for ScreenWin.
        :param root: Tkinter widget root created in Screen classes.
        :param winner: (int) in range (0-2) of the player number who won (0 for tie).
        :param player1: (int) in range (1-0) regarding player 1 type - 1: human, 2: AI.
        :param player2: (int) in range (1-0) regarding player 2 type - 1: human, 2: AI.
        :param stats1: (int) of how many wins player 1 had.
        :param stats2: (int) of how many wins player 2 had.
        """
        self.__root = root
        self.__winner = winner
        self.__player = {1: player1, 2: player2}
        self.__stats = {1: stats1, 2: stats2}
        # If winner var is not 0, adds to said player 1 win for the statistics.
        if self.__winner:
            self.__stats[self.__winner] += 1
        # Main win frame
        self.__frame = tk.Frame(self.__root, bg=Style.COLOR['BG_DEFAULT'], bd=Style.BORDER['XL'])
        self.__frame.pack()
        # Changes focus to this frame
        self.__frame.focus_set()
        # Calls private method to create actual win frame widgets.
        self._create_message()
        # Keyboard shortcut
        self.__frame.bind('<BackSpace>', lambda event: _go_to_menu(self.__frame, self.__root))

    def _create_message(self):
        """
        Private method that creates win frame widgets.
        """
        # Creates text label with winning/tie message.
        Style.create_text_label(self.__frame, Style.MESSAGE['GREETINGS'][self.__winner], Style.FONT['M'],
                                Style.COLOR['NOTICE'], Style.BORDER['L']).pack()
        Style.create_text_label(self.__frame, Style.MESSAGE['DO_NOW'], Style.FONT['S'], Style.COLOR['MESSAGE'],
                                Style.BORDER['M']).pack()
        # Creates menu buttons. PLAY AGAIN - to play with same settings and statistics.
        Style.create_menu_button(self.__frame, 'PLAY AGAIN', self._go_to_game_again).pack()
        # MAIN MENU - to go back to main menu and start again, and QUIT to quit program.
        Style.create_menu_button(self.__frame, 'MAIN MENU', lambda: _go_to_menu(self.__frame, self.__root)).pack()
        Style.create_menu_button(self.__frame, 'QUIT', self.__root.destroy).pack()
        # Create winning player icon based on winner number (or tie) and type.
        player_type = self.__player[self.__winner] if self.__winner else 0
        Style.create_image_label(self.__frame, Style.IMG_PLAYER['WIN'][self.__winner][player_type],
                                 Style.BORDER['L']).pack()

    def _go_to_game_again(self):
        """
        Private method that destroys this screen main frame and creates new ScreenGame instance,
        with the same settings and statistics.
        """
        self.__frame.destroy()
        ScreenGame(self.__root, self.__player[1], self.__player[2], self.__stats[1], self.__stats[2])


def _go_to_menu(frame, root):
    """
    Function for all screen classes that destroys a screen's main frame and creates new MenuScreen instance.
    :param frame: Tkinter (Frame) object to destroy.
    :param root: Tkinter root widget to operate on.
    """
    frame.destroy()
    ScreenMenu(root)
