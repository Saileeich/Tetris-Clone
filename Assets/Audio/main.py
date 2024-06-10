import pygame
from pygame.locals import *
import random
import math

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load("Assets/Audio/HipBop.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()
playing_music = False

icon = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon)

OLE_JACOB = pygame.image.load("Assets/olejacob.png")

BUTTON = pygame.mixer.Sound("Assets/Audio/Button.wav")
DROP = pygame.mixer.Sound("Assets/Audio/Drop.wav")
GAME_OVER = pygame.mixer.Sound("Assets/Audio/Game_over.wav")
LEVEL_UP = pygame.mixer.Sound("Assets/Audio/Level_up.wav")
MOVE_DOWN = pygame.mixer.Sound("Assets/Audio/Move_down.wav")
MOVE = pygame.mixer.Sound("Assets/Audio/Move.wav")
ROTATE = pygame.mixer.Sound("Assets/Audio/Rotate.wav")
SOLIDIFY = pygame.mixer.Sound("Assets/Audio/Solidify.wav")
PAUSE = pygame.mixer.Sound("Assets/Audio/Pause.wav")
HOLD = pygame.mixer.Sound("Assets/Audio/Hold.wav")
SOFT_DROP = pygame.mixer.Sound("Assets/Audio/Soft_drop.wav")


HEIGHT = 480
WIDTH = 480
FPS = 30
MOVE_TIME = 80

COL1 = (63, 50, 50)
COL2 = (2, 2, 2)

down_tick_check = 1
move_down_time = 1000 / 20

total_cleared_lines = 0
score = 0
difficult = 0
level = 1

FramePerSec = pygame.time.Clock()

# title = pygame.font.Font("Roboto-Regular.ttf", 20)
# info_font = pygame.font.Font("Roboto-Regular.ttf", 15)
big_title = pygame.font.Font("Assets/joystix monospace.otf", 30)
title = pygame.font.Font("Assets/joystix monospace.otf", 15)
info_font = pygame.font.Font("Assets/joystix monospace.otf", 10)

surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tertis")

board = []
for row in range(22):
    board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

move = {"left": False, "right": False, "down": False}

hold = []
can_hold = True

tspin = False
tspin_corners = {"front": 0, "back": 0}
can_tspin = False

tetronimos_choice = [0, 1, 2, 3, 4, 5, 6]
bag = tetronimos_choice.copy()
random.shuffle(bag)
first_tetronimos = [bag.pop(0), bag.pop(1)]

last_mouse1 = 0
time_paused = 0
start_pause_time = 0

highscores = []

running = True
paused = False
menu = True
game_over = False
global tetr


