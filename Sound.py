import const
import pygame

class Sound:
    def __init__(self, asset):
        self.asset = asset
        self.enabled = const.SOUNDENABLED
        self.setVolume(const.SOUNDVOLUME)
        
    def play(self, soundKey):
        if not self.enabled:
            return 

        if soundKey not in self.asset.sounds.keys():
            return
        
        self.asset.sounds[soundKey].play()

    def setVolume(self, volume):
        self.volume = volume

        if not self.enabled:
            return

        pygame.mixer.music.set_volume(self.volume)

    def toggle(self):
        self.enabled = not self.enabled