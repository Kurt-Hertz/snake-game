import pygame
import random
from enum import Enum
from collections import namedtuple


pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIHGT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y') 

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


BlOCK_SIZE = 20
SPEED = 20

class SnakeGame:

    def __init__(self, w = 640, h = 480) :
        self.w = w
        self.h = h

        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()


        #init game loop
        self.direction = Direction.RIHGT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BlOCK_SIZE, self.head.y), 
                      Point(self.head.x-(2*BlOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BlOCK_SIZE) // BlOCK_SIZE) * BlOCK_SIZE
        y = random.randint(0, (self.h-BlOCK_SIZE) // BlOCK_SIZE) * BlOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake :
            self._place_food()


    def play_step(self) :
        #collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIHGT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        #check game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        #new food / forward
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        #update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        #return game over and score
        game_over = False
        return game_over, self.score

    def _is_collision(self):
        #hit bound
        if self.head.x > self.w - BlOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BlOCK_SIZE or self.head.y < 0:
            return True
        #his body
        if self.head in self.snake[1:]:
            return True
        
        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BlOCK_SIZE, BlOCK_SIZE ))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12 ))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BlOCK_SIZE, BlOCK_SIZE ))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIHGT:
            x += BlOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BlOCK_SIZE
        elif direction == Direction.DOWN:
            y += BlOCK_SIZE
        elif direction == Direction.UP:
            y -= BlOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__' :
    game = SnakeGame()

    #game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    
    pygame.quit()
    