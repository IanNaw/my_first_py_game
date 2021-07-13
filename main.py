import pygame
import random



#Set up the bubble brain
class Bubble():
    #Bubble class constructure function
    def __init__(self, x, y):
        #Make some variables for the Bubble
        self.x = x
        self.y = y
        self.speed = random.randint(1, 3)
        self.pic = pygame.image.load("../assets/Bubble.png")
        self.on_screen = True

        #Shrink my bubble
        self.pic = pygame.transform.scale(self.pic, (15, 15))
        
    #Bubble update function
    def update(self, screen):
        self.y -= self.speed
        screen.blit(self.pic, (self.x, self.y))
        
        if self.y < -self.pic.get_height():
            self.on_screen = False
        

#Set up the Enemy's brian
class Enemy():
    
    #Enemy constructor funcion
    def __init__(self, x, y, speed, size):
        #Enemy's variables
        self.type = random.randint(0, 3)
        if self.type == 0:
            self.pic = pygame.image.load("../assets/Fish04_A.png")
            self.pic2 = pygame.image.load("../assets/Fish04_B.png")
        if self.type == 1:
            self.pic = pygame.image.load("../assets/Fish05_A.png")
            self.pic2 = pygame.image.load("../assets/Fish05_B.png")
        if self.type == 2:
            self.pic = pygame.image.load("../assets/Fish02_A.png")
            self.pic2 = pygame.image.load("../assets/Fish02_B.png")
        if self.type == 3:
            self.pic = pygame.image.load("../assets/Fish01_A.png")
            self.pic2 = pygame.image.load("../assets/Fish01_B.png")
        self.speed = speed
        self.size = size
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.25), self.size)
        self.animation_timer_max = 16
        self.animation_timer = self.animation_timer_max
        self.animation_frame = 0 

        #Shrink the enemy pic
        self.pic = pygame.transform.scale(self.pic, (int(self.size*1.25), self.size))
        self.pic2 = pygame.transform.scale(self.pic2, (int(self.size*1.25), self.size))

        #Flip the pic if moving left
        if self.speed < 0 :
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.pic2 = pygame.transform.flip(self.pic2, True, False)

    #Enemy update function
    def update(self, screen):
        self.animation_timer -= 1
        if self.animation_timer <= 0:
            self.animation_timer = self.animation_timer_max
            self.animation_frame += 1
            if self.animation_frame > 1:
                self.animation_frame = 0 
        self.x += self.speed
        if self.animation_frame == 0:
            screen.blit(self.pic, (self.x, self.y))
        else:
            screen.blit(self.pic2, (self.x, self.y))
        self.hitbox.x += self.speed
        #pygame.draw.rect(screen, (255, 0, 255), self.hitbox)

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

# Loading all pictures for the game
background_pic = pygame.image.load("../assets/Scene_A.png")
background_pic_2 = pygame.image.load("../assets/Scene_B.png")
player_pic = pygame.image.load("../assets/Fish03_A.png")
player_pic_2 = pygame.image.load("../assets/Fish03_open.png")
player_pic_anim = pygame.image.load("../assets/Fish03_B.png")

#Timers
background_timer_max = 20
background_timer = background_timer_max
background_frame = 0

fish_anim_timer_max = 6
fish_anim_timer = 0

player_swim_timer_max = 8
player_swim_timer = player_swim_timer_max
player_swim_frame = 0

bubble_timer = 0


#My variables for player
player_starting_x = 480
player_starting_y = 310
player_starting_size = 30
player_alive = False
player_facing_left = False
player_speed = 0.01
player_speed_x = 0
player_speed_y = 0
player_size = player_starting_size
player_x = player_starting_x
player_y = player_starting_y 
player_hitbox = pygame.Rect(player_x, player_y, int(player_size*1.25), player_size)


#HUD variables
score = -1
score_font = pygame.font.SysFont("default", 30)
score_text_variable = ""
play_pic = pygame.image.load("../assets/BtnPlay.png")
play_button_x = game_width/2 -play_pic.get_width()/2
play_button_y = game_height/2 -play_pic.get_height()/2
tittle_pic = pygame.image.load("../assets/BtnRestart.png")
tittle_x = game_width/2 -tittle_pic.get_width()/2
tittle_y = play_button_y - 200


#Enemy spawn timer variables
enemy_timer_max = 20
enemy_timer = enemy_timer_max


#My enemy's array
enemies = []
enemies_to_remove = []

#Make the bubbles array 
bubbles = []
bubbles_to_remove = []


# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:

    
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    
    
    #Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_speed_x += player_speed
    if keys[pygame.K_LEFT]:
        player_speed_x -= player_speed
    if keys[pygame.K_UP]:
        player_speed_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_speed_y += player_speed

    #Slowing down the player
    if player_speed_x > 1:
        player_speed_x -= 0.1
    if player_speed_x < -1:
        player_speed_x += 0.1
    if player_speed_y > 1:
        player_speed_y -= 0.1
    if player_speed_y < -1:
        player_speed_y += 0.1

    #Move the player
    player_x += player_speed_x
    player_y += player_speed_y
    
    #Where is the player looking
    if player_speed_x > 0:
        player_facing_left = False
    else:
        player_facing_left = True
    
    #Cheat 
    if keys[pygame.K_SPACE]:
        player_size += 2

    #Stop the player from leaving the screen
    if player_x < 0:
        player_x = 0
        player_speed_x = 0 
    if player_x > game_width - int(player_size*1.25):
        player_x = game_width - int(player_size*1.25)
        player_speed_x = 0
    if player_y < 0:
        player_y = 0
        player_speed_y = 0
    if player_y > game_height - player_size:
        player_y = game_height - player_size
        player_speed_y = 0


    #Enemy spawn timer loop
    enemy_timer -= 1
    if enemy_timer <= 0:
        new_enemy_y = random.randint(1, game_height)
        new_enemy_speed = random.randint(1, 10)
        new_enemy_size = random.randint(player_size/2, player_size*2)
        
        if random.randint(0, 1) == 0:   
            enemies.append(Enemy(-new_enemy_size*2, new_enemy_y, new_enemy_speed, new_enemy_size))
        else:
            enemies.append(Enemy(game_width, new_enemy_y, -new_enemy_speed, new_enemy_size))
        enemy_timer = enemy_timer_max
    
    background_timer -= 1
    if background_timer <= 0:
        background_frame +=1
        if background_frame > 1:
            background_frame = 0
        background_timer = background_timer_max

    if background_frame == 0:
        screen.blit(background_pic, (0,0));
    else:
        screen.blit(background_pic_2, (0,0))

    
    if player_alive:
        #Player hitbox
        player_hitbox.x = player_x
        player_hitbox.y = player_y
        player_hitbox.width = (player_size*1.25)
        player_hitbox.height = player_size
        #pygame.draw.rect(screen,(255, 255, 255), player_hitbox)

        #The score
        if player_alive:
            score_text_variable = "Score: "+str(score)
        else:
            score_text_variable = "Final Score: "+str(score)

        if score >= 0:
          screen.blit(score_text, (30, 30))  
        
        #Hitbox collition
        for enemy in enemies:
            if player_hitbox.colliderect(enemy.hitbox):
                if player_size >= enemy.size:
                    player_size +=2
                    score += enemy.size
                    enemies.remove(enemy)
                    fish_anim_timer = fish_anim_timer_max
                else:
                    player_alive = False

        #Making player swimming anim
        player_swim_timer -= 1
        if player_swim_timer == 0:
            player_swim_timer = player_swim_timer_max
            player_swim_frame += 1
            if player_swim_frame > 1:
                player_swim_frame = 0
        #Draw player pic
        if fish_anim_timer > 0:
            player_pic_small = pygame.transform.scale(player_pic_2, (int(player_size*1.25), player_size))
            fish_anim_timer -= 1
        else:
            if player_swim_frame == 0:
                player_pic_small = pygame.transform.scale(player_pic, (int(player_size*1.25), player_size))
            else:
                player_pic_small = pygame.transform.scale(player_pic_anim, (int(player_size*1.25), player_size))
        if player_facing_left:
            player_pic_small = pygame.transform.flip(player_pic_small, True, False)
                    
        #Changing Perspective
        
   
        screen.blit(player_pic_small, (player_x,player_y))
    
    

    #Player hitbox
    player_hitbox.x = player_x
    player_hitbox.y = player_y
    player_hitbox.width = (player_size*1.25)
    player_hitbox.height = player_size
    #pygame.draw.rect(screen,(255, 255, 255), player_hitbox)


    for enemy in enemies_to_remove:
        enemies.remove(enemy)
    enemies_to_remove = []
    
    #Updating enemies
    for enemy in enemies:
        enemy.update(screen)
        if enemy.x < -1000 or enemy.x > game_width+1000:
            enemies_to_remove.append(enemy)

    #Make a new bubble every time timer hits 0
    bubble_timer -= 1
    if bubble_timer <= 0 and player_alive:
        if player_facing_left:
            bubbles.append(Bubble(player_x, player_y))
        else:
            bubbles.append(Bubble(player_x + player_size*1.25, player_y))
        bubble_timer = random.randint(40, 90)
    
    #Update all the bubbles
    for bubble in bubbles:
        if bubble.on_screen:
            bubble.update(screen)
        else:
            bubbles_to_remove.append(bubble)

    #Remove the bubbles in bubbles_to_remove
    for bubble in bubbles_to_remove:
        bubbles.remove(bubble)
    bubbles_to_remove = []
        

    #Draw the menu
    if not player_alive:
        screen.blit(tittle_pic, (tittle_x, tittle_y))
        screen.blit(play_pic, (play_button_x, play_button_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if mouse_x > play_button_x and mouse_x < play_button_x+play_pic.get_width():
                if mouse_y > play_button_y and mouse_y < play_button_y+play_pic.get_height():
                    #Restart the game
                    for enemy in enemies:
                        enemies_to_remove.append(enemy)
                    player_alive = True
                    player_speed = 0.3
                    player_size = player_starting_size
                    player_x = player_starting_x
                    player_y = player_starting_y 
                    score = 0
            
    
    score_text = score_font.render(score_text_variable, 1, (255, 255, 255))
    #screen.blit(score_text, (30, 30))

    
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
