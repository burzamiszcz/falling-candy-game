import pygame, sys
import numpy as np
import os
from win32api import GetSystemMetrics

def resource_path0(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



#rozdzielczosc ekranu
screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)

pygame.init()
pygame.display.set_caption('DRUG GAME')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#dźwięki
gameover = pygame.mixer.Sound(resource_path0('data\\gameover.wav'))
getib = pygame.mixer.Sound(resource_path0('data\\getib.wav'))
lostib = pygame.mixer.Sound(resource_path0('data\\lostib.wav'))


#grafiki
    #tło
bg_surface = pygame.image.load(resource_path0('data\\assets\\backgrounds\\background%s.jpg')%(np.random.randint(1,5))).convert()
bg_surface = pygame.transform.scale(bg_surface, (screen_width, screen_height))

    #drugs
drugs_list = []
for i in range(10):
    drug_to_list = pygame.image.load(resource_path0('data\\assets\\drugs\\%s.png')%(i + 1)).convert_alpha()
    drug_to_list = pygame.transform.scale(drug_to_list, (45, 45))
    drugs_list.append(drug_to_list)

    #postać
player_surface = pygame.image.load(resource_path0('data\\assets\\player.png')).convert_alpha()
player_surface = pygame.transform.scale(player_surface, (150, 150))
    #postać koniec gry
playerdead_surface = pygame.image.load(resource_path0('data\\assets\\player.png')).convert_alpha()
playerdead_surface = pygame.transform.scale(playerdead_surface, (150, 150))
    #życia
heart_surface = pygame.image.load(resource_path0('data\\assets\\heart.png')).convert_alpha()
heart_surface = pygame.transform.scale(heart_surface, (50, 50))

#font dla gry
game_font = pygame.font.Font(resource_path0('data\\Lato-Black.ttf'), 40)


#wyświetlanie wyniku gry
def score_display(score):
    score_surface = game_font.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(screen_width / 2, 100))
    screen.blit(score_surface, score_rect)

#ekran końcowy
def gameover_display():
    global drugs, score, lifes, gameover_data, is_game_stared, time

    gameover_surface = game_font.render('GAME OVER', True, (255, 255, 255))
    gameover_rect = gameover_surface.get_rect(center=(screen_width / 2, 300))
    screen.blit(gameover_surface, gameover_rect)

    replay_surface = game_font.render('REPLAY?', True, (255, 255, 255))
    replay_rect = replay_surface.get_rect(center=(screen_width / 2, 500))
    if replay_rect.collidepoint(mx, my):
        replay_surface = game_font.render('REPLAY?', True, (255, 0, 0))
        if pygame.mouse.get_pressed()[0]:
            drugs = []
            score = 0
            lifes = 3
            gameover_data = 0
            time = 0
    screen.blit(replay_surface, replay_rect)

    exit_game_surface = game_font.render('EXIT', True, (255, 255, 255))
    exit_game_rect = exit_game_surface.get_rect(center=(screen_width/2, 700))
    if exit_game_rect.collidepoint(mx, my):
        exit_game_surface = game_font.render('EXIT', True, (255, 0, 0))
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()
    screen.blit(exit_game_surface, exit_game_rect)


    

def start_menu(mx, my):
    global is_game_stared

    start_game_surface = game_font.render('START', True, (255, 255, 255))
    exit_game_surface = game_font.render('EXIT', True, (255, 255, 255))
    start_game_rect = start_game_surface.get_rect(center=(screen_width/2, 300))
    exit_game_rect = exit_game_surface.get_rect(center=(screen_width/2, 500))
    if start_game_rect.collidepoint(mx, my):
        start_game_surface = game_font.render('START', True, (255, 0, 0))
        if pygame.mouse.get_pressed()[0]:
            is_game_stared = 1
    if exit_game_rect.collidepoint(mx, my):
        exit_game_surface = game_font.render('EXIT', True, (255, 0, 0))
        if pygame.mouse.get_pressed()[0]:
            pygame.quit()
            sys.exit()

    screen.blit(start_game_surface, start_game_rect)
    screen.blit(exit_game_surface, exit_game_rect)



class drug_c:
    def __init__(self):
        self.d_x_pos = np.random.randint(-10, screen_width - 100)
        self.d_y_pos = -100
        self.image = drugs_list[np.random.randint(1,10)]
        self.angle = np.random.randint(-40,40)
        self.spin_speed = np.random.randint(1,3) + np.random.random()
        self.surface = pygame.transform.rotate(self.image, self.angle)
        self.falling_speed = np.random.randint(0,1) + np.random.random()

#wyświetlanie drugów
def drug_blitz():
    global score, lifes
    for drug in drugs:
        drug_rect = drug.surface.get_rect(center = (drug.d_x_pos, drug.d_y_pos))
        drug.angle += drug.spin_speed
        drug.surface = pygame.transform.rotate(drug.image, drug.angle)
        screen.blit(drug.surface, drug_rect)
        if player_rect.colliderect(drug_rect):
            drugs.remove(drug)
            getib.play()
            score += 1
            continue
        if drug.d_y_pos >= screen_height:
            lifes -= 1
            lostib.play()
            drugs.remove(drug)
            continue
        drug.d_y_pos += (1.2 + 0.03 * time * 2) + drug.falling_speed

def drug_spawn(chance):
    if chance <= 0.1:
        drugs.append(drug_c())


#pomocnicze parametry
drugs = []
score = 0
lifes = 3
time = 0
tick = 0
gameover_data = 0
is_game_stared = 0

while True:
    tick += 1
    if tick == 120:
        time += 1
        tick = 0


#dodanie kolejnego levelu gry jako podwyzszenie gracza
    #pozycja myszy
    mx, my = pygame.mouse.get_pos()

    #eventy w gierce
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if tick % 12 == 0 and is_game_stared == 1 and gameover_data == 0:
        print('spawn')
        drug_spawn(np.random.random() - 0.005 * score)

    #wyświetlanie tła
    screen.blit(bg_surface, (0, 0))

    if is_game_stared == 1:
        #gra podczas posiadania żyć
        if lifes > 0:
            drug_blitz()

        #gra bez zyć
        else:
            if gameover_data == 0:
                gameover.play()
                gameover_data = 1
            gameover_display()


        #wyświetlanie żyć
        for i in range(lifes):
            screen.blit(heart_surface, (50 + i * 55, 10))
            
        #wyswietlanie playera
        if gameover_data == 0:
            player_rect = player_surface.get_rect(midbottom = (mx, screen_height))
            screen.blit(player_surface, player_rect)

        #martwa postać
        else:
            playerdead_rect = playerdead_surface.get_rect(midbottom = (mx, screen_height))
            screen.blit(playerdead_surface, playerdead_rect)
        score_display(score)
        # ib_pos_y += 1
        # screen.blit(ib_surface, (0, ib_pos_y))
    else:
        start_menu(mx, my)

    pygame.display.update()
    clock.tick(120)
