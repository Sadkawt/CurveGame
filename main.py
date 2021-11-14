import pygame
from pygame import gfxdraw, freetype
import random
import math
import time

from Snake import *
from ScoreBoard import *
from powerUp import *

class Player:
    def __init__(self, name, controlls):
        self.name = name
        self.controlls = controlls
        color1 = random.randrange(70,255)
        color2 = random.randrange(70,255)
        color3 = random.randrange(70,255)
        self.color = (color1, color2, color3)

def display_winner(screen, winner_name):
    WINNER_FONT = pygame.font.SysFont("Comic Sans MS", 50)
    title = WINNER_FONT.render("WINNER: " + winner_name, False, (255, 255, 255))
    screen.blit(title, (150, 250))

def check_intersection(snake_obj, circle_list_list):
    snake_circle = snake_obj.get_snake_circle()
    current_snakes_list = snake_obj.get_circle_list()
    for circle_list in circle_list_list:
        if current_snakes_list == circle_list:
            for x in range(len(circle_list)-5):
                if circle_v_circle_collision(snake_circle, circle_list[x]) == True:
                    return True
        else:
            for x in range(len(circle_list)):
                if circle_v_circle_collision(snake_circle, circle_list[x]) == True:
                    return True

    return False

def start_screen(screen):
    running = True
    pygame.init()

    GAME_FONT = pygame.font.SysFont("Comic Sans MS", 60)
    INFO_FONT = pygame.font.SysFont("Comic Sans MS", 20)
    PLAYER_FONT = pygame.font.SysFont("Comic Sans MS", 20)
    title = GAME_FONT.render('JAG KNULLADE DIN MAMMA', False, (155, 122, 147))
    infoText = INFO_FONT.render("Tryck på Space för att lägga till spelare eller backspace för att ta bort spelare",False, (255, 255, 255))

    player_list = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_list) != 0:
                    score_board = ScoreBoard(player_list)
                    start_game(screen, player_list, score_board)

                if event.key == pygame.K_RETURN:
                    tempName = name_setup(screen)
                    tempControl = control_setup(screen)
                    player_list.append(Player(tempName, tempControl))

                elif event.key == pygame.K_BACKSPACE and len(player_list) != 0:
                    player_list.pop()


        screen.fill((104, 151, 147))
        #***************__UPDATE__***************#
        for player in player_list:
            screen.blit(PLAYER_FONT.render(player.name, False, (255, 255, 255)), (100, 200 + 30*player_list.index(player)))


        #***************__DRAW__***************#
        screen.blit(title,(20,20))
        screen.blit(infoText, (20,100))

        pygame.display.flip()

def name_setup(screen):
    pygame.init()
    player_name = ""
    NAME_FONT = pygame.font.SysFont("Comic Sans MS", 20)
    INFO_FONT = pygame.font.SysFont("Comic Sans MS", 50)
    nameText = NAME_FONT.render(player_name, False, (155, 122, 147))
    infoText = INFO_FONT.render("spelar namn: ", False, (155, 122, 147))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(player_name) != 0:
                        player_name = player_name[:-1]
                        nameText = NAME_FONT.render(player_name, False, (255, 255, 255))
                elif event.key == pygame.K_RETURN:
                    return player_name

                elif event.key == pygame.K_SPACE:
                    player_name += " "
                    nameText = NAME_FONT.render(player_name, False, (255, 255, 255))

                else:
                    player_name += pygame.key.name(event.key)
                    nameText = NAME_FONT.render(player_name, False, (255, 255, 255))

        screen.fill((104, 151, 147))
        screen.blit(infoText, (100, 270))
        screen.blit(nameText, (420, 300))
        pygame.display.flip()

def control_setup(screen):
    pygame.init()
    #Used for controlling
    player_control = [None, None]
    #Used for drawing
    player_control_string = ["", ""]

    INFO_FONT = pygame.font.SysFont("Comic Sans MS", 30)
    CONTROL_FONT = pygame.font.SysFont("Comic Sans MS", 30)
    info_text = INFO_FONT.render("Välj dina kontroller: ", False, (255, 255, 255))
    control_text = CONTROL_FONT.render(player_control_string[0] + " and " + player_control_string[1], False, (255, 255, 255))

    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_control[0] != None and player_control[1] != None:
                    return player_control
                # Doesn't update if user tries to input same input for two buttons
                elif event.key != player_control[0] and event.key != player_control[1] and event.key != pygame.K_RETURN:
                    player_control[counter] = event.key
                    player_control_string[counter] = pygame.key.name(event.key)

                    if counter == 1:
                        counter -=1
                    else:
                        counter +=1
                    control_text = CONTROL_FONT.render(player_control_string[0] + " and " + player_control_string[1], False, (255, 255, 255))

        screen.fill((104, 151, 147))
        screen.blit(info_text, (300,200))
        screen.blit(control_text, (400,300))
        pygame.display.flip()

def start_game(screen, player_list, score_board):
    pygame.init()
    clock = pygame.time.Clock()
    circleTimer = 0

    placement_list = []
    live_snake_list = []
    dead_snake_list = []

    game_is_over = False

    powerUp_manager = PowerUp_manager()

    for player in player_list:
        live_snake_list.append(Snake(player.name, player.controlls, random.randrange(200, 700),random.randrange(200, 400), random.randrange(0, 360), player.color))

    screen.fill((0,0,0))
    for snake in live_snake_list:
        snake.render(screen)
        snake.render_dir_vector(screen)
    score_board.render(screen)
    pygame.display.flip()

    time.sleep(2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    score_board.update_score(placement_list)
                    score_board.sort()
                    start_game(screen, player_list, score_board)

                for snake in live_snake_list:
                    if event.key == snake.controlls[0]:
                        snake.set_moving(1)
                    elif event.key == snake.controlls[1]:
                        snake.set_moving(-1)

            elif event.type == pygame.KEYUP:
                for snake in live_snake_list:
                    if event.key in snake.controlls:
                        snake.set_moving(0)

        screen.fill((0,0,0))

        circle_list_list = []

        for snake in live_snake_list:
            snake.update_position()

            snake.check_place_circle()
            snake.render(screen)

            powerUp_manager.check_pick_up(snake)

            circle_list_list.append(snake.get_circle_list())
            if snake.check_out_of_bounds_kill(screen) == True:
                placement_list.insert(0,snake.name)
                dead_snake_list.append(live_snake_list.pop(live_snake_list.index(snake)))
                if len(live_snake_list) == 1:
                    placement_list.insert(0,live_snake_list[0].name)
                    winner_name = live_snake_list[0].name
                    game_is_over = True
                    dead_snake_list.append(live_snake_list.pop(0))


        for snake in dead_snake_list:
            snake.render(screen)
            circle_list_list.append(snake.get_circle_list())

        for snake in live_snake_list:
            if check_intersection(snake, circle_list_list) == True:
                placement_list.insert(0,snake.name)
                dead_snake_list.append(live_snake_list.pop(live_snake_list.index(snake)))
                if len(live_snake_list) == 1:
                    placement_list.insert(0,live_snake_list[0].name)
                    winner_name = live_snake_list[0].name
                    game_is_over = True
                    dead_snake_list.append(live_snake_list.pop(0))

        score_board.render(screen)
        powerUp_manager.render(screen)

        if game_is_over:
            display_winner(screen, winner_name)

        else:
            powerUp_manager.update_seed()
            powerUp_manager.update_powerUps()

        pygame.display.flip()

        clock.tick(60)




def main():

    running = True

    pygame.init()

    size = (1500, 1000)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Curve Game")
    start_screen(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
