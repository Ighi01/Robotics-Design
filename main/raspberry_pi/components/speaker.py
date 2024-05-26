from pygame.mixer import Channel, Sound

from robot.side import Side


class Speaker:
    channel: Channel
    side: Side
    volume: int

    def __init__(self, channel_index: int, side: Side, volume: int = 100):
        assert 0 <= volume <= 100
        self.channel = Channel(channel_index)
        self.side = side
        self.volume = volume
        if side == Side.LEFT:
            self.channel.set_volume(self.volume / 100, 0)
        else:
            self.channel.set_volume(0, self.volume / 100)

    def play(self, sound: Sound):
        self.channel.play(sound)

    def play_and_wait(self, sound: Sound):
        self.play(sound)
        while self.channel.get_busy():
            pass
