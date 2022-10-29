import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, animated, size, screen) -> None:
        super().__init__()
        self.size = size
        self.animated = animated
        self.img_frames = img
        self.image = img[0]
        self.imgFrame = 0
        self.rect = self.image.get_rect()
        self.imgAngle = None
        self.x = 100
        self.y = 100
        self.rect.topleft = [self.x, self.y]
        self.speed = 0
        self.state = False
        self.screen = screen
        self.fill()

    def fill(self):
        if self.animated == False:
            self.image.fill(WHITE)
            self.rect.center = [360, 200]
            pygame.display.flip()

    def update(self):
        pygame.draw.rect(self.screen, BLACK,
                         [self.rect.topleft[0]-2, self.rect.topleft[1], self.rect.bottomright[0] - self.rect.topleft[0],
                          self.rect.bottomright[1] - self.rect.topleft[
                              1]])  # Clear the old sprite from the page without clearing the whole page
        if self.state and self.animated:
            self.imgFrame += 1  # Increment sprite frame
            self.imgFrame %= 4  # Makes sure curr_frame doesn't go out of arr bounds
        self.image = self.img_frames[self.imgFrame]

    def moveRight(self):
        self.state = True
        self.x += 10
        if self.x > self.size-(self.rect.bottomright[0]-self.rect.bottomleft[0]):
            pygame.draw.rect(self.screen, BLACK,
                         [self.rect.topleft[0], self.rect.topleft[1], self.rect.bottomright[0] - self.rect.topleft[0],
                          self.rect.bottomright[1] - self.rect.topleft[
                              1]])  # Clear the old sprite from the page without clearing the whole page
            self.x = 0
            self.y = random.randint(100, self.size-100)
        self.rect.topleft = [self.x, self.y]

    def getRect(self):
        return self.rect


class Scene:
    def __init__(self, size=100) -> None:
        self.size = size
        self.position = 0
        self.otherSprites = pygame.sprite.Group()
        self.frameRate = 30
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        self.state = 1  #1 = active | 2 = paused/inactive | 0 = Game Over
        self.sprites = pygame.sprite.Group()
        self.currSprite = None
        pygame.init()
        self.screen = pygame.display.set_mode((self.size, self.size))

    def start(self):
        while self.keepGoing:
            if self.state == 1: #if state is active
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.keepGoing = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            self.keepGoing = False
                        elif event.key == pygame.K_p:
                            self.pause(2)
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT:
                            self.currSprite.state = False
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    self.currSprite.moveRight()

                if self.checkCollision():
                    # Displays text on screen
                    font = pygame.font.Font('freesansbold.ttf', 32)  # Font of text
                    text = font.render('Game Over', True, GREEN, BLACK)  # Text to display with color green and black background
                    textRect = text.get_rect()  # Text rectangle
                    textRect.center = (self.size // 2, 100 // 2)  # Center text
                    self.screen.blit(text, textRect)  # Add text to screen
                    self.end()

                self.update()
                self.clock.tick(self.frameRate)
            elif self.state == 2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.keepGoing = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.pause(1)
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            self.keepGoing = False
            elif self.state == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.keepGoing = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            self.keepGoing = False

    def end(self):
        self.state = 0

    def pause(self, num):
        self.state = num

    def update(self):
        self.sprites.update()
        # Redraw sprite
        self.sprites.draw(self.screen)
        self.otherSprites.draw(self.screen)
        # Refresh display
        pygame.display.flip()

    def clear(self):
        self.screen.fill(BLACK)
        pygame.display.flip()

    def getSize(self):
        return self.size
    
    def getScreen(self):
        return self.screen

    def checkCollision(self):
        if pygame.sprite.spritecollideany(self.currSprite, self.otherSprites):
            return True

s = Scene(400)

toucan_frames = [pygame.image.load('toucan_0.png'), pygame.image.load('toucan_1.png'), pygame.image.load('toucan_2.png'), pygame.image.load('toucan_3.png')]
toucan = Sprite(toucan_frames, True, s.getSize(), s.getScreen())
box = Sprite([pygame.Surface([20,20])], False, s.getSize(), s.getScreen())
s.sprites.add(toucan)
s.otherSprites.add(box)
s.currSprite = toucan
s.start()