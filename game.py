import pygame
import sys
from pygame.math import Vector2
import random

class Serpent:
    def __init__(self):
        self.corps = [Vector2(5,10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)
        self.nouveauBlock = False

        self.tete_haut = pygame.image.load('./Ressources/Serpent/tete_haut.png').convert_alpha()
        self.tete_bas = pygame.image.load('./Ressources/Serpent/tete_bas.png').convert_alpha()
        self.tete_gauche = pygame.image.load('./Ressources/Serpent/tete_gauche.png').convert_alpha()
        self.tete_droite = pygame.image.load('./Ressources/Serpent/tete_droite.png').convert_alpha()

        self.queue_haut = pygame.image.load('./Ressources/Serpent/queue_haut.png').convert_alpha()
        self.queue_bas = pygame.image.load('./Ressources/Serpent/queue_bas.png').convert_alpha()
        self.queue_gauche = pygame.image.load('./Ressources/Serpent/queue_gauche.png').convert_alpha()
        self.queue_droite = pygame.image.load('./Ressources/Serpent/queue_droite.png').convert_alpha()

        self.corps_vertical = pygame.image.load('./Ressources/Serpent/corps_vertical.png').convert_alpha()
        self.corps_horizontal = pygame.image.load('./Ressources/Serpent/corps_horizontale.png').convert_alpha()

        self.corps_haut_droite = pygame.image.load('./Ressources/Serpent/corps_haut_droite.png').convert_alpha()
        self.corps_haut_gauche = pygame.image.load('./Ressources/Serpent/corps_haut_gauche.png').convert_alpha()
        self.corps_bas_droite = pygame.image.load('./Ressources/Serpent/corps_bas_droite.png').convert_alpha()
        self.corps_bas_gauche = pygame.image.load('./Ressources/Serpent/corps_bas_gauche.png').convert_alpha()

        # SON
        self.son_manger = pygame.mixer.Sound('./Ressources/Sons/manger.mp3')

    def dessinerSerpent(self):
        self.teteGraphisme()
        self.queueGraphisme()

        for index, block in enumerate(self.corps):
            xPos = int(block.x * tailleCellule)
            yPos = int(block.y * tailleCellule)

            block_rect = pygame.Rect(xPos, yPos, tailleCellule, tailleCellule)

            if index == 0:
                screen.blit(self.tete, block_rect)
            elif index == len(self.corps) - 1 :
                screen.blit(self.queue, block_rect)
            else:
                block_precedent = self.corps[index + 1] - block
                block_suivant = self.corps[index - 1] - block
                if block_precedent.x == block_suivant.x:
                    screen.blit(self.corps_vertical, block_rect)
                elif block_precedent.y == block_suivant.y:
                    screen.blit(self.corps_horizontal, block_rect)
                else:
                    if ((block_precedent.x == -1) and (block_suivant.y == -1)) or ((block_precedent.y == -1) and (block_suivant.x == -1)):
                        screen.blit(self.corps_haut_gauche, block_rect)
                    elif ((block_precedent.x == -1) and (block_suivant.y == 1)) or ((block_precedent.y == 1) and (block_suivant.x == -1)):
                        screen.blit(self.corps_bas_gauche, block_rect)
                    elif ((block_precedent.x == 1) and (block_suivant.y == -1)) or ((block_precedent.y == -1) and (block_suivant.x == 1)):
                        screen.blit(self.corps_haut_droite, block_rect)
                    elif ((block_precedent.x == 1) and (block_suivant.y == 1)) or ((block_precedent.y == 1) and (block_suivant.x == 1)):
                        screen.blit(self.corps_bas_droite, block_rect)


    def teteGraphisme(self):
        relation_tete = self.corps[1] - self.corps[0]
        if relation_tete == Vector2(1, 0): self.tete = self.tete_gauche
        elif relation_tete == Vector2(-1, 0): self.tete = self.tete_droite
        elif relation_tete == Vector2(0, 1): self.tete = self.tete_haut
        elif relation_tete == Vector2(0, -1): self.tete = self.tete_bas

    def queueGraphisme(self):
        relation_queue = self.corps[-2] - self.corps[-1]
        if relation_queue == Vector2(1, 0): self.queue = self.queue_gauche
        elif relation_queue == Vector2(-1, 0): self.queue = self.queue_droite
        elif relation_queue == Vector2(0, 1): self.queue = self.queue_haut
        elif relation_queue == Vector2(0, -1): self.queue = self.queue_bas


    def mouvementSerpent(self):
        if self.nouveauBlock == True:
            copie_corps = self.corps[:]
            copie_corps.insert(0, copie_corps[0] + self.direction)
            self.corps = copie_corps[:]
            self.nouveauBlock = False
        else:
            copie_corps = self.corps[:-1]
            copie_corps.insert(0, copie_corps[0] + self.direction)
            self.corps = copie_corps[:]


    def ajouterBlock(self):
        self.nouveauBlock = True

    def lireSons(self):
        self.son_manger.play()

    def repeter(self):
        self.corps = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class Fruit:
    def __init__(self):
        self.aleatoire()
        # Créer une position x et y
        # dessiner un carré

    def dessinerFruit(self):
        fruit_rectangle = pygame.Rect(int(self.position.x * tailleCellule), int(self.position.y * tailleCellule), tailleCellule, tailleCellule)
        screen.blit(pomme, fruit_rectangle)
        #pygame.draw.ellipse(screen, (126, 10, 10), fruit_rectangle)
        # Créer un rectangle
        # Dessiner le rectangle

    def aleatoire(self):
        self.x = random.randint(0, nombreCellule - 1)
        self.y = random.randint(0, nombreCellule - 1)
        self.position = Vector2(self.x, self.y)



class Main:
    def __init__(self):
        self.serpent = Serpent()
        self.fruit = Fruit()

    def update(self):
        self.serpent.mouvementSerpent()
        self.verifierCollision()
        self.verifierGameOver()

    def dessinerElements(self):
        self.dessinerGazon()
        self.fruit.dessinerFruit()
        self.serpent.dessinerSerpent()
        self.ecrireScore()

    def verifierCollision(self):
        if self.fruit.position == self.serpent.corps[0]:
            self.fruit.aleatoire() # repositionner le fruit
            self.serpent.ajouterBlock()
            self.serpent.lireSons()

        for block in self.serpent.corps[1:]:
            if block == self.fruit.position:
                self.fruit.aleatoire()



    def verifierGameOver(self):
        # Tester si le serpent touche les bords
        if (not 0 <= self.serpent.corps[0].x < nombreCellule) or (not 0 <= self.serpent.corps[0].y < nombreCellule):
            self.gameOver()

        # Tester si la tête touche le corps
        for block in self.serpent.corps[1:]:
            if block == self.serpent.corps[0]:
                self.gameOver()
    def gameOver(self):
        self.serpent.repeter()

    def dessinerGazon(self):
        couleur_gazon = (167, 209, 61)

        for ligne in range(nombreCellule):
            if ligne % 2 == 0:
                for colomne in range(nombreCellule):
                    if colomne % 2 == 0:
                        gazon_rect = pygame.Rect(colomne * tailleCellule, ligne * tailleCellule, tailleCellule, tailleCellule)
                        pygame.draw.rect(screen, couleur_gazon, gazon_rect)
                else:
                    for colomne in range(nombreCellule):
                        if colomne % 2 == 0:
                            gazon_rect = pygame.Rect(colomne * tailleCellule, ligne * tailleCellule, tailleCellule,
                                                     tailleCellule)
                            pygame.draw.rect(screen, couleur_gazon, gazon_rect)
            else:
                for colomne in range(nombreCellule):
                    if colomne % 2 != 0:
                        gazon_rect = pygame.Rect(colomne * tailleCellule, ligne * tailleCellule, tailleCellule,
                                                 tailleCellule)
                        pygame.draw.rect(screen, couleur_gazon, gazon_rect)

    def ecrireScore(self):
        score_text = str(len(self.serpent.corps) - 3)
        score_surface = jeu_font.render(score_text, True, (56, 74, 12))
        scoreX = int(tailleCellule * nombreCellule - 60)
        scoreY = int(tailleCellule * nombreCellule - 40)
        score_rect = score_surface.get_rect(center = (scoreX, scoreY))
        pomme_rect = pomme.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(pomme_rect.left, pomme_rect.top, pomme_rect.width + score_rect.width + 6, pomme_rect.height + 8)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(pomme, pomme_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
tailleCellule = 30
nombreCellule = 20
screen = pygame.display.set_mode((nombreCellule * tailleCellule, nombreCellule * tailleCellule))
horloge = pygame.time.Clock()
pomme = pygame.image.load('./Ressources/apple.png').convert_alpha()

# POUR LE SCORE
jeu_font = pygame.font.Font('./Ressources/Polices/Franchise.ttf', 30)

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)

jeu = Main()
while True:
    # Afficher tous les éléments
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            jeu.update()

        if event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_UP:
                if jeu.serpent.direction.y != 1:
                    jeu.serpent.direction = Vector2(0, -1)
            if event.key  == pygame.K_DOWN:
                if jeu.serpent.direction.y != -1:
                    jeu.serpent.direction = Vector2(0, 1)
            if event.key  == pygame.K_RIGHT:
                if jeu.serpent.direction.x != -1:
                    jeu.serpent.direction = Vector2(1, 0)
            if event.key  == pygame.K_LEFT:
                if jeu.serpent.direction.x != 1:
                    jeu.serpent.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70)) # Changer la couleur de l'écran
    jeu.dessinerElements()
    pygame.display.update()
    horloge.tick(60)