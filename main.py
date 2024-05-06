import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('perfect-beauty.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)

WIDTH, HEIGHT = 500, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 90
clock = pygame.time.Clock()
pygame.display.set_caption("2048")
font = pygame.font.Font('freesansbold.ttf', 30)

colors = {
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
    'black': "#000000"
}

board_value = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
direction = ""
score = 0
file = open("height_score", "r")
init_height_score = int(file.readline())
file.close()
height_score = init_height_score

black = '#000000'
light_yellow = '#FFECA1'
dark_yellow = '#FFDE59'

class Button:
    def __init__(self, text, position, font, color, text_color, action):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action
        self.label = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.label.get_width() + 20, self.label.get_height() + 20)
        self.visible = True

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.label, (self.position[0] + 10, self.position[1] + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def hide(self, screen):
        self.visible = False

    def show(self, screen):
        self.visible = True


def action1():
    global screen, game_start
    screen = 'game'
    game_start = True
    init_game()

def action2():
    print("Вибрано кнопку 2")

def action3():
    global run
    run = False

def restart_game():
    init_game()

def exit_game():
    global run
    run = False

def music_on_off():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()
        music_playing = False
        button4.text = "Music Off"
    else:
        pygame.mixer.music.unpause()
        music_playing = True
        button4.text = "Music On"
    button4.label = button4.font.render(button4.text, True, button4.text_color)

button1 = Button("Start game", (173, 170), font, dark_yellow, black, action1)
button2 = Button("Settings", (180, 270), font, dark_yellow, black, action2)
button3 = Button("Exit", (210, 370), font, dark_yellow, black, action3)
button4 = Button("Music On", (350, 550), font, dark_yellow, black, music_on_off)
restart_button = Button("Restart", (150, 320), font, dark_yellow, black, restart_game)
exit_button = Button("Exit", (300, 320), font, dark_yellow, black, exit_game)

buttons = [button1, button2, button3, button4]

def draw_board():
    if game_start:
        pygame.draw.rect(window, colors["background"], [0,0,500,500], 0, 10)
        score_text = font.render(f'Score: {score}', True, 'black')
        height_score_text = font.render(f'High Score: {height_score}', True, 'black')
        window.blit(score_text, (10, 510))
        window.blit(height_score_text, (10, 550))

def draw_box(board):
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
                    font = pygame.font.Font('freesansbold.ttf', 60 - (5 * value_len))
                    value_text = font.render(str(value), True, value_color)
                    text_rect = value_text.get_rect(center=(j *120 + 70, i * 120 + 70))
                    window.blit(value_text, text_rect)
                    pygame.draw.rect(window, 'black', [j * 120 + 20, i * 120 + 20, 100, 100], 4, 2)

def new_box(board):
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
    global score
    global game_over
    global height_score 
    
    merged = [[False for _ in range(4)] for _ in range(4)]

    if direc == "UP":
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
 
    elif direc == "DOWN":
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

    elif direc == "LEFT":
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

    elif direc == "RIGHT":
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
    if score > height_score:
        height_score = score
        file = open("height_score", "w")
        file.write(f'{height_score}')
        file.close()
    if game_over_check(board):
        game_over = True
    return board

def init_game():
    global board_value, score, game_over
    board_value = [[0 for _ in range(4)] for _ in range(4)]
    game_over = False
    score = 0
    new_box(board_value)


screen = 'menu'
music_playing = True
game_start = False
game_over = False
run = True
init_game()


while run:
    clock.tick(FPS)

    mouse_pos = pygame.mouse.get_pos()

    if screen == 'menu':
        window.fill(light_yellow)
        for button in buttons:
            button.draw(window)

    elif screen == 'game':
        draw_board()
        draw_box(board_value)
        for button in buttons:
            if button4.is_clicked(mouse_pos):
                button4.action()
                button4.draw(window)
        if direction:
            board_value = take_turn(direction, board_value)
            new_box(board_value)
            direction = ""
    elif screen == 'gameover':
        window.fill('#E8E8E8')
        # Вивід повідомлення про програш
        font_game_over = pygame.font.Font('freesansbold.ttf', 40)
        game_over_text = font_game_over.render("Game Over!", True, 'black')
        window.blit(game_over_text, (150, 250))
        # Показуємо або приховуємо кнопки "Restart" і "Exit" залежно від статусу гри
        restart_button.draw(window)
        exit_button.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if screen == 'menu':
                run = False
            else:
                screen = 'menu'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if screen == 'menu':
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        button.action()
            elif screen == 'gameover':
                if restart_button.is_clicked(mouse_pos):
                    restart_button.action()
                elif exit_button.is_clicked(mouse_pos):
                    exit_button.action()
            elif screen == 'game':
                if button4.is_clicked(mouse_pos):
                    button4.action()
        elif event.type == pygame.KEYDOWN:
            if screen == 'game':
                if event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"

    if game_over:
        screen = 'gameover'

    pygame.display.flip()