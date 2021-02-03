import pygame
from random import randrange

largura = 1080
altura = 720
tamanho = 20

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
cinza = (128, 128, 128)
prata = (192, 192, 192)
amarelo = (255, 255, 0)
fuchsia = (255, 0, 255)

try:
    pygame.init()
except:
    print('\033[31mHouve um erro!\033[m')

screen = pygame.display.set_mode((largura, altura))
fps = pygame.time.Clock()


def texto(msg, tam, cor, x_pos, y_pos):
    font = pygame.font.SysFont(None, tam)
    texto1 = font.render(msg, True, cor)
    screen.blit(texto1, [x_pos, y_pos])


def bordas(posx, posy, tamx, tamy):
    pygame.draw.rect(screen, prata, [posx, posy, tamx, tamy])


def player(pos_player1):
    for xy in pos_player1:
        pygame.draw.rect(screen, preto, [xy[0], xy[1], tamanho, tamanho])


def bonus(pos_x1, pos_y1):
    pygame.draw.rect(screen, vermelho, [pos_x1, pos_y1, tamanho, tamanho])


def jogo(gameover=False, modo=''):
    pos_x = randrange(0, largura - tamanho, 20)
    pos_y = randrange(0, altura - tamanho, 20)
    bonus_x = randrange(0, largura - tamanho, 20)
    bonus_y = randrange(0, altura - tamanho, 20)
    pos_player = list()
    playertam = 2
    contador = 0
    movimento_x = movimento_y = 0
    vel = 10
    sair = True

    while sair:

        for event2 in pygame.event.get():

            if event2.type == pygame.QUIT:
                sair = False
                gameover = False

            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_ESCAPE:
                    sair = False
                    gameover = False
            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_UP and movimento_y != tamanho:
                    movimento_x = 0
                    movimento_y = -tamanho
                if event2.key == pygame.K_DOWN and movimento_y != -tamanho:
                    movimento_x = 0
                    movimento_y = tamanho
                if event2.key == pygame.K_LEFT and movimento_x != tamanho:
                    movimento_x = -tamanho
                    movimento_y = 0
                if event2.key == pygame.K_RIGHT and movimento_x != -tamanho:
                    movimento_x = tamanho
                    movimento_y = 0

        screen.fill(branco)

        pos_y += movimento_y
        pos_x += movimento_x

        if pos_x == bonus_x and pos_y == bonus_y:
            bonus_x = randrange(0, largura - tamanho, 20)
            bonus_y = randrange(0, altura - tamanho, 20)
            playertam += 1
            contador += 1

        if modo == 'l':
            if pos_x + tamanho > largura:
                pos_x = 0
            if pos_x < 0:
                pos_x = largura - tamanho
            if pos_y + tamanho > altura:
                pos_y = 0
            if pos_y < 0:
                pos_y = altura - tamanho
        if modo == 'c':
            if pos_x + tamanho > largura:
                sair = False
                gameover = True
            if pos_x < 0:
                sair = False
                gameover = True
            if pos_y + tamanho > altura:
                sair = False
                gameover = True
            if pos_y < 0:
                sair = False
                gameover = True

        bloco = list()
        player_inicio = list()
        player_inicio.append(pos_x)
        player_inicio.append(pos_y)
        pos_player.append(player_inicio)
        bloco.append(player_inicio)
        if len(pos_player) > playertam:
            del pos_player[0]

        if playertam > 3:
            for c in range(0, playertam - 1):
                if bloco[0] == pos_player[c]:
                    sair = False
                    gameover = True

        if contador == 5:
            vel += 5
            contador = 0

        player(pos_player)
        bonus(bonus_x, bonus_y)

        pygame.display.update()
        fps.tick(vel)

    return gameover, playertam - 2


