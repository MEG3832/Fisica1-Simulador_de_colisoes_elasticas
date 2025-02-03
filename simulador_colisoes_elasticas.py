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
tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
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
        if bola["x"] + bola["raio"] + bola["vx"] >= largura or bola["x"] - bola["raio"] + bola["vx"] <= 0:
            bola["vx"] *= -1

    for i in range(0, n_bolas):
        for j in range(i + 1, n_bolas):
            # Calcula a posição futura das bolinhas
            dx = (bolas[i]["x"] + bolas[i]["vx"]) - (bolas[j]["x"] + bolas[j]["vx"])
            dy = (bolas[i]["y"] + bolas[i]["vy"]) - (bolas[j]["y"] + bolas[j]["vy"])

            distancia = math.sqrt(dx**2 + dy**2)

            # Verifica se há colisão na próxima posição
            if distancia <= bolas[i]["raio"] + bolas[j]["raio"]:
                
                vcmx = (bolas[i]["massa"]*bolas[i]["vx"] + bolas[j]["massa"]*bolas[j]["vx"]) / (bolas[i]["massa"] + bolas[j]["massa"])
                vcmy = (bolas[i]["massa"]*bolas[i]["vy"] + bolas[j]["massa"]*bolas[j]["vy"]) / (bolas[i]["massa"] + bolas[j]["massa"])

                aux = bolas[i]["vx"]
                bolas[i]["vx"] = 2 * vcmx - bolas[i]["vx"]
                bolas[j]["vx"] = (bolas[i]["massa"] * (aux - bolas[i]["vx"]) + bolas[j]["massa"] * bolas[j]["vx"]) / bolas[j]["massa"]

                aux = bolas[i]["vy"]
                bolas[i]["vy"] = 2 * vcmy - bolas[i]["vy"]
                bolas[j]["vy"] = (bolas[i]["massa"] * (aux - bolas[i]["vy"]) + bolas[j]["massa"] * bolas[j]["vy"]) / bolas[j]["massa"]

    # Atualiza as posições após resolver as colisões
    for bola in bolas:
        bola["x"] += bola["vx"]
        bola["y"] += bola["vy"]

        pygame.draw.circle(tela, bola["cor"], (int(bola["x"]), int(bola["y"])), bola["raio"])

    pygame.display.update()
