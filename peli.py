import pygame
import sys
import random
from pygame.locals import *

# Alustaa pygamen

pygame.init()
pygame.font.init()
pygame.mixer.init()

koko = (400,600)
ruutu = pygame.display.set_mode(koko)
pygame.display.set_caption("Hiiri syö lasia -peli")

fontti = pygame.font.SysFont("Ebrima", 25)
fontti2 = pygame.font.SysFont("Ebrima", 60)

tekstivari = (255,255,255)
loppuvari = (150,26,2)

pelaaja = pygame.image.load("pelaaja.png")
lasi = pygame.image.load("lasi.png")
tausta = pygame.image.load("tausta.png")

pelaaja = pygame.transform.scale(pelaaja, (64,64))
lasi = pygame.transform.scale(lasi, (32,32))

pygame.mixer.music.load("taustamusa.mp3")
pygame.mixer.music.play(-1)
bonk = pygame.mixer.Sound("bonk.ogg")

pelx = 170
pely = 450
nopeus = 7
vihunopeus = 3
hp = 5
highscore = 0

vihut = [[100,100],[400,300],[300,0],[100,300], [100,500], [350,500]]

on_kirjoitettu = False

with open("highscore","r") as tiedosto:
    luettu = tiedosto.read()
    highscore = float(luettu)

ajastin = pygame.time.Clock()
FPS = 30
alkuaika = pygame.time.get_ticks()
loppuaika = 0

# Käsittelee tapahtumia
def peruna():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Pelilogiikka
def porkkana():
    # Taustan piirto
    global pelx, pely, hp, highscore, vihunopeus
    ruutu.blit(tausta, (0,0))

    # Pelaajan liikkuminen
    nappaimet = pygame.key.get_pressed()
    if nappaimet[pygame.K_RIGHT]:
        pelx += nopeus
    if nappaimet[pygame.K_LEFT]:
        pelx -= nopeus
    
    if pelx < 40:
        pelx = 40
    if pelx > 296:
        pelx = 296

    # Vihollisten liikkuminen
    for vihu in vihut:
        vihu[1] += vihunopeus
        if vihu[1] > 600:
            vihu[1] = -10
            vihu[0] = random.randint(50, 300)

    # Vihollisten piirto
    for vihu in vihut:
        ruutu.blit(lasi,vihu)
    
    # Kosketuksen tarkistus
    for vihu in vihut:
        if vihu[1] + 32 > pely and vihu[1] < pely + 64:
            if vihu[0] + 32 > pelx and vihu[0] < pelx + 64:
                # KOSKEE!
                bonk.play()
                hp -= 1
                vihu[1] = -160
                vihu[0] = random.randint(50, 300)


    # Tekstin piirto
    teksti = fontti.render("Elämiä jäljellä: " + str(hp), True, tekstivari)
    ruutu.blit(teksti, (60,30))

    aika = pygame.time.get_ticks() - alkuaika
    teksti = fontti.render("Aika: " + str(aika/1000), True, tekstivari)
    ruutu.blit(teksti, (60,60))

    if aika/1000 > highscore:
        highscore = aika/1000

    if aika//1000 % 10 == 0:
        vihunopeus += 0.1

    # Pelaajan piirto
    ruutu.blit(pelaaja, (pelx,pely))
    pygame.display.flip()


# Pelin loppu
def lanttu():
    global on_kirjoitettu, loppuaika

    ruutu.fill(loppuvari)
    teksti = fontti2.render("Hiiri kuoli", True, tekstivari)
    ruutu.blit(teksti, (50,30))
    teksti = fontti2.render("lasin", True, tekstivari)
    ruutu.blit(teksti, (50,90))
    teksti = fontti2.render("yliannos-", True, tekstivari)
    ruutu.blit(teksti, (50,150))
    teksti = fontti2.render("tukseen", True, tekstivari)
    ruutu.blit(teksti, (50,210))

    if not on_kirjoitettu:
        on_kirjoitettu = True
        loppuaika = pygame.time.get_ticks()
        pygame.mixer.music.stop()
        with open("highscore","w") as tiedosto:
            tiedosto.write(str(highscore))

    if pygame.time.get_ticks() - loppuaika > 5000:
        pygame.quit()
        sys.exit()

    teksti = fontti.render("Korkein pistemäärä: " + str(highscore), True, tekstivari)
    ruutu.blit(teksti, (50,350))

    pygame.display.flip()


# Pelin silmukka
while True:
    peruna()
    if hp > 0:
        porkkana()
    else:
        lanttu()
    ajastin.tick(FPS)