comeco = True
fimdejogo = False
inicio = True
dados = tuple()
modo1 = ''
while comeco:
    while inicio:

        screen.fill(branco)

        pygame.draw.rect(screen, cinza, [350, 240, 360, 50])
        texto('MODO CLÁSSICO[C]', 50, branco, 360, 250)

        pygame.draw.rect(screen, cinza, [390, 380, 280, 50])
        texto('MODO LIVRE[L]', 50, branco, 400, 390)

        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        if 350 < x < 710 and 240 < y < 290:
            bordas(350, 240, 360, 5)
            bordas(350, 285, 360, 5)
            bordas(350, 240, 5, 50)
            bordas(705, 240, 5, 50)
        if 390 < x < 670 and 380 < y < 430:
            bordas(390, 380, 280, 5)
            bordas(390, 425, 280, 5)
            bordas(390, 380, 5, 50)
            bordas(665, 380, 5, 50)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                comeco = fimdejogo = inicio = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    comeco = fimdejogo = inicio = False
                if event.key == pygame.K_c:
                    modo1 = 'c'
                    inicio = False
                    dados = jogo(modo=modo1)
                    comeco = fimdejogo = dados[0]
                if event.key == pygame.K_l:
                    modo1 = 'l'
                    inicio = False
                    dados = jogo(modo=modo1)
                    comeco = fimdejogo = dados[0]

            if event.type == pygame.MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if 350 < x < 710 and 240 < y < 290:
                    modo1 = 'c'
                    inicio = False
                    dados = jogo(modo=modo1)
                    comeco = fimdejogo = dados[0]
                if 390 < x < 670 and 380 < y < 430:
                    modo1 = 'l'
                    inicio = False
                    dados = jogo(modo=modo1)
                    comeco = fimdejogo = dados[0]

        pygame.display.update()

    while fimdejogo:

        screen.fill(branco)

        pygame.draw.rect(screen, preto, [435, 255, 200, 50])
        texto('Game Over', 50, azul, 440, 260)

        pygame.draw.rect(screen, preto, [240, 355, 350, 50])
        texto('Jogar Novamente[R]', 50, verde, 240, 360)

        pygame.draw.rect(screen, preto, [635, 355, 125, 50])
        texto('Sair[S]', 50, vermelho, 640, 360)

        pygame.draw.rect(screen, preto, [0, 0, 1080, 40])
        texto(f'PONTOS: {dados[1]}', 30, branco, 10, 10)

        pygame.draw.rect(screen, preto, [290, 450, 455, 50])
        texto('VOLTAR PARA O MENU[M]', 50, branco, 300, 460)

        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        if 240 < x < 590 and 355 < y < 405:
            bordas(240, 355, 350, 5)
            bordas(240, 400, 350, 5)
            bordas(240, 355, 5, 50)
            bordas(585, 355, 5, 50)
        if 635 < x < 760 and 355 < y < 405:
            bordas(635, 355, 125, 5)
            bordas(635, 400, 125, 5)
            bordas(635, 355, 5, 50)
            bordas(755, 355, 5, 50)
        if 290 < x < 735 and 450 < y < 500:
            bordas(290, 450, 455, 5)
            bordas(290, 495, 455, 5)
            bordas(290, 450, 5, 50)
            bordas(740, 450, 5, 50)

        for event1 in pygame.event.get():

            if event1.type == pygame.QUIT:
                comeco = fimdejogo = False

            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_ESCAPE:
                    comeco = fimdejogo = False
                if event1.key == pygame.K_s:
                    comeco = fimdejogo = False
                if event1.key == pygame.K_r:
                    dados = jogo(modo=modo1)
                    comeco = fimdejogo = dados[0]
                if event1.key == pygame.K_m:
                    inicio = True
                    fimdejogo = False

            if event1.type == pygame.MOUSEBUTTONUP:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if 240 < x < 590 and 355 < y < 405:
                    dados = jogo(modo=modo1)
                    comeco = fimdejogo = dados[0]
                if 635 < x < 760 and 355 < y < 405:
                    comeco = fimdejogo = False
                if 290 < x < 735 and 450 < y < 500:
                    inicio = True
                    fimdejogo = False

        pygame.display.update()

pygame.quit()
