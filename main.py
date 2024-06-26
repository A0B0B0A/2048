import pygame
import random

# створення музики
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('perfect-beauty.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)

# Зміна розміру вікна та завантаження зображень
WIDTH, HEIGHT = 500, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 90
clock = pygame.time.Clock()
pygame.display.set_caption("2048")
font = pygame.font.Font("arial-unicode-ms.ttf", 30)

# Завантаження зображень та визначення кольорів
setting_img = pygame.image.load('settings_img.jpg')
setting_img = pygame.transform.scale(setting_img, (WIDTH, HEIGHT))

menu_img = pygame.image.load('menu.jpg')
menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))

lose_img = pygame.image.load('lose_img.jpg')
lose_img = pygame.transform.scale(lose_img, (WIDTH, HEIGHT))

win_img = pygame.image.load('win_img.jpg')
win_img = pygame.transform.scale(win_img, (WIDTH, HEIGHT))

loading_img = pygame.image.load('loading_img.jpg')
loading_img = pygame.transform.scale(loading_img, (WIDTH, HEIGHT))

colors = {  # словник кольорів
    0: "#D6D6DA",
    2: "#E5DFD9",
    4: "#ECCEB1",
    8: "#EFBF8F",
    16: "#EEBC8B",
    32: "#F28B0C",
    64: "#EE4C40",
    128: "#EDEB8B",
    256: "#EDEB74",
    512: "#EDEB5A",
    1024: "#F3D65F",
    2048: "#FEFA0A",
    'dark_text': "#8B7066",
    'light_text': "#FFFFFF",
    'background': "#B6B6C0",
    'black': "#000000",
    'light_yellow': '#FFECA1',
    'dark_yellow': '#FFDE59',
    'dark_gray': '#878585',
    'light_red': '#F7807A',
    'white': '#ffffff'
}

# Ініціалізація змінних гри
board_value = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
direction = ""
score = 0
file = open("height_score", "r")
init_height_score = int(file.readline())
file.close()
height_score = init_height_score

