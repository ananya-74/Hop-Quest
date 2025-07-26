import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,35))
    screen.blit(score_surf,score_rect )
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 350:
                screen.blit(cactus_surf, obstacle_rect)
            else:
                screen.blit(hotair_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return [] 

def collisions(player, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player.colliderect(obstacle_rect):
                # Only count as collision if player's feet are at or below the top of the cactus
                if player.bottom >= obstacle_rect.top + 10:  # +10 for a little tolerance
                    return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 350:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]    


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('sound.mp3')
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound('jump.wav')

screen = pygame.display.set_mode((900, 450))
pygame.display.set_caption("Run&Jump") 
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 35)
game_active = False
start_time = 0
score = 0

background_surface = pygame.image.load('graphics/background.jpg').convert()

# score_surf = test_font.render('My Game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400,50))

#cactus
cactus_frame_1 = pygame.image.load('graphics/cactus1.png').convert_alpha()
cactus_frame_2 = pygame.image.load('graphics/cactus11.png').convert_alpha()
cactus_frames = [cactus_frame_1, cactus_frame_2]
cactus_frame_index = 0
cactus_surf = cactus_frames[cactus_frame_index]
#hotair
hotair_frame1 = pygame.image.load('graphics/hotair1.png').convert_alpha()
hotair_frame2 = pygame.image.load('graphics/hotair.png').convert_alpha()
hotair_frames = [hotair_frame1, hotair_frame2]
hotair_frame_index = 0
hotair_surf = hotair_frames[hotair_frame_index]

obstacle_rect_list = []

player_walk1 = pygame.image.load('graphics/girl1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/girl22.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/girl_jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80,350))
player_gravity = 0
#intro screen
player_stand = pygame.image.load('graphics/girl1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(350,240))

game_name = test_font.render('HOP QUEST',False,(96,96,96))
game_name_rect = game_name.get_rect(center = (410,115))

game_message = test_font.render('Press space to run',False,(96,96,96))
game_message_rect = game_message.get_rect(center = (410,370))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

cactus_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(cactus_animation_timer,500)

hotair_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(hotair_animation_timer,200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 350:
                    player_gravity = -20
                    jump_sound.play()

            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE and player_rect.bottom >= 350:
                  player_gravity = -22 
                  jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000) 
        if game_active:
            if event.type == obstacle_timer and game_active:
               if randint(0,2):
                   obstacle_rect_list.append(cactus_surf.get_rect(midbottom = (randint(900, 1000), 350)))
               else:
                   obstacle_rect_list.append(hotair_surf.get_rect(midbottom = (randint(900, 1000), 210)))
            
            if event.type == cactus_animation_timer:
                if cactus_frame_index == 0: cactus_frame_index = 1
                else: cactus_frame_index = 0
                cactus_surf = cactus_frames[cactus_frame_index]

            if event.type == hotair_animation_timer:
                if hotair_frame_index == 0: hotair_frame_index = 1
                else: hotair_frame_index = 0
                hotair_surf = hotair_frames[hotair_frame_index]
    

    if game_active:
        screen.blit(background_surface,(0,0))
        score = display_score()
        # pygame.draw.rect(screen,"#2addf4",score_rect)
        # pygame.draw.rect(screen,'#2addf4',score_rect,10)
        # screen.blit(score_surf, score_rect)

        # stone_rect.x -= 4
        # if stone_rect.right <= 0: stone_rect.left = 800
        # screen.blit(stone_surf, stone_rect)
                
        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 350: player_rect.bottom = 350
        player_animation()
        screen.blit(player_surf, player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect,obstacle_rect_list)
    else:
        screen.fill((204, 204, 0))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,350)
        player_gravity  = 0

        score_message = test_font.render(f'Your score:{score}',False,(96,96,96))
        score_message_rect = score_message.get_rect(center = (410,370))
        screen.blit(game_name,game_name_rect)

        if score == 0:screen.blit(game_message,game_message_rect)
        else:screen.blit(score_message,score_message_rect)    

    pygame.display.update()
    clock.tick(55)