class Tetronimo:
    def __init__(self, id, position=0):
        self.id = id
        match id:
            # I-piece
            case 0:
                # x
                # x
                # x
                # x
                self.color = (96, 193, 203)

                self.states = [
                    [(-1, 0), (0, 0), (1, 0), (2, 0)],
                    [(0, -1), (0, 0), (0, 1), (0, 2)],
                    [(-2, 0), (-1, 0), (0, 0), (1, 0)],
                    [(0, -2), (0, -1), (0, 0), (0, 1)],
                ]

                self.rotation_offset = [
                    [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)],
                    [(0, 1), (0, 1), (0, 1), (0, -1), (0, -2)],
                    [(-1, 1), (1, 1), (-2, 1), (1, 0), (-2, 0)],
                    [(-1, 0), (0, 0), (0, 0), (0, 1), (0, -2)],
                ]
            # J-piece
            case 1:
                #   x
                #   x
                # x x
                self.color = (65, 86, 158)

                self.states = [
                    [(-1, -1), (-1, 0), (0, 0), (1, 0)],
                    [(1, -1), (0, -1), (0, 0), (0, 1)],
                    [(-1, 0), (0, 0), (1, 0), (1, 1)],
                    [(0, -1), (0, 0), (0, 1), (-1, 1)],
                ]

                self.rotation_offset = [
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                ]
            # L-piece
            case 2:
                # x
                # x
                # x x
                self.color = (227, 167, 51)

                self.states = [
                    [(-1, 0), (0, 0), (1, 0), (1, -1)],
                    [(0, -1), (0, 0), (0, 1), (1, 1)],
                    [(-1, 1), (-1, 0), (0, 0), (1, 0)],
                    [(-1, -1), (0, -1), (0, 0), (0, 1)],
                ]

                self.rotation_offset = [
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                ]
            # O-piece
            case 3:
                # x x
                # x x
                self.color = (225, 222, 63)

                self.states = [
                    [(0, 0), (1, 0), (1, -1), (0, -1)],
                    [(0, 0), (1, 0), (1, -1), (0, -1)],
                    [(0, 0), (1, 0), (1, -1), (0, -1)],
                    [(0, 0), (1, 0), (1, -1), (0, -1)],
                ]

                self.rotation_offset = [[(0, 0)], [(0, 0)], [(0, 0)], [(0, 0)]]
            # S-piece
            case 4:
                #   x x
                # x x
                self.color = (91, 181, 79)

                self.states = [
                    [(-1, 0), (0, 0), (0, -1), (1, -1)],
                    [(0, -1), (0, 0), (1, 0), (1, 1)],
                    [(-1, 1), (0, 1), (0, 0), (1, 0)],
                    [(-1, -1), (-1, 0), (0, 0), (0, 1)],
                ]

                self.rotation_offset = [
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                ]
            # T-piece
            case 5:
                # x x x
                #   x
                self.color = (135, 89, 159)

                self.states = [
                    [(-1, 0), (0, 0), (0, -1), (1, 0)],
                    [(0, -1), (0, 0), (1, 0), (0, 1)],
                    [(-1, 0), (0, 0), (0, 1), (1, 0)],
                    [(-1, 0), (0, 0), (0, -1), (0, 1)],
                ]

                self.rotation_offset = [
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                ]

                self.tspin_checks = [
                    [(-1, -1), (1, -1), (-1, 1), (1, 1)],
                    [(1, -1), (1, 1), (-1, -1), (-1, 1)],
                    [(-1, 1), (1, 1), (-1, -1), (1, -1)],
                    [(-1, 1), (-1, -1), (1, -1), (1, 1)],
                ]
            # Z-piece
            case 6:
                # x x
                #   x x
                self.color = (224, 62, 54)

                self.states = [
                    [(-1, -1), (0, -1), (0, 0), (1, 0)],
                    [(0, 1), (0, 0), (1, 0), (1, -1)],
                    [(-1, 0), (0, 0), (0, 1), (1, 1)],
                    [(-1, 1), (-1, 0), (0, 0), (0, -1)],
                ]

                self.rotation_offset = [
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
                    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
                ]

        self.state = 0
        self.old_state = 0

        self.pos = position
        self.old_pos = position

        self.side_time = 0
        self.down_time = 0
        self.lock_down_timer = False
        self.lock_down_time = 0
        self.lock_rotations = 0

        self.blink_time = 0
        self.blinked = False

        if position != 0:
            if self.check_collision(self.pos, self.state)["block"]:
                # Game over
                global game_over
                global start_pause_time
                start_pause_time = pygame.time.get_ticks()
                GAME_OVER.play()
                game_over = True

                with open("highscores.csv", "a") as file:
                    file.write(";" + str(math.floor(score)))

            self.toggle_self_on_board()

    def toggle_self_on_board(self):
        # Turn off old pos
        for pos in self.states[self.old_state]:
            board[self.old_pos[1] + pos[1] + 2][self.old_pos[0] + pos[0]] = 0

        # Turn on new pos
        for pos in self.states[self.state]:
            board[self.pos[1] + pos[1] + 2][self.pos[0] + pos[0]] = [self.color, 1]

        self.old_pos = self.pos
        self.old_state = self.state

    def deactivate_tetronimo(self):
        if self.blinked:
            self.color = (self.color[0] - 25, self.color[1] - 25, self.color[2] - 25)
            self.blinked = False

        for pos in self.states[self.state]:
            board[self.pos[1] + pos[1] + 2][self.pos[0] + pos[0]] = [self.color, 0]

        global tspin
        global tspin_corners
        if self.id == 5 and can_tspin:
            tspin_corners = {"front": 0, "back": 0}
            if sum(
                value == True
                for value in self.check_collision(
                    (
                        self.pos[0] + self.tspin_checks[self.state][0][0],
                        self.pos[1] + self.tspin_checks[self.state][0][1],
                    ),
                    self.state,
                ).values()
            ):
                tspin_corners["front"] += 1
            if sum(
                value == True
                for value in self.check_collision(
                    (
                        self.pos[0] + self.tspin_checks[self.state][1][0],
                        self.pos[1] + self.tspin_checks[self.state][1][1],
                    ),
                    self.state,
                ).values()
            ):
                tspin_corners["front"] += 1
            if sum(
                value == True
                for value in self.check_collision(
                    (
                        self.pos[0] + self.tspin_checks[self.state][2][0],
                        self.pos[1] + self.tspin_checks[self.state][2][1],
                    ),
                    self.state,
                ).values()
            ):
                tspin_corners["back"] += 1
            if sum(
                value == True
                for value in self.check_collision(
                    (
                        self.pos[0] + self.tspin_checks[self.state][3][0],
                        self.pos[1] + self.tspin_checks[self.state][3][1],
                    ),
                    self.state,
                ).values()
            ):
                tspin_corners["back"] += 1

            if tspin_corners["front"] + tspin_corners["back"] >= 3:
                tspin = True

        global tetr
        global tetronimos_choice
        global first_tetronimos
        global bag
        global can_hold
        global down_tick_check

        tetr = Tetronimo(first_tetronimos.pop(0), (4, 0))
        first_tetronimos.append(bag.pop(0))
        if not len(bag):
            bag = tetronimos_choice.copy()
            random.shuffle(bag)

        can_hold = True
        down_tick_check = 1
        self.lock_rotations = 0

    def turn_off_self_on_board(self):
        # Turn off
        for pos in self.states[self.state]:
            board[self.pos[1] + pos[1] + 2][self.pos[0] + pos[0]] = 0

    def hold(self):
        global tetr
        global tetronimos_choice
        global first_tetronimos
        global bag
        global hold
        global can_hold
        global down_tick_check

        if can_hold:
            HOLD.play()
            # Turn off
            for pos in self.states[self.state]:
                board[self.pos[1] + pos[1] + 2][self.pos[0] + pos[0]] = 0

            if not len(hold):
                hold.append(self.id)
                tetr = Tetronimo(first_tetronimos.pop(0), (4, 0))
                first_tetronimos.append(bag.pop(0))
                if not len(bag):
                    bag = tetronimos_choice.copy()
                    random.shuffle(bag)
            else:
                hold.append(self.id)
                tetr = Tetronimo(hold.pop(0), (4, 0))
            can_hold = False

            self.lock_rotations = 0
            down_tick_check = 1

    def update_self(self, new_pos, new_state):
        # Position
        self.old_pos = self.pos
        self.pos = new_pos

        # State
        self.old_state = self.state
        if new_state >= 4:
            self.state = 0
        elif new_state < 0:
            self.state = 3
        else:
            self.state = new_state

        # Update board
        self.toggle_self_on_board()

    def check_collision(self, pos, state):
        output = {"right": False, "left": False, "down": False, "block": False}

        for block in self.states[state]:
            if pos[0] + block[0] >= 10:
                output["right"] = True
            if pos[0] + block[0] < 0:
                output["left"] = True
            if pos[1] + block[1] >= 20:
                output["down"] = True
            try:
                if check := board[pos[1] + block[1] + 2][pos[0] + block[0]]:
                    if check[1] == 0:
                        output["block"] = True
            except:
                pass

        return output

    def movement(self):
        global can_tspin

        cur_time = pygame.time.get_ticks() - time_paused

        if move["left"] and not move["right"]:
            # check time
            if cur_time - MOVE_TIME > self.side_time:
                # move left
                coli = self.check_collision((self.pos[0] - 1, self.pos[1]), self.state)
                if not sum(value == True for value in coli.values()):
                    MOVE.play()
                    self.update_self((self.pos[0] - 1, self.pos[1]), self.state)

                # update time
                self.side_time = cur_time
        elif move["right"] and not move["left"]:
            # check time
            if cur_time - MOVE_TIME > self.side_time:
                # move right
                coli = self.check_collision((self.pos[0] + 1, self.pos[1]), self.state)
                if not sum(value == True for value in coli.values()):
                    MOVE.play()
                    self.update_self((self.pos[0] + 1, self.pos[1]), self.state)

                # update time
                self.side_time = cur_time

        if move["down"]:
            # check time
            if cur_time - move_down_time > self.down_time:
                # move down
                coli = self.check_collision((self.pos[0], self.pos[1] + 1), self.state)
                if not sum(value == True for value in coli.values()):
                    SOFT_DROP.play()

                    self.update_self((self.pos[0], self.pos[1] + 1), self.state)

                    if tetr.id == 5:
                        can_tspin = False

                    global score
                    score += 1

                # update time
                self.down_time = cur_time

        global down_tick_check
        global level

        if 1 <= down_tick_check:
            # move down
            coli = self.check_collision((self.pos[0], self.pos[1] + 1), self.state)
            if not sum(value == True for value in coli.values()):
                self.update_self((self.pos[0], self.pos[1] + 1), self.state)

                if tetr.id == 5:
                    can_tspin = False

            down_tick_check -= 1

        match level:
            case 1:
                down_tick_check += 0.01667
            case 2:
                down_tick_check += 0.021017
            case 3:
                down_tick_check += 0.026977
            case 4:
                down_tick_check += 0.035256
            case 5:
                down_tick_check += 0.04693
            case 6:
                down_tick_check += 0.06361
            case 7:
                down_tick_check += 0.0879
            case 8:
                down_tick_check += 0.1236
            case 9:
                down_tick_check += 0.1775
            case 10:
                down_tick_check += 0.2598
            case 11:
                down_tick_check += 0.388
            case 12:
                down_tick_check += 0.59
            case 13:
                down_tick_check += 0.92
            case 14:
                down_tick_check += 1.46
            case _:
                down_tick_check += 2.36

        if (
            sum(
                value == True
                for value in self.check_collision(
                    (self.pos[0], self.pos[1] + 1), self.state
                ).values()
            )
            and not self.lock_down_timer
        ):
            self.lock_down_timer = True
            self.lock_down_time = pygame.time.get_ticks() - time_paused

        if self.lock_down_timer and self.blink_time + 125 <= (
            pygame.time.get_ticks() - time_paused
        ):
            if self.blinked:
                self.color = (
                    self.color[0] - 25,
                    self.color[1] - 25,
                    self.color[2] - 25,
                )
                self.blinked = False
            else:
                self.color = (
                    self.color[0] + 25,
                    self.color[1] + 25,
                    self.color[2] + 25,
                )
                self.blinked = True
            self.toggle_self_on_board()
            self.blink_time = pygame.time.get_ticks() - time_paused

        if (
            self.lock_down_timer
            and self.lock_down_time + 500 <= (pygame.time.get_ticks() - time_paused)
            and sum(
                value == True
                for value in self.check_collision(
                    (self.pos[0], self.pos[1] + 1), self.state
                ).values()
            )
        ):
            if self.blinked:
                self.color = (
                    self.color[0] - 25,
                    self.color[1] - 25,
                    self.color[2] - 25,
                )
                self.blinked = False
            SOLIDIFY.play()
            self.deactivate_tetronimo()

    def get_down_pos(self):
        down_y = self.pos[1]
        while not sum(
            value == True
            for value in self.check_collision(
                (self.pos[0], down_y), self.state
            ).values()
        ):
            down_y += 1
        else:
            return (self.pos[0], down_y + 1)


