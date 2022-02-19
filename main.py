import pygame 
import math
import random

# Inicializar o pygame e Criar a janela do jogo 
pygame.init()
altura = 560
largura = 840
screen = pygame.display.set_mode((largura,altura)) # criando a tela.

pygame.display.set_caption("Guerra Espacial")

# Fundo
fundo = pygame.image.load('Fundo.png')

# Objetos Do Jogo
# Jogador
velocidadeJogador = 4
JogadorIMG = pygame.image.load('Jogador.png') # Imagem da nave Jogador
JogadorLarguraIMG = 128 # pra subtrair na hora da borda
JogadorX = largura * 0.45 # pos inicial eixo X da nave
JogadorY = altura * 0.75 # pos inicial eixo Y da nave
Jogador_MudaX = 0 # isto sera somado ao JogadorX.

# Inimigo
velocidadeInimigo = 6

# lista para os atributos de cada Inimigo.
InimigoIMG = []
InimigoLarguraIMG = []
InimigoX = []
InimigoY = []
Inimigo_MudaX = []
Inimigo_MudaY = []
# quantidade de inimigos
InimigoQuant = 7
# inserindo os dados de cada Inimigo
for i in range(InimigoQuant):
    InimigoIMG.append(pygame.image.load('Inimigo.png')) # Imagem pro Inimigo 
    InimigoIMG.append(pygame.image.load('Inimigo2.png')) # Imagem pro Inimigo
    InimigoLarguraIMG.append(50) # pra subtrair na hora da borda 
    InimigoX.append(random.randint(0, largura - InimigoLarguraIMG[i])) # pos inicial eixo X randomizado 
    InimigoY.append(altura * 0.01) # posicao inicial Y comum
    Inimigo_MudaX.append(random.randint(-1, 1) * velocidadeInimigo + 1) #  Deixamos uma velocidade randomica pra esquerda e direita para o eixo x 
    Inimigo_MudaY.append(random.randint(0, 9) * 0.06)  # Randomizamos um pouco a velocidade de queda 

# Missil
velocidadeMissil = 7
MissilIMG = pygame.image.load('Missil.png') 
MissilX = 0
MissilY = altura * 0.90
Missil_MudaX = 0 
Missil_MudaY = velocidadeMissil 
MissilEstado = "Carregado"

# utilizando formula de distancia entre cordenadas de dois pontos
def Colisao(X1,Y1,X2,Y2):
    Distancia = math.sqrt(math.pow(X1 - X2, 2) + (math.pow(Y1 - Y2, 2)))
    if Distancia <= 50  :
        ExplosaoIMG = pygame.image.load('Explosão.png') 
        screen.blit(ExplosaoIMG, (MissilX, MissilY))
        return True
    else:
        return False

# funcoes para cada objeto aparecer na tela.
def Jogador(x,y):
    screen.blit(JogadorIMG, (x,y)) # aqui estamos desenhando a nave sobre a janela do jogo(surface)
def Inimigo(x,y,i):
    screen.blit(InimigoIMG[i], (x,y)) 
def AtirarMissil(x,y): # comeca o lancamento do Missil 
    global MissilEstado
    MissilEstado = "Descarregado"
    screen.blit(MissilIMG, (x,y))

# O jogo
running = True
while running:
    screen.fill((255,255,255)) # mudando a cor da janela pra branco
    screen.blit(fundo,(0,0))
    for event in pygame.event.get():
        if(event.type == pygame.QUIT): # caso o evento quit() é acionado, o programa fecha. o evento quit() é clicar no X na janela.
            running = False 

    # Teclado Jogador
        if(event.type == pygame.KEYDOWN): # este evento verifica se uma tecla foi presionada 
            if(event.key == pygame.K_a): # caso seja a tecla A, decrementa de JogadorX
                Jogador_MudaX -= velocidadeJogador
            if(event.key == pygame.K_d): # caso seja a tecla D, incrementa de JogadorX
                Jogador_MudaX += velocidadeJogador
            if(event.key == pygame.K_SPACE): # caso seja a tecla espaco, verifica se o Missil esta na tela.
                if(MissilEstado == "Carregado"): # aqui verificamos se o Missil esta na tela.
                    MissilX = JogadorX + JogadorLarguraIMG/4 # pegamos a posicao atual do Jogador para o Missil 
                    AtirarMissil(MissilX,MissilY) # atiramos o Missil de acordo com a posicao atual do Jogador 
        if(event.type == pygame.KEYUP): # este evento verifica se uma tecla foi solta, isso foi feito pra poder segurar a tecla 
            if(event.key == pygame.K_a):
                Jogador_MudaX = 0
            if(event.key == pygame.K_d):
                Jogador_MudaX = 0

    # Movimentos Jogador
    JogadorX = JogadorX + Jogador_MudaX  

    # Movimentos Missil
    if (MissilY < 0): 
        MissilY = altura * 0.90
        MissilEstado = "Carregado" # no momento que o Missil atinge o final do mapa, ele reseta.   
    if (MissilEstado == "Descarregado"): # enquanto o Missil nao chega no final do mapa, ele vai andando
        AtirarMissil(MissilX,MissilY)
        MissilY -= Missil_MudaY

    for i in range(InimigoQuant):
        # Movimentos Inimigo
        InimigoX[i] = InimigoX[i] + Inimigo_MudaX[i]  
        InimigoY[i] = InimigoY[i] + Inimigo_MudaY[i] 
        # Borda da tela para Inimigo
        if(InimigoX[i] < 0):
            Inimigo_MudaX[i] = velocidadeInimigo
        if(largura - InimigoLarguraIMG[i] < InimigoX[i]): 
            Inimigo_MudaX[i] = -velocidadeInimigo
        if(JogadorY <= InimigoY[i]):
            running = False # Perdeu, deixou passar o asteroid
        # verificar se teve colisao entre o inimigo e o Missil
        Resultado = Colisao(InimigoX[i],InimigoY[i],MissilX,MissilY)
        if (Resultado):
            MissilY = altura * 0.90
            MissilEstado = "Carregado" # caso aconteceu uma colissao, resetar o Missil
            InimigoX[i] = random.randint(0, largura - InimigoLarguraIMG[i]) # pos inicial eixo X da nave
            InimigoY[i] = altura * 0.01 # pos inicial eixo Y da nave
        Inimigo(InimigoX[i],InimigoY[i], i) # chamada da funcao para movimentar inimigo

    # Borda da tela para Jogador
    if(JogadorX < 0):
        JogadorX = 0.1
    if(largura - JogadorLarguraIMG < JogadorX):
        JogadorX = largura - JogadorLarguraIMG 
    
    # Chamadas 
    Jogador(JogadorX,JogadorY) # chamanda da funcao Jogador para atualizar a pocisao do Jogador em cada frame
    pygame.display.update()
