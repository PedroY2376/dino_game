import pygame
from random import randrange, choice
import os

#! Salvando diretorios
diretorio_principal = os.path.dirname(__file__)
diretorio_graphics = os.path.join(diretorio_principal, 'graphics')
diretorio_sounds = os.path.join(diretorio_principal, 'sound')

pygame.init()
pygame.mixer.init()

#! Básic
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Game')
clock = pygame.time.Clock()

#! Sprite Sheet
sprite_sheet = pygame.image.load(os.path.join(diretorio_graphics, 'dinoSpritesheet.png')).convert_alpha()

#! Sons
som_colision = pygame.mixer.Sound(os.path.join(diretorio_sounds, 'death_sound.wav'))
som_colision.set_volume(1)
som_pontucao = pygame.mixer.Sound(os.path.join(diretorio_sounds, 'score_sound.wav'))
som_pontucao.set_volume(0.75)

#! Variáveis
colidiu = False
escolha_obstaculo = choice([0,0,1])
pontos = 0
velocidade_jogo = 5

def exibe_mensagem(msg, tamanho_font, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho_font, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 5
    colidiu = False
    dino_voador.rect.x = SCREEN_WIDTH + 40
    cacto.rect.x = SCREEN_WIDTH + 40
    escolha_obstaculo = choice([0,0,1])
    dino.rect.y = SCREEN_HEIGHT - 64
    dino.active_jump = False

#! Classes
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dino = []
        for i in range (3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dino.append(img)
            
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sounds, 'jump_sound.wav'))
        self.som_pulo.set_volume(0.5)
            
        self.index_lista = 0
        self.image = self.imagens_dino[self.index_lista]
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect(center = (100,SCREEN_HEIGHT - 64))    
        self.mask = pygame.mask.from_surface(self.image)  
        
        self.pos_y_init = (SCREEN_HEIGHT - 64) - 96/2
        self.active_jump = False
        self.gravity = 0
   
    def jump(self):
        self.active_jump = True
        self.som_pulo.play()
   
    def update(self): 
        if self.active_jump:
            if self.rect.y <= 300:
                self.active_jump = False
            self.gravity -= 1.5
            self.rect.y += self.gravity
        else:
            if self.rect.y < self.pos_y_init:
                self.gravity += 1.5
                self.rect.y += self.gravity
            else: 
                self.rect.y = self.pos_y_init
                self.gravity = 0
                   
        if self.index_lista >2:
            self.index_lista = 0
        self.index_lista += 0.15  
        self.image = self.imagens_dino[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = sprite_sheet.subsurface((32*7, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH+randrange(30, 300, 90),randrange(50, 200, 50)))
        
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect = self.image.get_rect(center = (SCREEN_WIDTH+randrange(30, 300, 90),randrange(50, 200, 50)))
            
        self.rect.x -= velocidade_jogo

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32*6, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect(bottomleft = (pos_x*64, SCREEN_HEIGHT))
        
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
        self.rect.x -= 5

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((32*5, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2.5, 32*2.5))   
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH + 40, SCREEN_HEIGHT - 64))
        self.mask = pygame.mask.from_surface(self.image)  
        self.escolha = escolha_obstaculo
        
    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0: self.rect.x = SCREEN_WIDTH
            self.rect.x -= velocidade_jogo
   
class Dino_voador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dino = []
        for i in range (3,5):
            img = sprite_sheet.subsurface((32*i, 0), (32,32))
            img = pygame.transform.scale(img, (32*2.5, 32*2.5)) 
            self.imagens_dino.append(img)
            
        self.index_image = 0
        self.image = self.imagens_dino[self.index_image]    
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH + 40, 300))
        self.escolha = escolha_obstaculo
        
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0: self.rect.x = SCREEN_WIDTH
            self.rect.x -= velocidade_jogo
            
            if self.index_image >1:
                self.index_image = 0
            self.index_image += 0.1  
            self.image = self.imagens_dino[int(self.index_image)]
      
#! Instanciar as classes 
todas_sprite = pygame.sprite.Group()
dino = Dino()
todas_sprite.add(dino)

for i in range (4):
    nuvens = Nuvens()
    todas_sprite.add(nuvens)

for i in range(int((SCREEN_WIDTH + 64)/64)):
    ground = Ground(i)
    todas_sprite.add(ground)

cacto = Cacto()
todas_sprite.add(cacto)

dino_voador = Dino_voador()
todas_sprite.add(dino_voador)

sprite_obstaculos = pygame.sprite.Group()
sprite_obstaculos.add(cacto)
sprite_obstaculos.add(dino_voador)

#! Loop Infinito
while True:
    clock.tick(60)
    screen.fill('white')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if colidiu == True and event.key == pygame.K_r:
                reiniciar_jogo()
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and dino.rect.y == dino.pos_y_init and colidiu == False:
        dino.jump()


    if dino_voador.rect.topright[0] <= 0 or cacto.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,0,1])
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo
        
        cacto.rect.x = SCREEN_WIDTH
        dino_voador.rect.x = SCREEN_WIDTH
        
    colision = pygame.sprite.spritecollide(dino, sprite_obstaculos, False, pygame.sprite.collide_mask)     
    if colision and colidiu == False:
        som_colision.play()
        colidiu = True
        
    if colidiu == True:
        if pontos % 100 == 0: pontos += 1
        game_over = exibe_mensagem('GAME OVER', 40, (0,0,0))
        reiniciar_txt = exibe_mensagem('Pressione r para reiniciar', 20, (0,0,0))
        screen.blit(game_over, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(reiniciar_txt, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60))
        pass
    else:
        pontos += 0.5
        todas_sprite.update()
        txt_pontos = exibe_mensagem(int(pontos), 40, (0,0,0))
    
    if pontos % 100 == 0:
        som_pontucao.play()
        if velocidade_jogo >= 15: velocidade_jogo += 0    
        else: velocidade_jogo += 1       
    
    todas_sprite.draw(screen)
    screen.blit(txt_pontos, (520,30))
    pygame.display.update()