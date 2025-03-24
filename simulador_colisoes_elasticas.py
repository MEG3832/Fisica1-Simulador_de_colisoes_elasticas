import pygame
import random
import math
from pygame.locals import *
from sys import exit

pygame.init() 

# Cria a tela
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h
tela = pygame.display.set_mode((largura, altura), FULLSCREEN)
pygame.display.set_caption('Simulador de colisões elásticas')
relogio = pygame.time.Clock()

n_bolas = random.randint(10, 50)
densidade_area = random.randint(7, 565)
bolas = []

# Verifica se há sobreposição com alguma bola já existente
def verifica_sobreposição (nova_bola, bolas_existentes):
    for bola in bolas_existentes:
        dx = bola["x"] - nova_bola["x"]
        dy = bola["y"] - nova_bola["y"]

        distancia = math.sqrt(dx**2 + dy**2)

        if distancia < bola["raio"] + nova_bola["raio"]:
            return True
                    
    return False

# Cria as bolas
for i in range(n_bolas):
    while True: 
        raio = random.randint(15, 50)

        nova_bola = {
            "x": random.randint(raio, largura - raio),
            "y": random.randint(raio, altura - raio),
            "vx": random.randint(1, 4),
            "vy": random.randint(1, 4),
            "cor": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "raio": raio,
            "massa": math.pi * (raio ** 2) * densidade_area
        }

        # Elas apenas são criadas se estiverem em uma posição propícia
        if not verifica_sobreposição(nova_bola, bolas):
            bolas.append(nova_bola)
            break

while True:

    relogio.tick(60)

    tela.fill((255, 250, 255))

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            exit()

    for bola in bolas:
        # Detecta colisão com as paredes
        if bola["y"] + bola["raio"] + bola["vy"] >= altura or bola["y"] - bola["raio"] + bola["vy"] <= 0:
            bola["vy"] *= -1
        elif bola["x"] + bola["raio"] + bola["vx"] >= largura or bola["x"] - bola["raio"] + bola["vx"] <= 0:
            bola["vx"] *= -1

    for i in range(0, n_bolas):
        for j in range(i + 1, n_bolas):
            # Calcula a posição futura das bolinhas
            dx = bolas[i]["x"] - bolas[j]["x"]
            dy = bolas[i]["y"] - bolas[j]["y"]

            distancia = math.sqrt(dx**2 + dy**2)

            # Verifica se há colisão na próxima posição
            if distancia <= bolas[i]["raio"] + bolas[j]["raio"]:
                
                # Separa as bolas caso a distância entre elas seja menor do que a soma dos raios
                erro = bolas[i]["raio"] + bolas[j]["raio"] - distancia
                nx = dx / distancia
                ny = dy / distancia
                bolas[i]["x"] += nx * (erro / 2)
                bolas[i]["y"] += ny * (erro / 2)
                bolas[j]["x"] -= nx * (erro / 2)
                bolas[j]["y"] -= ny * (erro / 2)

                # Separa as bolas das bordas, caso tenham retornado para lá
                if bolas[i]["x"] - bolas[i]["raio"] < 0:
                    bolas[i]["x"] += bolas[i]["raio"] - bolas[i]["x"]
                elif bolas[i]["x"] - bolas[i]["raio"] > largura:
                    bolas[i]["x"] -= bolas[i]["raio"] - bolas[i]["x"]
                elif bolas[i]["y"] - bolas[i]["raio"] < 0:
                    bolas[i]["y"] += bolas[i]["raio"] - bolas[i]["y"]
                elif bolas[i]["y"] - bolas[i]["raio"] > largura:
                    bolas[i]["y"] -= bolas[i]["raio"] - bolas[i]["y"]

                # Vetor normal da colisão
                nx = dx / distancia
                ny = dy / distancia

                 # Projeção escalar das velocidades no vetor normal
                v1n = bolas[i]["vx"] * nx + bolas[i]["vy"] * ny
                v2n = bolas[j]["vx"] * nx + bolas[j]["vy"] * ny

                vcm = (bolas[i]["massa"]*v1n + bolas[j]["massa"]*v2n) / (bolas[i]["massa"] + bolas[j]["massa"])

                # Velocidades após a colisão
                v1n_final = 2*vcm - v1n
                v2n_final = 2*vcm - v2n

                # Componentes perpendicular ao vetor normal permanecem inalteradas
                v1t_x = bolas[i]["vx"] - v1n * nx
                v1t_y = bolas[i]["vy"] - v1n * ny
                v2t_x = bolas[j]["vx"] - v2n * nx
                v2t_y = bolas[j]["vy"] - v2n * ny

                # Recompõe os vetores de velocidade final
                bolas[i]["vx"] = v1n_final * nx + v1t_x
                bolas[i]["vy"] = v1n_final * ny + v1t_y
                bolas[j]["vx"] = v2n_final * nx + v2t_x
                bolas[j]["vy"] = v2n_final * ny + v2t_y

    # Atualiza as posições após resolver as colisões
    for bola in bolas:
        bola["x"] += bola["vx"]
        bola["y"] += bola["vy"]

        pygame.draw.circle(tela, bola["cor"], (int(bola["x"]), int(bola["y"])), bola["raio"])

    pygame.display.update()
