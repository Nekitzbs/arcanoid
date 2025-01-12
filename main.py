import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Arkanoid")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)

paddle_width = 150
paddle_height = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 50, paddle_width, paddle_height)

ball_radius = 10
initial_ball_speed = 7
balls = [pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
ball_speeds = [[initial_ball_speed, -initial_ball_speed]]

brick_width = 90
brick_height = 30

current_level = 1
max_levels = 20

language = 'EN'

bonuses = []


def get_text(text):
    translations = {
        'EN': {
            'Arkanoid': "Arkanoid",
            'Press Enter to Start': "Press Enter to Start",
            'Paused': "Paused",
            'Level Complete': "Level Complete!",
            'You Win!': "You Win!",
            'Game Over': "Game Over",
            'Settings': "Settings",
            'Change Language': "Change Language",
            'Back': "Back",
            'Restart': "Press Enter to Restart",
            'Exit Game': "Exit Game",
            'Main Menu': "Main Menu"
        },
        'RU': {
            'Arkanoid': "Арканоид",
            'Press Enter to Start': "Нажмите Enter для начала",
            'Paused': "Пауза",
            'Level Complete': "Уровень завершён!",
            'You Win!': "Вы выиграли!",
            'Game Over': "Игра окончена",
            'Settings': "Настройки",
            'Change Language': "Сменить язык",
            'Back': "Назад",
            'Restart': "Нажмите Enter для перезапуска",
            'Exit Game': "Выйти из игры",
            'Main Menu': "Главное меню"
        }
    }
    return translations[language].get(text, text)


def create_bricks(level):
    rows = 3 + level // 2
    columns = 19
    bricks = []
    for j in range(rows):
        for i in range(columns):
            bricks.append(
                pygame.Rect(10 + i * (brick_width + 10), 50 + j * (brick_height + 10), brick_width, brick_height))
    return bricks


bricks = create_bricks(current_level)


def draw_button(text, rect):
    pygame.draw.rect(screen, GREY, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (
    rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))


def show_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(get_text('Arkanoid'), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 200))

    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

    draw_button(get_text('Press Enter to Start'), start_button)
    draw_button(get_text('Settings'), settings_button)
    draw_button(get_text('Exit Game'), exit_button)

    pygame.display.flip()
    return start_button, settings_button, exit_button


def show_pause_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(get_text('Paused'), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 200))

    resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    main_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

    draw_button(get_text('Press Enter to Start'), resume_button)
    draw_button(get_text('Settings'), settings_button)
    draw_button(get_text('Main Menu'), main_menu_button)

    pygame.display.flip()
    return resume_button, settings_button, main_menu_button


def show_level_complete():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(get_text('Level Complete'), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)


def show_game_over():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(get_text('Game Over'), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))
    font = pygame.font.Font(None, 36)
    text = font.render(get_text('Restart'), True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + 20))
    pygame.display.flip()


def settings_menu():
    global language

    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        text = font.render(get_text('Settings'), True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))

        change_language_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 50)
        back_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 50)

        draw_button(f"{get_text('Change Language')}: {language}", change_language_button)
        draw_button(get_text('Back'), back_button)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_language_button.collidepoint(event.pos):
                    language = 'RU' if language == 'EN' else 'EN'
                if back_button.collidepoint(event.pos):
                    return


def reset_game():
    global current_level, bricks, balls, ball_speeds

    current_level = 1
    bricks = create_bricks(current_level)
    balls = [pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
    ball_speeds = [[initial_ball_speed, -initial_ball_speed]]


def spawn_bonus(brick):
    if random.random() < 0.4:
        bonuses.append({'rect': pygame.Rect(brick.x, brick.y, 30, 30), 'type': 'extra_ball'})


def apply_bonus(bonus_type):
    global balls, ball_speeds
    if bonus_type == 'extra_ball':
        for ball in balls[:]:
            new_ball = ball.copy()
            new_speed = random.choice(
                [[initial_ball_speed, initial_ball_speed], [-initial_ball_speed, -initial_ball_speed]])
            balls.append(new_ball)
            ball_speeds.append(new_speed)


def main():
    global current_level, bricks, balls, ball_speeds
    in_menu = True
    paused = False
    game_over = False

    pygame.mouse.set_visible(True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    pygame.mouse.set_visible(paused)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if in_menu:
                    start_button, settings_button, exit_button = show_menu()
                    if start_button.collidepoint(event.pos):
                        in_menu = False
                        pygame.mouse.set_visible(False)
                    elif settings_button.collidepoint(event.pos):
                        settings_menu()
                    elif exit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                elif game_over:
                    reset_game()
                    game_over = False
                    pygame.mouse.set_visible(True)
                elif paused:
                    resume_button, settings_button, main_menu_button = show_pause_menu()
                    if resume_button.collidepoint(event.pos):
                        paused = False
                        pygame.mouse.set_visible(False)
                    elif settings_button.collidepoint(event.pos):
                        settings_menu()
                    elif main_menu_button.collidepoint(event.pos):
                        paused = False
                        in_menu = True
                        pygame.mouse.set_visible(True)

        if in_menu:
            show_menu()
            continue

        if paused:
            show_pause_menu()
            continue

        if game_over:
            show_game_over()
            continue

        mouse_x = pygame.mouse.get_pos()[0]
        paddle.x = mouse_x - paddle_width // 2
        paddle.clamp_ip(screen.get_rect())

        for ball, speed in zip(balls, ball_speeds):
            ball.x += speed[0]
            ball.y += speed[1]

            if ball.left <= 0 or ball.right >= WIDTH:
                speed[0] = -speed[0]
            if ball.top <= 0:
                speed[1] = -speed[1]
            if ball.colliderect(paddle):
                speed[1] = -speed[1]

        for ball in balls:
            hit_index = ball.collidelist(bricks)
            if hit_index != -1:
                hit_rect = bricks.pop(hit_index)
                ball_speeds[balls.index(ball)][1] = -ball_speeds[balls.index(ball)][1]
                spawn_bonus(hit_rect)

        for bonus in bonuses[:]:
            bonus['rect'].y += 5
            if bonus['rect'].colliderect(paddle):
                bonuses.remove(bonus)
                apply_bonus(bonus['type'])
            elif bonus['rect'].top > HEIGHT:
                bonuses.remove(bonus)

        if not bricks:
            current_level += 1
            if current_level > max_levels:
                print(get_text('You Win!'))
                reset_game()
                game_over = True
                pygame.mouse.set_visible(True)
            else:
                show_level_complete()
                bricks = create_bricks(current_level)
                balls = [pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)]
                ball_speeds = [[initial_ball_speed, -initial_ball_speed]]

        balls = [ball for ball in balls if ball.bottom < HEIGHT]
        if not balls:
            game_over = True
            pygame.mouse.set_visible(True)

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        for ball in balls:
            pygame.draw.ellipse(screen, WHITE, ball)
        for brick in bricks:
            pygame.draw.rect(screen, WHITE, brick)
        for bonus in bonuses:
            pygame.draw.rect(screen, (255, 255, 0), bonus['rect'])

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()