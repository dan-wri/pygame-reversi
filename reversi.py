import pygame


class Game:
    def __init__(self):
        self.__board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.__board_size = len(self.__board)

        self.__directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

    @property
    def board(self):
        return self.__board

    @property
    def board_size(self):
        return self.__board_size

    def playable(self):
        for row in self.__board:
            if 0 in row:
                return True
        return False

    def __is_on_board(self, row, col):
        return 0 <= row < self.__board_size and 0 <= col < self.__board_size

    def __pieces_to_flip(self, row: int, col: int, turn: int):
        if self.__board[row][col] != 0:
            return []

        pieces = []

        for row_change, col_change in self.__directions:
            current_pieces = []
            current_row, current_col = row + row_change, col + col_change

            while self.__is_on_board(current_row, current_col) and self.__board[current_row][current_col] != 0:
                if self.__board[current_row][current_col] == turn:
                    pieces.extend(current_pieces)
                    break

                current_pieces.append((current_row, current_col))
                current_row += row_change
                current_col += col_change

        return pieces

    def search_board(self, turn: int):
        options = set()

        for row in range(self.__board_size):
            for col in range(self.__board_size):
                if self.__pieces_to_flip(row, col, turn):
                    options.add((row, col))

        return options

    def update_board(self, index: tuple, turn: int):
        indexes = self.__pieces_to_flip(index[0], index[1], turn)

        if not indexes:
            raise ValueError("Invalid move (no pieces to flip)")

        for row, col in indexes:
            self.__board[row][col] = turn

        self.__board[index[0]][index[1]] = turn

    def determine_winner(self):
        sum_black = 0
        sum_white = 0

        for row in self.__board:
            sum_black += row.count(1)
            sum_white += row.count(2)

        if sum_black > sum_white:
            return (1, sum_black, sum_white)
        elif sum_white > sum_black:
            return (2, sum_black, sum_white)

        return None, sum_black, sum_white