tetr = Tetronimo(random.randint(0, 6), (4, 0))


def draw_square(size, pos, color):
    square_surf = pygame.Surface(size)
    square_surf.fill(color)
    surface.blit(square_surf, pos, square_surf.get_rect())


def draw_text(text, pos, color, font):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def draw_ui():
    # Draw background
    surface.fill(COL1)

    # Board
    draw_square((200, 400), (140, 40), COL2)

    # Hold
    global hold
    draw_square((80, 80), (30, 40), COL2)  # background
    draw_text("HOLD", (45, 123), COL2, title)  # Title
    if len(hold):
        hold_display_piece = Tetronimo(hold[0])
        if hold_display_piece.id == 0:
            for off in hold_display_piece.states[0]:
                draw_square(
                    (13, 13),
                    (57 + (off[0] * 13), 75 + (off[1] * 13)),
                    hold_display_piece.color,
                )
        elif hold_display_piece.id == 3:
            for off in hold_display_piece.states[0]:
                draw_square(
                    (13, 13),
                    (57 + (off[0] * 13), 80 + (off[1] * 13)),
                    hold_display_piece.color,
                )
        else:
            for off in hold_display_piece.states[0]:
                draw_square(
                    (13, 13),
                    (63 + (off[0] * 13), 80 + (off[1] * 13)),
                    hold_display_piece.color,
                )

    # Score
    global score
    draw_square((80, 20), (30, 180), COL2)  # background
    draw_text(
        "0" * (9 - len(str(math.floor(score)))) + str(math.floor(score)),
        (33, 184),
        COL1,
        info_font,
    )
    draw_text("SCORE", (30, 203), COL2, title)

    # Lines
    global total_cleared_lines
    draw_square((80, 20), (30, 240), COL2)  # background
    draw_text(
        "0" * (9 - len(str(total_cleared_lines))) + str(total_cleared_lines),
        (33, 244),
        COL1,
        info_font,
    )
    draw_text("LINES", (30, 263), COL2, title)

    # Level
    global level
    draw_square((80, 20), (30, 300), COL2)  # background
    draw_text("0" * (9 - len(str(level))) + str(level), (33, 304), COL1, info_font)
    draw_text("Level", (30, 323), COL2, title)

    # Time
    draw_square((80, 20), (30, 360), COL2)  # Background
    if game_over or paused:
        draw_text(
            "0" * (9 - len(str(math.floor((start_pause_time - time_paused) / 1000))))
            + str(math.floor((start_pause_time - time_paused) / 1000)),
            (33, 364),
            COL1,
            info_font,
        )
    else:
        draw_text(
            "0"
            * (9 - len(str(math.floor((pygame.time.get_ticks() - time_paused) / 1000))))
            + str(math.floor((pygame.time.get_ticks() - time_paused) / 1000)),
            (33, 364),
            COL1,
            info_font,
        )
    draw_text("Time", (30, 383), COL2, title)

    # Next
    global first_tetronimos
    draw_square((80, 80), (370, 40), COL2)  # background
    draw_text("NEXT", (385, 123), COL2, title)  # Title
    hold_display_piece = Tetronimo(first_tetronimos[0])
    if hold_display_piece.id == 0:
        for off in hold_display_piece.states[0]:
            draw_square(
                (13, 13),
                (397 + (off[0] * 13), 75 + (off[1] * 13)),
                hold_display_piece.color,
            )
    elif hold_display_piece.id == 3:
        for off in hold_display_piece.states[0]:
            draw_square(
                (13, 13),
                (397 + (off[0] * 13), 80 + (off[1] * 13)),
                hold_display_piece.color,
            )
    else:
        for off in hold_display_piece.states[0]:
            draw_square(
                (13, 13),
                (403 + (off[0] * 13), 80 + (off[1] * 13)),
                hold_display_piece.color,
            )

    # Draw blocks
    _x = 140
    _y = 40

    down_pos = tetr.get_down_pos()
    for off in tetr.states[tetr.state]:
        # Ghost tetronimo
        draw_square(
            (20, 20),
            (_x + (20 * (down_pos[0] + off[0])), (20 * (down_pos[1] + off[1]))),
            (tetr.color[0] / 1.75, tetr.color[1] / 1.5, tetr.color[2] / 1.25),
        )

    for row in board[2::]:
        for square in row:
            if square:
                # Blocks
                draw_square((20, 20), (_x, _y), COL1)
                draw_square((18, 18), (_x + 1, _y + 1), square[0])
            _x += 20
        _x = 140
        _y += 20

    surface.blit(OLE_JACOB, (WIDTH - 40, HEIGHT - 50), OLE_JACOB.get_rect())