# Клас кнопки
class Button:
    def __init__(self, text, position, font, color, text_color, action, width_color):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action
        self.width_color = width_color
        self.label = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.label.get_width() + 20,
                                self.label.get_height() + 20)
        self.visible = True

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
            pygame.draw.rect(screen, self.width_color, self.rect, width=5)
            screen.blit(self.label, (self.position[0] + 10, self.position[1] + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def hide(self, screen):
        self.visible = False

    def show(self, screen):
        self.visible = True


# Функція ініціалізації гри
def init_game():
    global board_value
    global score
    global game_over
    board_value = [[0 for _ in range(4)] for _ in range(4)]
    game_over = False
    score = 0
    new_box(board_value)
    new_box(board_value)


# Функції кнопок
def start_game():
    global screen, game_start
    screen = 'game'
    game_start = True
    init_game()


def go_to_settings():
    global screen
    screen = 'settings'


def restart_game():
    global screen, game_over
    screen = 'game'
    game_over = False
    init_game()


def exit_game():
    global run
    run = False


def music_on_off():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_playing = False
        music_btn.text = "Music Off"
    else:
        pygame.mixer.music.unpause()
        music_playing = True
        music_btn.text = "Music On"
    music_btn.label = music_btn.font.render(music_btn.text, True, music_btn.text_color)


def return_to_menu():
    global screen
    screen = 'menu'

def resume_game():
    global screen
    screen = 'game'
# кнопки
game_start_btn = Button("Start game", (173, 170), font, colors['light_red'], colors["black"], start_game, (152, 245, 249))
settings_btn = Button("Settings", (180, 270), font, colors['light_red'], colors["black"], go_to_settings,(152, 245, 249))
exit_btn = Button("Exit", (210, 370), font, colors['light_red'], colors["black"], exit_game, (152, 245, 249))
music_btn = Button("Music On", (355, 540), font, colors['light_red'], colors["black"], music_on_off,(152, 245, 249))
restart_button = Button("Restart", (120, 450), font, colors['black'], colors["white"], restart_game, (255, 255, 255))
exit_button = Button("Exit", (300, 450), font, colors['black'], colors["white"], exit_game,(255, 255, 255))
menu_button = Button(" \u21A9 ", (0, 0), font, colors['dark_gray'], colors['black'], return_to_menu, (0, 0, 0))
resume_button = Button("Resume", (270, 450), font, colors['black'], colors['white'], resume_game, (255, 255, 255))

# Лист кнопок
buttons_menu = [game_start_btn, settings_btn, exit_btn, music_btn]
buttons_gameover = [restart_button, exit_button]
buttons_win = [menu_button]
buttons_settings = [menu_button]
buttons_pause = [restart_button, resume_button, menu_button]

def draw_board():
    '''фукнція створення рахунків'''
    if game_start:
        window.fill(colors["background"])  # Зміна кольору фону
        # створення та показ рахунків
        score_text = font.render(f'Score: {score}', True, 'black')
        height_score_text = font.render(f'High Score: {height_score}', True, 'black')
        window.blit(score_text, (10, 510))
        window.blit(height_score_text, (10, 550))

def draw_box(board):
    '''функція створення клітинки'''
    if game_start:
        for i in range(4):
            for j in range(4):
                value = board[i][j]
                if value > 8:
                    value_color = colors["light_text"]
                else:
                    value_color = colors["dark_text"]
                if value <= 2048:
                    color = colors[value]
                else:
                    color = colors["black"]
                pygame.draw.rect(window, color, [j * 120 + 20, i * 120 + 20, 100, 100])
                if value > 0:
                    value_len = len(str(value))
                    font = pygame.font.Font('calibri-font-family\calibri-bold.ttf', 60 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j * 120 + 70, i * 120 + 70))
                    window.blit(value_text, text_rect)
                    pygame.draw.rect(window, 'black', [j * 120 + 20, i * 120 + 20, 100, 100], 4, 2)


def new_box(board):
    '''функція створення нових клітинок'''
    count = 0
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count == 1:  # Перевірка, чи з'явився лише один новий квадратик
        return board


def game_over_check(board):
    """функція перевірки програшу"""
    # Перевірка, чи є вільні клітини
    if any(0 in row for row in board):
        return False
    # Перевірка, чи можливі ще які-небудь ходи
    for i in range(4):
        for j in range(4):
            if (i < 3 and board[i][j] == board[i + 1][j]) or \
                    (j < 3 and board[i][j] == board[i][j + 1]):
                return False
    return True


def take_turn(direc, board):
    '''функція руху клітинок, перевірка перемоги а також переписування найвищого рахунку якщо він менший за поточний '''
    global score
    global game_over
    global height_score
    global screen

    merged = [[False for _ in range(4)] for _ in range(4)]

    if direc == "UP":  # рух клітинок в верх
        for j in range(4):
            for i in range(1, 4):
                if board[i][j] != 0:
                    row = i
                    while row > 0 and board[row - 1][j] == 0:
                        row -= 1
                    if row != i:
                        board[row][j] = board[i][j]
                        board[i][j] = 0
                    if row > 0 and board[row - 1][j] == board[row][j] and not merged[row - 1][j]:
                        board[row - 1][j] *= 2
                        score += board[row - 1][j]
                        board[row][j] = 0
                        merged[row - 1][j] = True

    elif direc == "DOWN":  # рух клітинок вниз
        for j in range(4):
            for i in range(2, -1, -1):
                if board[i][j] != 0:
                    row = i
                    while row < 3 and board[row + 1][j] == 0:
                        row += 1
                    if row != i:
                        board[row][j] = board[i][j]
                        board[i][j] = 0
                    if row < 3 and board[row + 1][j] == board[row][j] and not merged[row + 1][j]:
                        board[row + 1][j] *= 2
                        score += board[row + 1][j]
                        board[row][j] = 0
                        merged[row + 1][j] = True

    elif direc == "LEFT":  # рух клітинок в ліво
        for i in range(4):
            for j in range(1, 4):
                if board[i][j] != 0:
                    col = j
                    while col > 0 and board[i][col - 1] == 0:
                        col -= 1
                    if col != j:
                        board[i][col] = board[i][j]
                        board[i][j] = 0
                    if col > 0 and board[i][col - 1] == board[i][col] and not merged[i][col - 1]:
                        board[i][col - 1] *= 2
                        score += board[i][col - 1]
                        board[i][col] = 0
                        merged[i][col - 1] = True

    elif direc == "RIGHT":  # рух клітинок в право
        for i in range(4):
            for j in range(2, -1, -1):
                if board[i][j] != 0:
                    col = j
                    while col < 3 and board[i][col + 1] == 0:
                        col += 1
                    if col != j:
                        board[i][col] = board[i][j]
                        board[i][j] = 0
                    if col < 3 and board[i][col + 1] == board[i][col] and not merged[i][col + 1]:
                        board[i][col + 1] *= 2
                        score += board[i][col + 1]
                        board[i][col] = 0
                        merged[i][col + 1] = True

    if score > height_score:  # перевірка якщо рахунок більший за найвищий рахунок то найвищий рахунок набуває значення поточного рахунку
        height_score = score
        file = open("height_score", "w")
        file.write(f'{height_score}')
        file.close()

    if game_over_check(board):
        game_over = True

    if 2048 in [tile for row in board for tile in
                row]:  # перевірка чи є клітинка з цифрою 2048 і якщо є то зміна екрану на екран win
        screen = 'win'
    return board


screen = 'loading'#змінна яка визначає який екран відмалювати
music_playing = True
game_start = False
run = True
init_game()

while run:
    clock.tick(FPS)

    # запам'ятовуємо позицію миші
    mouse_pos = pygame.mouse.get_pos()


    if screen == 'menu':
        # window.fill(colors["light_yellow"])
        window.blit(menu_img, (0, 0))
        for button in buttons_menu:
            button.draw(window)

    elif screen == 'game':
        draw_board()
        draw_box(board_value)
        music_btn.draw(window)
        if direction:
            board_value = take_turn(direction, board_value)
            new_box(board_value)
            direction = ""

    elif screen == 'gameover':
        # window.fill('#E8E8E8')
        window.blit(lose_img, (0, 0))
        for button in buttons_gameover:
            button.draw(window)

    elif screen == 'win':
        # window.fill('#E8E8E8')
        window.blit(win_img, (0, 0))
        font_win = pygame.font.Font('calibri-font-family\calibri-bold.ttf', 50)
        winning_text = font_win.render("You Win!", True, 'black')
        window.blit(winning_text, (150, 250))
        for button in buttons_win:
            button.draw(window)

    elif screen == 'pause':
        window.fill(colors['black'])
        font_pause = pygame.font.Font('calibri-font-family\calibri-bold.ttf', 75)
        pause_text = font_pause.render("Pause", True, 'white')
        window.blit(pause_text, (150, 250))
        for button in buttons_pause:
            button.draw(window)

    if game_over_check(board_value):
        screen = 'gameover'


    elif screen == 'settings':
        window.blit(setting_img, (0, 0))
        font_text = pygame.font.Font('calibri-font-family\calibri-bold.ttf', 25)
        text1 = font_text.render("Use \u2192, \u2190, \u2191, \u2193 to move. ", True, 'black')
        text2 = font_text.render("Use button 'music' to turn on or off music. ", True, 'black')
        text3 = font_text.render("Use 'x' to leave. ", True, 'black')
        text4 = font_text.render("Use ESC to pause game. ", True, 'black')
        window.blit(text1, (75, 35))
        window.blit(text2, (25, 75))
        window.blit(text3, (140, 155))
        window.blit(text4, (120, 115))
        for button in buttons_settings:
            button.draw(window)

    elif screen == 'loading':
        window.blit(loading_img, (0, 0))
        font_loading = pygame.font.Font('calibri-font-family\calibri-bold.ttf', 50)
        loading_text = font_loading.render("Click anywhere to start. ", True, 'black')
        window.blit(loading_text, (10, 525))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if screen == 'menu':
                run = False
            if screen == 'gameover':
                run = False
            else:
                screen = 'menu'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if screen == 'menu':
                for button in buttons_menu:
                    if button.is_clicked(mouse_pos):
                        button.action()

            elif screen == 'gameover':
                for button in buttons_gameover:
                    if button.is_clicked(mouse_pos):
                        button.action()
                if menu_button.is_clicked(mouse_pos):
                    menu_button.action()

            elif screen == 'game':
                if music_btn.is_clicked(mouse_pos):
                    music_btn.action()

            elif screen == 'win':
                for button in buttons_win:
                    if button.is_clicked(mouse_pos):
                        button.action()

            elif screen == 'settings':
                for button in buttons_settings:
                    if button.is_clicked(mouse_pos):
                        button.action()

            elif screen == 'loading':
                screen = 'menu'

            elif screen == 'pause':
                for button in buttons_pause:
                    if button.is_clicked(mouse_pos):
                        button.action()

        elif event.type == pygame.KEYDOWN:
            if screen == 'game':
                if event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    screen = 'pause'

    pygame.display.update()

pygame.quit()