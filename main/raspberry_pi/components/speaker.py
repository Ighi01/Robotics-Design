import pygame

from robot.side import Side


class Speaker:
    side: Side
    volume: int
    channel: pygame.mixer.Channel

    def __init__(self, side: Side, volume: int = 100):
        assert 0 <= volume <= 100
        self.side = side
        self.volume = volume
    
    def start(self, channel_index: int):
        self.channel = pygame.mixer.Channel(channel_index)
        if self.side == Side.LEFT:
            self.channel.set_volume(self.volume / 100, 0)
        else:
            self.channel.set_volume(0, self.volume / 100)
        
    def play(self, sound: str):
        self.channel.play(pygame.mixer.Sound(sound))

    def play_and_wait(self, sound: str):
        self.play(sound)
        while self.channel.get_busy():
            pass
