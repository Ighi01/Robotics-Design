from pygame.mixer import Channel, Sound

from robot.side import Side


class Speaker:
    channel: Channel
    side: Side

    def __init__(self, channel_index: int, side: Side):
        self.channel = Channel(channel_index)
        self.side = side
        if side == Side.LEFT:
            self.channel.set_volume(1, 0)
        else:
            self.channel.set_volume(0, 1)

    def play(self, sound: Sound):
        self.channel.play(sound)

    def play_and_wait(self, sound: Sound):
        self.play(sound)
        while self.channel.get_busy():
            pass
