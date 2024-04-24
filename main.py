import pygame
import random


pygame.init()

# pygame.mixer.init()
# pygame.mixer.music.load('')
# pygame.mixer.music.play()
# pygame.mixer.music.set_volume(0.3)

WIDTH, HEIGHT = 500, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 90
clock = pygame.time.Clock()
pygame.display.set_caption("2048")
font = pygame.font.Font('freesansbold.ttf', 30) 

colors = {0: ("#D6D6DA"),
          2:   ("#E5DFD9"),
          4:   ("#ECCEB1"),
          8:   ("#EFBF8F"),
          16:  ("#EEBC8B"),
          32:  ("#F28B0C"),
          64:  ("#EE4C40"),
          128: ("#EDEB8B"),
          256: ("#EDEB74"),
          512: ("#EDEB5A"),
          1024:("#F3D65F"),
          2048:("#FEFA0A"),
          'dark_text': ("#8B7066"),
          'light_text': ("#FFFFFF"),
          'background': ("#B6B6C0"),
          'black': ("#000000")
}

board_value = [[0 for _ in range (4)]for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ""
score = 0 
file = open("hight_score", "r")
init_hight_score = int(file.readline())
file.close()
hight_score = init_hight_score


def draw_over():
    pygame.draw.rect(window, "#000000", [50, 50, 300, 100], 0 , 10)
    game_over_text1 = font.render("Game Over!", True, "#ffffff")
    game_over_text2 = font.render("Press ENTER to restart!", True, "#ffffff")
    window.blit(game_over_text1, (130, 65))
    window.blit(game_over_text2, (70, 105))

def take_turn(direc, board):
    global score
    merged = [[False for _ in range (4)] for _ in range(4)]
    
    if direc == "UP":
        for i in range(4):
            for j in range (4):
                shift = 0
                if i > 0:
                    for q in range(i):# перевіряємо скільки рядків треба перевіряти
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0 
                    if board[i -shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

 
    elif direc == "DOWN":
        for i in range(3):
            for j in range(4):
                shift  = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]                     
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True


    elif direc == "LEFT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True 


    elif direc == "RIGHT":
        for i in range(4):
            for j in range(4):
                shift = 0 
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] == board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift] 
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True

    return board  


def new_box(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count  < 1:
        row = random.randint(0,3)
        col = random.randint(0,3)
        if board [row][col] == 0:
            count += 1
            if random.randint(1,10) == 10:
                board [row][col] = 4 
            else:
                board [row][col] = 2
    if count < 1:
        full = True
    return board, full

def draw_board():
    pygame.draw.rect(window, colors["background"], [0,0,500,500], 0, 10)# колір, розмір, товщина, заукруглення
    score_text = font.render(f'Score: {score}', True, 'black')
    hight_score_text = font.render(f'Hight score: {hight_score}', True, 'black')
    window.blit(score_text, (10, 510))
    window.blit(hight_score_text, (10, 550))


def draw_box(board):
    for i in range(4):
        for j in range (4):
            value = board [i][j] #цифра
            if value > 8:
                value_color = colors["light_text"]
            else:
                value_color = colors["dark_text"]
            if value <= 2048:
                color = colors[value]
            else:
                color = colors["black"]
            pygame.draw.rect(window, color, [j * 120 + 20, i * 120  + 20, 100, 100])
            if value > 0:
                value_len = len(str(value))# довжина цифри
                font = pygame.font.Font('freesansbold.ttf', 60 - ( 5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center = (j *120 + 70, i * 120 + 70))
                window.blit(value_text, text_rect)
                pygame.draw.rect(window, 'black', [j * 120 + 20, i * 120  + 20, 100, 100],4,2)


run = True
while run:
    clock.tick(FPS)
    window.fill("#CECECE")

    draw_board()
    draw_box(board_value)

    if spawn_new or init_count < 2:
        board_value, game_over = new_box(board_value)
        spawn_new = False
        init_count += 1
    if direction != "":
        board_value = take_turn(direction, board_value)
        direction = ""
        spawn_new = True
        if game_over:
            draw_over()
            if hight_score > init_hight_score:
                file = open("hight_score", "w")
                file.write(f'{hight_score}')
                file.close()
                init_hight_score = hight_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            elif event.key == pygame.K_LEFT:
                direction = "LEFT"
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_value = [[0 for _ in range(4)]for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ""
                    game_over = False

    if score > hight_score:
        hight_score = score

    pygame.display.flip()