class Application:
    def __init__(self):
        pygame.init()

        self.__size = 720
        self.__window = pygame.display.set_mode((self.__size, self.__size))
        self.__clock = pygame.time.Clock()

        self.__game = Game()
        self.__turn = 1

        self.__initialise_dimensions()
        self.__initialise_colours()
        self.__initialise_fonts()

    def __initialise_dimensions(self):
        # Inner Board Sizing
        self.__rect_s = self.__size * 0.7
        self.__rect_x = (self.__size - self.__rect_s) / 2
        self.__rect_y = (self.__size - self.__rect_s) / 1.4

        # Piece Spacing Logic
        self.__increment = self.__rect_s / self.__game.board_size
        self.__piece_size = self.__increment * 0.4

        # Header Placement Logic
        self.__restart_coords = (
            self.__rect_x + (self.__increment / 2) - (self.__piece_size / 2) + 2, self.__rect_y - (self.__increment / 2) - (self.__piece_size / 2) + 2)
        self.__instruction_piece_coords = (
            (self.__rect_x + self.__rect_s) - (self.__increment / 2) + 2, self.__rect_y - (self.__increment / 2) + 2)

        # End Game Dimensions
        self.__outer_x, self.__outer_y, self.__outer_w, self.__outer_h = self.__shrink_dimension(self.__rect_s, self.__rect_s, self.__rect_x,
                                                                                                 self.__rect_y, 0.7, 0.4)
        border_scale = min(self.__outer_w, self.__outer_h) * 0.015
        self.__inner_x, self.__inner_y, self.__inner_w, self.__inner_h = self.__insert_rect(self.__outer_w, self.__outer_h, self.__outer_x,
                                                                                            self.__outer_y, border_scale)

    def __shrink_dimension(self, org_w: float, org_h: float, org_x: float, org_y: float, shrink_w: float, shrink_h: float):
        new_w = org_w * shrink_w
        new_h = org_h * shrink_h

        new_x = org_x + (org_w - new_w) / 2
        new_y = org_y + (org_h - new_h) / 2

        return new_x, new_y, new_w, new_h

    def __insert_rect(self, org_w: float, org_h: float, org_x: float, org_y: float, border_scale: float):
        return org_x + border_scale, org_y + border_scale, org_w - border_scale * 2, org_h - border_scale * 2

    def __initialise_colours(self):
        self.__back_green = (104, 172, 71)
        self.__board_green = (10, 172, 71)
        self.__title_green_back = (34, 139, 34)
        self.__title_green = (4, 71, 48)

        self.__black = (0, 0, 0)
        self.__white = (255, 255, 255)

    def __initialise_fonts(self):
        pygame.font.init()
        self.__font = pygame.font.SysFont('sfpro', int(self.__piece_size))
        self.__title_font = pygame.font.SysFont(
            'sfpro', int(self.__piece_size * 2))
        self.__unicode_font = pygame.font.SysFont(
            'applesymbols, segoeuisymbol', int(self.__piece_size))

    def __build_board(self, options: set):
        current_board = self.__game.board
        board_size = len(current_board)

        self.__window.fill(self.__back_green)

        pygame.draw.rect(self.__window, self.__board_green,
                         (self.__rect_x, self.__rect_y, self.__rect_s, self.__rect_s))

        self.__draw_restart()
        self.__draw_instructions()
        self.__draw_lines(board_size)
        self.__draw_pieces(current_board, board_size,
                           options, self.__board_green)

        pygame.display.flip()

    def __draw_restart(self):
        restart_text = self.__font.render(
            "Restart", True, self.__board_green)
        restart_icon = self.__unicode_font.render(
            "↻", True, self.__board_green)

        padding = self.__piece_size / 5

        pygame.draw.rect(self.__window, self.__title_green,
                         (self.__restart_coords[0], self.__restart_coords[1], restart_text.get_width() + restart_icon.get_width() + padding * 4, self.__piece_size))

        self.__restart_coords_end = (self.__restart_coords[0] + restart_text.get_width(
        ) + restart_icon.get_width() + padding * 4, self.__restart_coords[1] + self.__piece_size)

        self.__window.blit(
            restart_text, (self.__restart_coords[0] + padding, self.__restart_coords[1] + padding))

        self.__window.blit(
            restart_icon, (self.__restart_coords[0] + restart_text.get_width() + padding * 2.3, self.__restart_coords[1] + padding * 0.4))

    def __draw_instructions(self):
        turn_text = "Player 1" if self.__turn == 1 else "Player 2"
        piece_colour = self.__black if self.__turn == 1 else self.__white
        instruction_text = self.__font.render(
            f"{turn_text}'s turn:", True, piece_colour)

        offset = 3.5  # TODO: Experiment with division instead of fixed offset value
        text_coords = ((self.__instruction_piece_coords[0] - (
            self.__piece_size / 2) - instruction_text.get_width()) - (offset * 2), self.__instruction_piece_coords[1] - (self.__piece_size / 3))
        self.__window.blit(instruction_text, text_coords)

        pygame.draw.circle(self.__window, piece_colour,
                           self.__instruction_piece_coords, self.__piece_size / 2)

    def __draw_lines(self, board_size: int):
        for index in range(board_size + 1):
            offset = index * self.__increment

            pygame.draw.line(self.__window, self.__black,
                             (self.__rect_x, self.__rect_y + offset), (self.__rect_x + self.__rect_s, self.__rect_y + offset), 3)

            pygame.draw.line(self.__window, self.__black,
                             (self.__rect_x + offset, self.__rect_y), (self.__rect_x + offset, self.__rect_y + self.__rect_s), 3)

    def __draw_pieces(self, current_board: list, board_size: int, options: set, option_colour: tuple):
        for row in range(board_size):
            for col in range(board_size):
                piece_val = current_board[row][col]

                if piece_val == 1:
                    self.__board_piece(row, col, self.__black)
                elif piece_val == 2:
                    self.__board_piece(row, col, self.__white)
                elif (row, col) in options:
                    self.__board_piece(
                        row, col, (170, 170, 170), option_colour)

    def __board_piece(self, row: int, col: int, colour: tuple, option_colour: tuple = None):
        piece_x = self.__rect_x + \
            (col * self.__increment) + (self.__increment / 2) + 1
        piece_y = self.__rect_y + \
            (row * self.__increment) + (self.__increment / 2) + 1
        coords = (piece_x, piece_y)

        pygame.draw.circle(self.__window, colour,
                           coords, self.__piece_size)
        if option_colour:
            pygame.draw.circle(self.__window, option_colour,
                               coords, self.__piece_size * 0.9)

    def __restart_game(self):
        self.__game = Game()
        self.__turn = 1

    def __end_game(self):
        pygame.draw.rect(self.__window, self.__black,
                         (self.__outer_x, self.__outer_y, self.__outer_w, self.__outer_h))

        pygame.draw.rect(self.__window, self.__back_green,
                         (self.__inner_x, self.__inner_y, self.__inner_w, self.__inner_h))

        self.__draw_endgame_text()

        pygame.display.flip()

    def __draw_endgame_text(self):
        back_endtitle_text = self.__title_font.render(
            "Game Over!", True, self.__title_green_back)

        t_width = back_endtitle_text.get_width()
        t_height = back_endtitle_text.get_height()

        inner_centre_horizontal = self.__inner_x + \
            (self.__inner_w - t_width) / 2
        inner_upper_quarter = self.__inner_y + \
            (self.__inner_h - t_height) / 5.5

        back_endtitle_text_coords = (
            inner_centre_horizontal - 2.5, inner_upper_quarter - 2.5)

        endtitle_text = self.__title_font.render(
            "Game Over!", True, self.__title_green)

        endtitle_text_coords = (inner_centre_horizontal, inner_upper_quarter)

        self.__window.blit(back_endtitle_text, back_endtitle_text_coords)
        self.__window.blit(endtitle_text, endtitle_text_coords)

        border_left = self.__inner_x + self.__inner_w * 0.1
        border_right = self.__inner_x + self.__inner_w - self.__inner_w * 0.1
        border_top = inner_upper_quarter + t_height + (t_height / 2)

        pygame.draw.line(self.__window, self.__title_green, (border_left,
                         border_top), (border_right, border_top), 2)

        winner, sum_black, sum_white = self.__game.determine_winner()

        left_offset = border_left * 1.05
        right_offset = border_right * 0.95
        top_offset = border_top * 1.05

        if winner == 1:
            parts = self.__winner_string(
                "Player 1", "Player 2", sum_black, sum_white)
        elif winner == 2:
            parts = self.__winner_string(
                "Player 2", "Player 1", sum_white, sum_black)
        else:
            words = ["It's ", "a ", "draw! ", "Looks ", "like ",
                     "you're ", "as ", "good ", "as ", "eachother..."]
            parts = tuple(self.__font.render(word, True, self.__title_green)
                          for word in words)

        x_offset = left_offset
        y_offset = top_offset

        for part in parts:
            if x_offset + part.get_width() > right_offset:
                x_offset = left_offset
                y_offset += part.get_height() + part.get_height() * 0.2

            self.__window.blit(part, (x_offset, y_offset))
            x_offset += part.get_width()

    def __winner_string(self, winner: str, loser: str, first_score: int, second_score: int):
        winner_colour = self.__black if winner == "black" else self.__white
        loser_colour = self.__black if loser == "black" else self.__white
        standard_colour = self.__title_green

        words = [
            (f"{winner.capitalize()} ", winner_colour),
            ("won, ", standard_colour),
            ("placing ", standard_colour),
            (f"{first_score} ", winner_colour),
            ("coin ", standard_colour),
            ("pieces ", standard_colour),
            ("compared ", standard_colour),
            ("to ", standard_colour),
            (f"{loser}'s ", loser_colour),
            (f"{second_score} ", loser_colour),
            ("pieces. ", standard_colour),
            ("Well ", standard_colour),
            ("done ", standard_colour),
            (f"{winner}!", winner_colour)
        ]

        return tuple(
            self.__font.render(word, True, colour)
            for word, colour in words
        )

    def run(self):
        options = self.__game.search_board(self.__turn)
        self.__build_board(options)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.__restart_coords[0] < event.pos[0] < self.__restart_coords_end[0] and self.__restart_coords[1] < event.pos[1] < self.__restart_coords_end[1]:
                        self.__restart_game()
                        options = self.__game.search_board(self.__turn)
                        self.__build_board(options)

                if self.__game.playable() and options:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for index in options:
                            x = self.__rect_x + index[1] * self.__increment
                            y = self.__rect_y + index[0] * self.__increment
                            if x < event.pos[0] < x + self.__increment and y < event.pos[1] < y + self.__increment:
                                self.__game.update_board(index, self.__turn)
                                self.__turn = 3 - self.__turn

                                options = self.__game.search_board(self.__turn)
                                self.__build_board(options)
                                break
                else:
                    self.__end_game()

            self.__clock.tick(60)


Application().run()
