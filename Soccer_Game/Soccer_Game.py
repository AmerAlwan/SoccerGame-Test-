import pygame
import random
import os
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 217, 0)
BLUE = (0, 10, 255)
GREEN = (0, 255, 35)

fps = 60

width = 1466
height = 768
size = ((width, height))
up = False
down = False
right = False
left = False
ball_hit = False
going = False
fast = False
ball_timer_max = fps/4
ball_timer = 0


screen = pygame.display.set_mode(size)

pygame.display.set_caption("Fifa 2018 2D Edition")

Clock = pygame.time.Clock()

running = True
main = True

game_folder = os.path.dirname("../img")
MySpritesFolder = os.path.join(game_folder, "img")

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.SysFont("Bauhaus 93" , size)
    text_surface = font.render(text, True, color) # True refers to wether the text is anit-aliased
                                                  # Alies means ALL BLACK and creatss jagged lines
                                                  # Anti-Aliased uses grey pixel sto "smooth corner"
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def draw_image(surf, name, x, y, colorRemove):
    dr_image = pygame.image.load(os.path.join(MySpritesFolder, name)).convert()
    if colorRemove == '':
        pass
    else:
        dr_image.set_colorkey(colorRemove)
    
    surf.blit(dr_image, (x,y))

def wait(time):
    max = time * fps
    timer = 0
    while timer != max:
        
        timer += 1

def goal():
    global ball_hit
    ball_hit = False
    Ball.rect.x = width/2
    Ball.rect.y = height/2
    player.rect.x = (width/2) - 50
    player.rect.y = height / 2
    draw_text(screen, "GOAAAALLALALALALALALALALA!!!!!!!!!!!!!!!!!", 500, width / 2, height / 2, BLACK)
    #wait(2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(MySpritesFolder, 'player_left.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = width / 2 - 100
        self.rect.y = height / 2
        self.radius = int(self.rect.width * .85 / 2)

    def update(self):
        global up; global down; global left; global right
        global fast
        keys = pygame.key.get_pressed()
        self.previousx = self.rect.x
        self.previousy = self.rect.y
        direction = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_w]
        for i in range(0, len(direction)-1):
            if keys[pygame.K_SPACE] and keys[direction[i]]:
                fast = True

        if keys[pygame.K_d]:
            self.image = pygame.image.load(os.path.join(MySpritesFolder, 'player_left.png')).convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = self.previousx
            self.rect.y = self.previousy
            self.rect.x += 16
            right = True
            left = False; up = False; down = False
        if keys[pygame.K_a]:
            self.image = pygame.image.load(os.path.join(MySpritesFolder, 'player_right.png')).convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = self.previousx
            self.rect.y = self.previousy
            self.rect.x -= 16
            left = True
            right = False; up = False; down = False
        if keys[pygame.K_w]:
            self.image = pygame.image.load(os.path.join(MySpritesFolder, 'player_up.png')).convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = self.previousx
            self.rect.y = self.previousy
            self.rect.y -= 16
            up = True
            right = False; down = False; left = False;
        if keys[pygame.K_s]:
            self.image = pygame.image.load(os.path.join(MySpritesFolder, 'player_down.png')).convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.x = self.previousx
            self.rect.y = self.previousy
            self.rect.y += 16
            down = True
            up = False; right = False; left = False
        

        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height


class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(MySpritesFolder, "ball_1.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = width / 2
        self.rect.y = height / 2
        self.speedx = 0
        self.speedy = 0
        self.speed = 10
        self.radius = int(self.rect.width * .85 / 2)
    def update(self):
        global ball_hit
        global ball_timer
        global ball_timer_max
        global up; global down; global left; global right
        global going
        global fast
        self.speed = 10
        if self.rect.right > width:
                if self.rect.top > 256 and self.rect.bottom < 512:
                    print("hit")
                    goal()
        if self.rect.left < 50:
            if self.rect.top > 256 and self.rect.bottom < 512:
                    print("hit")
                    goal()
        if ball_hit:
            print("True1")
            if ball_timer < ball_timer_max:
                print("True2")
                if fast:
                    self.speed = 30
                    fast = False
                if going == False:
                    if up:
                        self.speedy = -self.speed
                        self.speedx = 0
                        going = True
                    if down:
                        self.speedy = self.speed
                        self.speedx = 0
                        going = True
                    if right:
                        self.speedx = self.speed
                        self.speedy = 0
                        print("True3")
                        going = True
                    if left:
                        self.speedx = -self.speed
                        self.speedy = 0
                        going = True
              
                ball_timer += 1
                self.rect.x += self.speedx
                self.rect.y += self.speedy
            elif ball_timer >= ball_timer_max:
                ball_timer = 0
                ball_hit = False
                self.speedx = 0
                self.speedy = 0
                going = False
                self.speed = 10
            self.speed  = 10
            if self.rect.x >= width:
                self.rect.x = width - 50
                #player.rect.x = 50
                #player.rect.y = 50
                ball_hit = False
            if self.rect.x < 0:
                self.rect.x = 0
                ball_hit = False
            if self.rect.y >= height:
                self.rect.y = height - 50
                #player.rect.x = 50
                #player.rect.y = 50
                ball_hit = False
            if self.rect.y < 0:
                self.rect.y = 0
                ball_hit = False
            
            
            



class background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        draw_image(screen, 'playground.png', 0, 0, '')
        draw_image(screen, 'goal_right.png', 5, (height / 2) - 125, BLACK)
        draw_image(screen, 'goal_left.png', width - 110, (height / 2) - 125, BLACK)


        
        

class main_screen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       # pygame.draw.ellipse(screen, BLUE, [((width / 9) * 6) - 90, (height / 4) - 15, 500, 100])
        
        back = pygame.image.load(os.path.join(MySpritesFolder, "main_background.png")).convert()
        back_x = 0
        back_y = 0
        screen.blit(back, (back_x, back_y))
        button_image = pygame.image.load(os.path.join(MySpritesFolder, "play_button.png")).convert()
        button_x = ((width / 9) * 6) - 120
        button_y = (height / 4) - 15
        button_image.set_colorkey(WHITE)
        screen.blit(button_image, (button_x, button_y))
        draw_text(screen, "Press Enter to Play", 50, (width / 9) * 7, height / 4, YELLOW)
        
    def update(self):
        pass


all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
players = pygame.sprite.Group()
main = main_screen()
#all_sprites.add(main)
player = Player()
#goals = Goals()
Ball = ball()
balls.add(Ball)
players.add(player)
all_sprites.add(Ball)
#goal = Goal()



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    key = pygame.key.get_pressed()

    all_sprites.update()
    #screen.fill(WHITE)
    

    if ball_hit == False:
        hits = pygame.sprite.spritecollide(player, balls, False, pygame.sprite.collide_circle)
        if hits:
            ball_hit = True
        

    if main:
        main.__init__()
    else:
        background()
        #Goals()
        all_sprites.add(player)
    all_sprites.draw(screen)
    if key[pygame.K_RETURN]:
            main = False
                
    Clock.tick(fps)

    pygame.display.flip()