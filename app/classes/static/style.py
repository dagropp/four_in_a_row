from app.data import game_data as data
import tkinter as tk


class Style:
    # Screen design consts determine fonts, borders, background, images paths and messages to the user.
    FONT = {'S': ('system', 20), 'M': ('system', 30)}
    BORDER = {'NONE': 0, 'S': 10, 'M': 20, 'L': 30, 'XL': 60}
    COLOR = {
        'BG_DEFAULT': 'black', 'BOARD': '#550000', 'TXT_DEFAULT': 'white', 'NOTICE': '#FF00AA', 'MESSAGE': '#00FF00',
        'PLAYER': {1: '#FF0000', 2: '#55FFFF'}
    }
    IMG_DIR = r'assets\images\\'
    IMAGES = {
        'TITLE': IMG_DIR + 'title.png',
        'CELL': {1: IMG_DIR + 'cell_1.png', 2: IMG_DIR + 'cell_2.png', data.INITIAL_VAL: IMG_DIR + 'cell_none.png',
                 data.WIN_VAL: IMG_DIR + 'cell_win.png'},
    }
    # Images paths for players: False/True if player is inactive/active, 1/2 for player num, 1/0 for human/AI.
    IMG_PLAYER = {
        False: {
            1: {1: IMG_DIR + 'player_1.png', 0: IMG_DIR + 'ai_1.png'},
            2: {1: IMG_DIR + 'player_2.png', 0: IMG_DIR + 'ai_2.png'}
        },
        True: {
            1: {1: IMG_DIR + 'player_1_active.png', 0: IMG_DIR + 'ai_1_active.png'},
            2: {1: IMG_DIR + 'player_2_active.png', 0: IMG_DIR + 'ai_2_active.png'}
        },
        'WIN': {
            0: {0: IMG_DIR + 'tie.png'},
            1: {1: IMG_DIR + 'player_1_win.png', 0: IMG_DIR + 'ai_1_win.png'},
            2: {1: IMG_DIR + 'player_2_win.png', 0: IMG_DIR + 'ai_2_win.png'}
        },
        'CLICK': {
            1: {1: IMG_DIR + 'click_1.png', 0: IMG_DIR + 'click_ai_1.png'},
            2: {1: IMG_DIR + 'click_2.png', 0: IMG_DIR + 'click_ai_2.png'},
            'WIN': {0: IMG_DIR + 'click_tie.png', 1: IMG_DIR + 'click_win_1.png', 2: IMG_DIR + 'click_win_2.png'},
            'NONE': IMG_DIR + 'click_empty.png'
        }
    }
    TITLE = {
        'PLAYER': {1: 'PLAYER 1', 2: 'PLAYER 2'},
        'START': 'START GAME',
        'QUIT': 'QUIT'
    }
    MESSAGE = {
        'GUIDE_UP': 'PRESS [Esc] TO QUIT PROGRAM [BACKSPACE] TO RETURN TO MAIN MENU',
        'GUIDE_MENU': 'CLICK ON PLAYER BUTTON TO SWITCH BETWEEN PERSON / COMPUTER',
        'WINNER': {0: 'GAME IS TIED...', 1: TITLE['PLAYER'][1] + ' HAS WON THE GAME!',
                   2: TITLE['PLAYER'][2] + ' HAS WON THE GAME!'},
        'GREETINGS': {0: 'GAME IS TIED...', 1: 'CONGRATULATIONS ' + TITLE['PLAYER'][1],
                      2: 'CONGRATULATIONS ' + TITLE['PLAYER'][2]},
        'TIE': 'GAME IS TIED...',
        'DO_NOW': 'WHAT WOULD YOU LIKE TO DO NOW?'
    }
    # Screen size to determine if to use small or large screen adjustments.
    LG_SCREEN = 1000

    @staticmethod
    def create_menu_button(frame, text, command, width_ratio=1.0, bg=COLOR['BG_DEFAULT']):
        """
        Function for all screen classes, that creates Tkinter menu buttons more efficiently.
        :param frame: Tkinter (Frame) object to put button in.
        :param text: (str) containing text to put in button.
        :param command: (method) for button to call.
        :param width_ratio: (float) of ratio of default button width.
        :param bg: (str) containing background color (default='black').
        :return: Tkinter (Button) object with requested image.
        """
        new_button = tk.Button(frame, text=text, relief='ridge', command=command, font=Style.FONT['S'],
                               bd=Style.BORDER['S'], bg=bg, fg=Style.COLOR['TXT_DEFAULT'], activebackground=bg,
                               activeforeground=Style.COLOR['MESSAGE'], width=int(30 * width_ratio))
        return new_button

    @staticmethod
    def create_image_label(frame, img_path, bd=BORDER['NONE']):
        """
        Function for all screen classes, that creates Tkinter image label more efficiently.
        :param frame: Tkinter (Frame) object to put label in.
        :param img_path: (str) containing path to image file.
        :param bd: (int) containing request border size. default=0.
        :return: Tkinter (Label) object with requested image.
        """
        img = tk.PhotoImage(file=img_path)
        img_label = tk.Label(frame, image=img, bg=Style.COLOR['BG_DEFAULT'], bd=bd)
        img_label.image = img
        return img_label

    @staticmethod
    def configure_image_label(label, img_path):
        """
        Function for all screen classes, that modifies Tkinter image label more efficiently.
        :param label: Tkinter (Label) object to modify.
        :param img_path: (str) containing path to image file for the label.
        """
        img = tk.PhotoImage(file=img_path)
        label.configure(image=img)
        label.image = img

    @staticmethod
    def create_text_label(frame, text, font, fg=COLOR['TXT_DEFAULT'], bd=BORDER['NONE']):
        """
        Function for all screen classes, that creates Tkinter text label more efficiently.
        :param frame: Tkinter (Frame) object to put label in.
        :param text: (str) containing text to put in label.
        :param font: (tuple) of (str) and (int) with font and size for the text.
        :param fg: (str) containing text color (default='white').
        :param bd: (int) containing request border size. default=0.
        :return: Tkinter (Label) object with requested text.
        """
        label = tk.Label(frame, text=text, font=font, bg=Style.COLOR['BG_DEFAULT'], fg=fg, bd=bd)
        return label
