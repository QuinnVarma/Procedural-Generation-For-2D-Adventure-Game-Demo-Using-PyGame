import pygame


class Player:
    def __init__(self, pos_x, pos_y):
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.radius = 2
        self.INCREASE_RATE = 1.01
        self.TOTAL_RADIUS = 7.5
        self.NODE_SIZE = 50
    def update(self,dt):
        self.get_input(dt)

    def draw(self,screen):
        pygame.draw.circle(screen, (52, 235, 198), ((self.pos.x * self.NODE_SIZE) + screen.get_width()/2, (self.pos.y * self.NODE_SIZE) + screen.get_height()/2), 2)
        pygame.draw.circle(screen, "green", ((self.pos.x * self.NODE_SIZE) + screen.get_width()/2, (self.pos.y * self.NODE_SIZE) + screen.get_height()/2), self.radius * self.NODE_SIZE, width = 2)
    def get_input(self,dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 1 * dt
        if keys[pygame.K_s]:
            self.pos.y += 1 * dt
        if keys[pygame.K_a]:
            self.pos.x -= 1 * dt
        if keys[pygame.K_d]:
            self.pos.x += 1 * dt

    def increaseRadius(self):
        if self.radius <= self.TOTAL_RADIUS:
            self.radius *= self.INCREASE_RATE
    def __str__(self):
        return f"Player {self.pos.x}, {self.pos.y}"