def check_lines():
    global level
    global total_cleared_lines
    global score
    global difficult
    global move_down_time
    global can_tspin
    global tspin

    cleared_lines = 0
    line_moves = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    i = 0
    for line in board[2::]:
        if not line.count(0):
            if not sum(block[1] == 1 or block[1] == 2 for block in line):
                cleared_lines += 1
                # add to line moves
                for line_i in range(20 - i, 20):
                    line_moves[line_i] += 1
        i += 1
    else:
        if cleared_lines:
            total_cleared_lines += cleared_lines
            if math.floor(total_cleared_lines / 10) + 1 > level:
                LEVEL_UP.play()
                level += 1
            move_down_time = 1000 / 20

            if tspin and can_tspin:
                if tspin_corners["front"] == 2:
                    # proper T-spin
                    match cleared_lines:
                        case 1:
                            score += 800 * level * (1 + (0.5 * difficult))
                            difficult = 1
                        case 2:
                            score += 1200 * level * (1 + (0.5 * difficult))
                            difficult = 1
                        case 3:
                            score += 1600 * level * (1 + (0.5 * difficult))
                            difficult = 1
                else:
                    # mini T-spin
                    match cleared_lines:
                        case 1:
                            score += 200 * level * (1 + (0.5 * difficult))
                            difficult = 1
                        case 2:
                            score += 400 * level * (1 + (0.5 * difficult))
                            difficult = 1
                can_tspin = False
                tspin = False
            else:
                match cleared_lines:
                    case 1:
                        score += 100 * level
                        difficult = 0
                    case 2:
                        score += 300 * level
                        difficult = 0
                    case 3:
                        score += 500 * level
                        difficult = 0
                    case 4:
                        score += 800 * level * (1 + (0.5 * difficult))
                        difficult = 1

            # move lines
            tetr.turn_off_self_on_board()
            for i in range(0, 20):
                board[19 - i + line_moves[i] + 2] = board[19 - i + 2]
            for i in range(cleared_lines):
                board[i + 2] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            tetr.toggle_self_on_board()

        elif can_tspin and tspin:
            if tspin_corners["front"] == 2:
                score += 400 * level
            else:
                score += 100 * level
            can_tspin = False
            tspin = False


