import pygame
import sys
import numpy as np
import os

red_1 = pygame.Color('#FF0000')
light_red = pygame.Color('#FFCCCB')
black = pygame.Color('#000000')
red = pygame.Color('#a72525')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
songlist = np.arange(1, 21)
np.random.shuffle(songlist)
playstack = songlist


class Btn:
    def __init__(self, pos, color=red_1, width=100, height=80, status=None):
        self.rect = pygame.Rect(pos, (width, height))
        self.width = width
        self.height = height
        self.pos = pos
        self.color = color
        self.status = status

    def skt(self):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.status == 'previous':
            pygame.draw.polygon(screen, pygame.Color('#ffffff'), (
                (self.pos[0] + self.width / 2 + 40, 520 + 20), (self.pos[0] + self.width / 2 + 40, 520 - 20),
                (self.pos[0] + self.width / 2 - 20, 520)))
            pygame.draw.polygon(screen, pygame.Color('#ffffff'), (
                (self.pos[0] + self.width / 10 * 3 + 40, self.pos[1] + self.height / 2 + 18),
                (self.pos[0] + self.width / 10 * 3 + 40, self.pos[1] + self.height / 2 - 18),
                (self.pos[0] + self.width / 10 * 3 - 20, self.pos[1] + self.height / 2)))
        if self.status == 'next':
            pygame.draw.polygon(screen, pygame.Color('#ffffff'), (
                (self.pos[0] + self.width / 2 - 40, 520 + 20), (self.pos[0] + self.width / 2 - 40, 520 - 20),
                (self.pos[0] + self.width / 2 + 20, 520)))
            pygame.draw.polygon(screen, pygame.Color('#ffffff'), (
                (self.pos[0] + self.width / 10 * 3, self.pos[1] + self.height / 2 + 18),
                (self.pos[0] + self.width / 10 * 3, self.pos[1] + self.height / 2 - 18),
                (self.pos[0] + self.width / 10 * 3 + 60, self.pos[1] + self.height / 2)))
        if self.status == 'play':
            pygame.draw.polygon(screen, pygame.Color('#ffffff'), (
                (self.pos[0] + self.width / 2 - 20, 520 + 25), (self.pos[0] + self.width / 2 - 20, 520 - 25),
                (self.pos[0] + self.width / 2 + 30, 520)))
        if self.status == 'pause':
            pygame.draw.rect(screen, pygame.Color('#ffffff'),
                             pygame.Rect(self.pos[0] + self.width / 2 - 15, self.pos[1] + self.height / 2 - 22, 10, 44),
                             border_radius=5)
            pygame.draw.rect(screen, pygame.Color('#ffffff'),
                             pygame.Rect(self.pos[0] + self.width / 2 + 15, self.pos[1] + self.height / 2 - 22, 10, 44),
                             border_radius=5)

    def tap(self, i):
        self.color = black
        global playstack
        if self.status == 'previous':
            if i != 0:
                i -= 1
        elif self.status == 'next':
            i += 1
            if i == np.size(playstack):
                np.random.shuffle(songlist)
                playstack = np.append(playstack, songlist)

        sng = str(playstack[i]) + '.mp3'
        pygame.mixer.music.load(sng)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        return i


pygame.display.set_caption('Music Player')

font = pygame.font.SysFont('Ariel', 32)

os.chdir('Audio')

playingN = True
j = 0

previous = Btn((250, 480), status='previous')
next = Btn((450, 480), status='next')
play = Btn((350, 480), status='play')

for j in range(np.size(playstack) + 1):
    if j == np.size(playstack):
        np.random.shuffle(songlist)
        playstack = np.append(playstack, songlist)
        screen.fill((light_red))
    song = str(playstack[j]) + '.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() or play.status == 'pause':
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if previous.rect.collidepoint(mouse[0], mouse[1]):
                previous.color = red
                if pygame.mouse.get_pressed()[0]:
                    j = previous.tap(j)
                    song = str(playstack[j]) + '.mp3'
                    if play.status == 'pause':
                        play.color = red_1
                        play.status = 'play'
            else:
                previous.color = red_1

            if next.rect.collidepoint(mouse[0], mouse[1]):
                next.color = red
                if pygame.mouse.get_pressed()[0]:
                    j = next.tap(j)
                    song = str(playstack[j]) + '.mp3'
                    if play.status == 'pause':
                        play.color = red_1
                        play.status = 'play'
            else:
                next.color = red_1

            if play.rect.collidepoint(mouse[0], mouse[1]):
                if play.status == 'play':
                    play.color = red
                elif play.status == 'pause':
                    play.color = red_1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play.status == 'play':
                        play.color = red
                        play.status = 'pause'
                        pygame.mixer.music.pause()
                    elif play.status == 'pause':
                        play.color = red_1
                        play.status = 'play'
                        pygame.mixer.music.unpause()
            else:
                if play.status == 'play':
                    play.color = red_1
                elif play.status == 'pause':
                    play.color = red

            screen.fill((light_red))
            previous.skt()
            next.skt()
            play.skt()
            text = font.render('Currently Playing : ' + song, 0, pygame.Color('#ffffff'))
            screen.blit(text, (screen.get_width() / 2 - 175, 250), )
            pygame.display.update()
