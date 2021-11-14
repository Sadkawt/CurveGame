import pygame
import math

class ScoreBoard:
    def __init__(self, name_list):
        self.player_list = []

        #skapar en lista med namn och score
        for name in name_list:
            self.player_list.append([name.name,0])

        self.player_list_next = self.player_list

    def update_score(self, placement_list):
        for placement, name in enumerate(placement_list):
            for x in range(len(self.player_list)):
                if self.player_list[x][0] == name:
                    self.player_list[x][1] += math.ceil(10/(placement+1))

    def sort(self):
        self.player_list.sort(key = lambda x: x[1], reverse=True)

    def render(self, screen):
        pygame.init()
        SCORE_FONT = pygame.font.SysFont("Comic Sans MS", 20)
        for index, player in enumerate(self.player_list):
            score = SCORE_FONT.render(str(player[0]) +": " + str(player[1]), False, (255, 255, 255))
            screen.blit(score, (0, index*40))