def game_loop():
    global move
    global can_tspin
    global playing_music

    if not playing_music:
        pygame.mixer.music.unpause()
        playing_music = True

    for event in pygame.event.get():
        if event.type == QUIT:
            global running
            global display
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                move["left"] = True
                tetr.side_time = (pygame.time.get_ticks() - time_paused) - MOVE_TIME

            elif event.key == K_RIGHT:
                move["right"] = True
                tetr.side_time = (pygame.time.get_ticks() - time_paused) - MOVE_TIME

            elif event.key == K_z:
                check_state = tetr.state - 1
                if check_state < 0:
                    check_state = 3

                for i in range(5):
                    if not sum(
                        value == True
                        for value in tetr.check_collision(
                            (
                                tetr.pos[0]
                                + (
                                    tetr.rotation_offset[tetr.state][i][0]
                                    - tetr.rotation_offset[check_state][i][0]
                                ),
                                tetr.pos[1]
                                + (
                                    tetr.rotation_offset[tetr.state][i][1]
                                    - tetr.rotation_offset[check_state][i][1]
                                ),
                            ),
                            check_state,
                        ).values()
                    ):
                        ROTATE.play()

                        tetr.update_self(
                            (
                                tetr.pos[0]
                                + (
                                    tetr.rotation_offset[tetr.state][i][0]
                                    - tetr.rotation_offset[check_state][i][0]
                                ),
                                tetr.pos[1]
                                + (
                                    tetr.rotation_offset[tetr.state][i][1]
                                    - tetr.rotation_offset[check_state][i][1]
                                ),
                            ),
                            check_state,
                        )

                        if tetr.lock_rotations <= 15 and sum(
                            value == True
                            for value in tetr.check_collision(
                                (tetr.pos[0], tetr.pos[1] + 1), tetr.state
                            ).values()
                        ):
                            tetr.lock_down_timer = False
                            if tetr.blinked:
                                tetr.color = (
                                    tetr.color[0] - 25,
                                    tetr.color[1] - 25,
                                    tetr.color[2] - 25,
                                )
                                tetr.blinked = False
                            tetr.toggle_self_on_board()
                            tetr.lock_rotations += 1

                        if tetr.id == 5:
                            can_tspin = True

                        break

            elif event.key == K_x:
                check_state = tetr.state + 1
                if check_state >= 4:
                    check_state = 0

                for i in range(5):
                    if not sum(
                        value == True
                        for value in tetr.check_collision(
                            (
                                tetr.pos[0]
                                + (
                                    tetr.rotation_offset[tetr.state][i][0]
                                    - tetr.rotation_offset[check_state][i][0]
                                ),
                                tetr.pos[1]
                                + (
                                    tetr.rotation_offset[tetr.state][i][1]
                                    - tetr.rotation_offset[check_state][i][1]
                                ),
                            ),
                            check_state,
                        ).values()
                    ):
                        ROTATE.play()

                        tetr.update_self(
                            (
                                tetr.pos[0]
                                + (
                                    tetr.rotation_offset[tetr.state][i][0]
                                    - tetr.rotation_offset[check_state][i][0]
                                ),
                                tetr.pos[1]
                                + (
                                    tetr.rotation_offset[tetr.state][i][1]
                                    - tetr.rotation_offset[check_state][i][1]
                                ),
                            ),
                            check_state,
                        )

                        if tetr.lock_rotations <= 15 and sum(
                            value == True
                            for value in tetr.check_collision(
                                (tetr.pos[0], tetr.pos[1] + 1), tetr.state
                            ).values()
                        ):
                            tetr.lock_down_timer = False
                            if tetr.blinked:
                                tetr.color = (
                                    tetr.color[0] - 25,
                                    tetr.color[1] - 25,
                                    tetr.color[2] - 25,
                                )
                                tetr.blinked = False
                            tetr.toggle_self_on_board()
                            tetr.lock_rotations += 1

                        if tetr.id == 5:
                            can_tspin = True

                        break

            elif event.key == K_DOWN:
                move["down"] = True
                tetr.down_time = (pygame.time.get_ticks() - time_paused) - MOVE_TIME

            elif event.key == K_UP:
                global score
                down_pos = tetr.get_down_pos()

                if tetr.id == 5:
                    can_tspin = False

                score -= tetr.pos[1] - down_pos[1] + 2

                tetr.update_self((down_pos[0], down_pos[1] - 2), tetr.state)
                DROP.play()
                tetr.deactivate_tetronimo()

            elif event.key == K_c:
                tetr.hold()

            elif event.key == K_ESCAPE:
                global start_pause_time
                global paused

                PAUSE.play()

                start_pause_time = pygame.time.get_ticks()
                paused = True

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                move["left"] = False

            elif event.key == K_RIGHT:
                move["right"] = False

            elif event.key == K_DOWN:
                move["down"] = False

    tetr.movement()
    check_lines()
    draw_ui()


