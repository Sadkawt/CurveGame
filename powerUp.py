import math
import random
import pygame

from Snake import circle_v_circle_collision

class PowerUp_manager:
    def __init__(self):
        self.powerUp_list = []
        self.active_powerUp_list = []
        self.itter = 0

    def update_seed(self):
        comparison = random.uniform(0, 1)
        seed = 1.001**self.itter - 1

        if seed > comparison:
            self.powerUp_list.append(PowerUp())
            self.itter = 0

        else:
            self.itter += 1

    def check_pick_up(self, snake_obj):
        snake_circle = snake_obj.get_snake_circle()
        for index, powerUp in enumerate(self.powerUp_list):
            #collision detection works since powerUp has the same attributes as a circle class
            if circle_v_circle_collision(snake_circle, powerUp):
                # Removes powerup from list for future rendering
                if powerUp.type == "grow":
                    powerUp_obj = Grow(snake_obj)

                elif powerUp.type == "shrink":
                    powerUp_obj = Shrink(snake_obj)

                elif powerUp.type == "accelerator":
                    powerUp_obj = Accelerator(snake_obj)

                elif powerUp.type == "retarder":
                    powerUp_obj = Retarder(snake_obj)

                elif powerUp.type == "clear":
                    powerUp_obj = Clear(snake_obj)

                self.active_powerUp_list.append(powerUp_obj)
                self.powerUp_list.pop(index)

    def update_powerUps(self):
        for index, powerUp_obj in enumerate(self.active_powerUp_list):
            powerUp_obj.update()

            if pygame.time.get_ticks() - powerUp_obj.start_time > powerUp_obj.end_time:
                powerUp_obj.revert()
                self.active_powerUp_list.pop(index)

    def render(self, screen):
        for powerUp in self.powerUp_list:
            powerUp.render(screen)


class PowerUp:
    def __init__(self):
        width, height = pygame.display.get_surface().get_size()

        self.x = random.randrange(50, width - 50)
        self.y = random.randrange(50, height - 50)

        self.radius = 10

        self.type = random.choice(["grow", "shrink", "accelerator", "retarder", "clear"])

        if self.type == "grow":
            self.color = (255,255,0)

        elif self.type == "shrink":
            self.color = (0,255,0)

        elif self.type == "accelerator":
            self.color = (0,0,255)

        elif self.type == "retarder":
            self.color = (255,0,0)

        elif self.type == "clear":
            self.color = (255,255,255)

    def render(self, screen):
        pygame.init()
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, self.radius, self.color)

class Grow:
    def __init__(self, snake_obj):
        self.snake = snake_obj
        self.snake.resize(2)
        self.start_time = pygame.time.get_ticks()
        self.end_time = 7000

        # Updates the snakes body so that it doesnt get warped
        self.snake.get_new_points()

    def update(self):
        pass

    def revert(self):
        self.snake.resize(-2)

class Shrink:
    def __init__(self, snake_obj):
        self.snake = snake_obj
        self.snake.resize(-2)
        self.start_time = pygame.time.get_ticks()
        self.end_time = 7000

        # Updates the snakes body so that it doesnt get warped
        self.snake.get_new_points()

    def update(self):
        pass

    def revert(self):
        self.snake.resize(2)

class Accelerator:
    def __init__(self, snake_obj):
        self.snake = snake_obj
        self.start_time = pygame.time.get_ticks()
        self.end_time = 3000

        # Updates the snakes body so that it doesnt get warped
        self.snake.get_new_points()

    def update(self):
        self.snake.velocity += 0.01
        self.snake.update_ball_time()

    def revert(self):
        pass

class Retarder:
    def __init__(self, snake_obj):
        self.snake = snake_obj
        self.start_time = pygame.time.get_ticks()
        self.end_time = 3000
    def update(self):
        if self.snake.velocity > 0.2:
            self.snake.velocity -= 0.01
            self.snake.update_ball_time()

    def revert(self):
        pass

class Clear:
    def __init__(self, snake_obj):
        snake_obj.circle_list = []

        snake_obj.polygon_list = [[(snake_obj.x + snake_obj.thickness*math.sin(snake_obj.angle + math.pi/2), snake_obj.y + snake_obj.thickness*math.cos(snake_obj.angle + math.pi/2)), (snake_obj.x + snake_obj.thickness*math.sin(snake_obj.angle - math.pi/2), snake_obj.y + snake_obj.thickness*math.cos(snake_obj.angle - math.pi/2)), (snake_obj.x + snake_obj.thickness*math.sin(snake_obj.angle + math.pi/2), snake_obj.y + snake_obj.thickness*math.cos(snake_obj.angle + math.pi/2)), (snake_obj.x + snake_obj.thickness*math.sin(snake_obj.angle - math.pi/2), snake_obj.y + snake_obj.thickness*math.cos(snake_obj.angle - math.pi/2))]]

        self.start_time = pygame.time.get_ticks()
        self.end_time = 0

    def update(self):
        pass

    def revert(self):
        pass
