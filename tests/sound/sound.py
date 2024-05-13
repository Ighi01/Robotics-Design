import pygame
from time import sleep

pygame.mixer.init(channels=2)
right_channel = pygame.mixer.Channel(0)
right_channel.set_volume(1.0, 0.0)
left_channel = pygame.mixer.Channel(1)
left_channel.set_volume(0.0, 1.0)

sound = pygame.mixer.Sound("sample-6s.wav")

right_channel.play(sound)
sleep(1)
left_channel.play(sound)
sleep(8)