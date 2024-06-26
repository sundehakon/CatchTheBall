import pygame
import random
import math

pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catch the Ball!")

GAME_RUNNING = 0
GAME_OVER = 1
GAME_WON = 2
GAME_START = 3
game_state = GAME_START

center_x = size[0] // 2
rect_width = 90
rect_height = 20
speed = 80
fallSpeed = 6
points = 0

font = pygame.font.Font(None, 36)

bg = pygame.image.load("background.png")

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def fall(self):
        self.y += fallSpeed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

circles = []

clock = pygame.time.Clock()

def is_collision(circle, rect):
    rect_x, rect_y, rect_width, rect_height = rect
    nearest_x = max(rect_x, min(circle.x, rect_x + rect_width))
    nearest_y = max(rect_y, min(circle.y, rect_y + rect_height))
    distance = math.sqrt((circle.x - nearest_x) ** 2 + (circle.y - nearest_y) ** 2)
    return distance < circle.radius

while True:
    if game_state == GAME_RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = GAME_OVER

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    center_x -= speed
                if event.key == pygame.K_RIGHT:
                    center_x += speed

                if center_x < 0:
                    center_x = 0
                if center_x > size[0] - rect_width:
                    center_x = size[0] - rect_width
                    
        if random.randint(1, 30) == 1:  
            x = random.randint(0, size[0])
            new_circle = Circle(x, 0, 30, (0, 0, 255))  
            circles.append(new_circle)
        
        for circle in circles:
            circle.fall()
            if circle.y > size[1] and not is_collision(circle, (center_x, 550, rect_width, rect_height)):
                points -= 1 

        new_circles = []
        for circle in circles:
            if is_collision(circle, (center_x, 550, rect_width, rect_height)):
                points += 5
            else:
                new_circles.append(circle)
        circles = new_circles
        
        circles = [circle for circle in circles if circle.y < size[1] + circle.radius]

        screen.fill((255, 255, 255))

        screen.blit(bg, (0, 0))

        pygame.draw.rect(screen, (255, 0, 0), (center_x, 550, rect_width, rect_height), border_radius=4)

        for circle in circles:
            circle.draw(screen)

        points_text = font.render(f"Points: {points}", True, (0, 0, 0))
        screen.blit(points_text, (10, 10))

        if points >= 50:
            game_state = GAME_WON

        if points <= -50:
            game_state = GAME_OVER

        pygame.display.flip()

        clock.tick(60)

    elif game_state == GAME_START:
        screen.fill((255, 255, 255))
        title_text = font.render("Catch The Ball!", True, (0, 0, 0))
        screen.blit(title_text, (size[0] // 2 - 70, size[1] // 2 - 20))
        start_text = font.render("Press any key to start", True, (0, 0, 0))
        screen.blit(start_text, (size[0] // 2 - 110, size[1] // 2 + 20))
        pygame.display.flip()

        start = True
        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    game_state = GAME_RUNNING
                    start = False

    elif game_state == GAME_WON:
        screen.fill((255, 255, 255))
        win_text = font.render("You Win!", True, (0, 0, 0))
        screen.blit(win_text, (size[0] // 2 - 70, size[1] // 2 - 20))
        restart_text = font.render("Press R to restart", True, (0, 0, 0))
        screen.blit(restart_text, (size[0] // 2 - 110, size[1] // 2 + 20))
        pygame.display.flip()

        restart = True
        while restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        points = 0
                        circles = []
                        game_state = GAME_RUNNING
                        restart = False

    elif game_state == GAME_OVER:
        screen.fill((255, 255, 255))
        win_text = font.render("You Lose!", True, (0, 0, 0))
        screen.blit(win_text, (size[0] // 2 - 70, size[1] // 2 - 20))
        restart_text = font.render("Press R to restart", True, (0, 0, 0))
        screen.blit(restart_text, (size[0] // 2 - 110, size[1] // 2 + 20))
        pygame.display.flip()

        restart = True
        while restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        points = 0
                        circles = []
                        game_state = GAME_RUNNING
                        restart = False

pygame.quit()