def menu_loop():
    for event in pygame.event.get():
        if event.type == QUIT:
            global running
            running = False

    global last_mouse1
    global menu
    global playing_music

    if playing_music:
        pygame.mixer.music.pause()
        playing_music = False

    if pygame.mouse.get_pressed()[0] - last_mouse1 == 1:
        mouse_pos = pygame.mouse.get_pos()

        if (
            mouse_pos[0] >= 315
            and mouse_pos[0] <= 395
            and mouse_pos[1] >= 258
            and mouse_pos[1] <= 298
        ):
            global time_paused
            global score
            global level
            global total_cleared_lines
            global down_tick_check
            global difficult
            global board
            global move
            global hold
            global can_hold
            global bag
            global first_tetronimos
            global tetr

            time_paused = pygame.time.get_ticks()
            score = 0
            level = 1
            total_cleared_lines = 0
            down_tick_check = 1
            difficult = False
            board = []
            for _row in range(22):
                board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            move = {"left": False, "right": False, "down": False}
            hold = []
            can_hold = True
            bag = tetronimos_choice.copy()
            random.shuffle(bag)
            first_tetronimos = [bag.pop(0), bag.pop(1)]

            tetr = Tetronimo(first_tetronimos.pop(0), (4, 0))
            first_tetronimos.append(bag.pop(0))

            BUTTON.play()

            menu = False
        elif (
            mouse_pos[0] >= 315
            and mouse_pos[0] <= 395
            and mouse_pos[1] >= 318
            and mouse_pos[1] <= 358
        ):
            BUTTON.play()
            running = False

    last_mouse1 = pygame.mouse.get_pressed()[0]

    surface.fill(COL1)
    draw_text("TERTIS", (279, 40), COL2, big_title)
    surface.blit(icon, (291, 90), icon.get_rect())

    # Play
    draw_square((80, 40), (315, 258), COL2)
    draw_text("PLAY", (331, 270), COL1, title)

    # quit
    draw_square((80, 40), (315, 318), COL2)
    draw_text("QUIT", (331, 330), COL1, title)

    # Highscores
    draw_square((200, 380), (40, 60), COL2)
    draw_text("HIGHSCORES", (84, 40), COL2, title)

    start_y = 65
    start_x = 45
    for y in range(len(highscores)):
        if y >= 18:
            draw_text(
                str(highscores[y]),
                (start_x + 95, start_y + (21 * (y - 18))),
                COL1,
                info_font,
            )
        elif y < 36:
            draw_text(
                str(highscores[y]), (start_x, start_y + (21 * y)), COL1, info_font
            )
        else:
            break

    surface.blit(OLE_JACOB, (WIDTH - 40, HEIGHT - 50), OLE_JACOB.get_rect())


