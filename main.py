import pygame
import random
from enum import Enum
from collections import namedtuple
from components.direction import Direction
from components import settings as st

pygame.init()
font = pygame.font.Font('./resources/arial.ttf', 25)


    
Point = namedtuple('Point', 'x, y')


class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-st.BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*st.BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-st.BLOCK_SIZE )//st.BLOCK_SIZE )*st.BLOCK_SIZE 
        y = random.randint(0, (self.h-st.BLOCK_SIZE )//st.BLOCK_SIZE )*st.BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(st.SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - st.BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - st.BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(st.BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, st.BLUE1, pygame.Rect(pt.x, pt.y, st.BLOCK_SIZE, st.BLOCK_SIZE))
            pygame.draw.rect(self.display,st.BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, st.RED, pygame.Rect(self.food.x, self.food.y, st.BLOCK_SIZE, st.BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, st.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += st.BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= st.BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += st.BLOCK_SIZE
        elif direction == Direction.UP:
            y -= st.BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()