import pygame

class Ball:
  def __init__(self,x,y,radius,speed):
    self.x = x
    self.y = y
    self.radius = radius
    self.speed = speed
    
  def move(self,keys,width,height):
    if keys == pygame.K_LEFT:
      self.x -= self.speed
    if keys == pygame.K_RIGHT:
      self.x += self.speed
    if keys == pygame.K_UP :
      self.y -= self.speed
    if keys == pygame.K_DOWN:
      self.y += self.speed
      
    # Ограничение (чтобы не выходил за экран)
    self.x = max(self.radius, min(self.x, width - self.radius))
    self.y = max(self.radius, min(self.y, height - self.radius))
      
      
  def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)