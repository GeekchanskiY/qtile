from libqtile.widget.base import InLoopPollText, _TextBox
from libqtile import bar

import subprocess


class VolumeWidget(_TextBox):

    def __init__(self, default_text="N/A", **config):
        _TextBox.__init__(self, text="test", width=bar.CALCULATED, **config)
        self.add_defaults(_TextBox.defaults)
        self.get_volume()

    def get_volume(self):
        volume = subprocess.run(['amixer', '-D', 'pulse', 'sget', 'Master'], capture_output=True).stdout
        volume = str(volume).split(" ")[30]
        self.text = volume
        self.draw()

    def increase_volume(self):
        subprocess.run(["amixer", "-c", "0", "-q", "-D", "pulse", "set", "Master", "2%+"])
        self.get_volume()

    def decrease_volume(self):
        subprocess.run(["amixer", "-c", "0", "-q", "-D", "pulse", "set", "Master", "2%-"])
        self.get_volume()

    def try_test(self):
        self.increase_volume()