def pause_loop():
    global time_paused
    global paused
    global menu
    for event in pygame.event.get():
        if event.type == QUIT:
            global running
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                time_paused += pygame.time.get_ticks() - start_pause_time
                paused = False

    global last_mouse1
    global playing_music

    if playing_music:
        pygame.mixer.music.pause()
        playing_music = False

    if pygame.mouse.get_pressed()[0] - last_mouse1 == 1:
        mouse_pos = pygame.mouse.get_pos()

        if (
            mouse_pos[0] >= 195
            and mouse_pos[0] <= 285
            and mouse_pos[1] >= 248
            and mouse_pos[1] <= 288
        ):
            global score
            global level
            global total_cleared_lines
            global down_tick_check
            global difficult
            global board
            global move
            global hold
            global can_hold
            global bag
            global first_tetronimos
            global tetr

            time_paused = pygame.time.get_ticks()
            score = 0
            level = 1
            total_cleared_lines = 0
            down_tick_check = 1
            difficult = False
            board = []
            for _row in range(22):
                board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            move = {"left": False, "right": False, "down": False}
            hold = []
            can_hold = True
            bag = tetronimos_choice.copy()
            random.shuffle(bag)
            first_tetronimos = [bag.pop(0), bag.pop(1)]

            tetr = Tetronimo(first_tetronimos.pop(0), (4, 0))
            first_tetronimos.append(bag.pop(0))

            BUTTON.play()

            paused = False
        elif (
            mouse_pos[0] >= 195
            and mouse_pos[0] <= 285
            and mouse_pos[1] >= 308
            and mouse_pos[1] <= 348
        ):
            time_paused += pygame.time.get_ticks() - start_pause_time

            with open("highscores.csv", "r") as file:
                global highscores
                highscores = file.read().split(";")
                highscores = list(map(lambda x: math.floor(float(x)), highscores))
                highscores.sort(reverse=True)
                print(highscores)

            BUTTON.play()

            paused = False
            menu = True
        elif (
            mouse_pos[0] >= 195
            and mouse_pos[0] <= 285
            and mouse_pos[1] >= 188
            and mouse_pos[1] <= 228
        ):
            time_paused += pygame.time.get_ticks() - start_pause_time
            BUTTON.play()
            paused = False

    last_mouse1 = pygame.mouse.get_pressed()[0]

    draw_ui()

    draw_square((264, 304), (108, 88), COL1)
    draw_square((260, 300), (110, 90), (COL2))
    draw_text("PAUSED", (166, 110), (COL1), big_title)

    draw_square((90, 40), (195, 188), COL1)
    draw_text("RESUME", (204, 200), COL2, title)

    draw_square((90, 40), (195, 248), COL1)
    draw_text("RESTART", (200, 260), COL2, title)

    draw_square((90, 40), (195, 308), COL1)
    draw_text("MN MENU", (198, 320), COL2, title)

    surface.blit(OLE_JACOB, (WIDTH - 40, HEIGHT - 50), OLE_JACOB.get_rect())


def game_over_loop():
    global score
    global level
    global total_cleared_lines
    global down_tick_check
    global difficult
    global board
    global move
    global hold
    global can_hold
    global bag
    global first_tetronimos
    global tetr
    global last_mouse1
    global time_paused
    global game_over
    global menu

    for event in pygame.event.get():
        if event.type == QUIT:
            global running
            running = False

    global playing_music
    if playing_music:
        pygame.mixer.music.pause()
        playing_music = False

    draw_ui()

    draw_square((264, 304), (108, 88), COL1)
    draw_square((260, 300), (110, 90), (COL2))
    draw_text("GAME OVER", (126, 110), (COL1), big_title)

    draw_square((200, 60), (140, 165), COL1)
    draw_text("score : " + str(math.floor(score)), (145, 173), COL2, info_font)  # Score
    draw_text(
        "lines : " + str(total_cleared_lines), (145, 189), COL2, info_font
    )  # Lines cleared
    draw_text(
        "time  : " + str((start_pause_time - time_paused) / 1000),
        (145, 205),
        COL2,
        info_font,
    )  # Time

    draw_square((90, 40), (195, 248), COL1)
    draw_text("RESTART", (200, 260), COL2, title)

    draw_square((90, 40), (195, 308), COL1)
    draw_text("MN MENU", (198, 320), COL2, title)

    if pygame.mouse.get_pressed()[0] - last_mouse1 == 1:
        mouse_pos = pygame.mouse.get_pos()

        if (
            mouse_pos[0] >= 195
            and mouse_pos[0] <= 285
            and mouse_pos[1] >= 308
            and mouse_pos[1] <= 348
        ):
            BUTTON.play()

            time_paused += pygame.time.get_ticks() - start_pause_time

            with open("highscores.csv", "r") as file:
                global highscores
                highscores = file.read().split(";")
                highscores = list(map(lambda x: math.floor(float(x)), highscores))
                highscores.sort(reverse=True)
                print(highscores)

            game_over = False
            menu = True
        elif (
            mouse_pos[0] >= 195
            and mouse_pos[0] <= 285
            and mouse_pos[1] >= 248
            and mouse_pos[1] <= 288
        ):
            BUTTON.play()

            time_paused = pygame.time.get_ticks()
            score = 0
            level = 1
            total_cleared_lines = 0
            down_tick_check = 1
            difficult = False
            board = []
            for _row in range(22):
                board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            move = {"left": False, "right": False, "down": False}
            hold = []
            can_hold = True
            bag = tetronimos_choice.copy()
            random.shuffle(bag)
            first_tetronimos = [bag.pop(0), bag.pop(1)]

            tetr = Tetronimo(first_tetronimos.pop(0), (4, 0))
            first_tetronimos.append(bag.pop(0))

            game_over = False

    last_mouse1 = pygame.mouse.get_pressed()[0]

    surface.blit(OLE_JACOB, (WIDTH - 40, HEIGHT - 50), OLE_JACOB.get_rect())


def main():
    with open("highscores.csv", "r") as file:
        global highscores
        highscores = file.read().split(";")
        highscores = list(map(lambda x: math.floor(float(x)), highscores))
        highscores.sort(reverse=True)
        print(highscores)

    while running:
        if not menu and not paused and not game_over:
            game_loop()
        elif menu:
            menu_loop()
        elif paused:
            pause_loop()
        elif game_over:
            game_over_loop()
        pygame.display.update()
        FramePerSec.tick(FPS)
    else:
        pygame.quit()


if __name__ == "__main__":
    main()
