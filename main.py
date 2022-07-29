from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from design import Ui_GMDEditor
from logic import MainLogic
import controller as c
import download_logic

import sys
import os
import json

class GMDEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(GMDEditor, self).__init__()

        self.logic = MainLogic()

        self.ui = Ui_GMDEditor()
        self.ui.setupUi(self)

        self.ui.foldersButton.clicked.connect(c.setup_folders)
        self.ui.startButton.clicked.connect(self.start_logic)
        self.ui.showcaserNewButton.clicked.connect(self.add_showcaser)
        self.ui.startDownload.clicked.connect(self.download_showcases)

        self.showcasersLinks = ['https://www.youtube.com/channel/UCnkX9Nug4XNQkVPMhqvXJBA', 'https://www.youtube.com/channel/UCZwP1iUQiAKYQp5w-9mJb_w', 'https://www.youtube.com/c/Neiro1999']

        if os.path.exists('parameters.json'):
            with open('parameters.json', 'r', encoding='utf-8') as f:
                s = json.load(f)

                try:
                    c.set_value(self.ui.addTransitionsCheck, s['is_transition'])
                    c.set_value(self.ui.fadeSpeedSpin, s['fade_speed'])
                    c.set_value(self.ui.transitionDurationSpin, s['transition_duration'])
                    c.set_value(self.ui.showcaseSizeSpin, s['showcase_scale'])
                    c.set_value(self.ui.showcaseSpeedSpin, s['showcase_speed'])
                    c.set_value(self.ui.musicVolumeSpin, s['music_volume'])
                    c.set_value(self.ui.voiceVolumeSpin, s['voice_volume'])
                    c.set_value(self.ui.audioNameLine, s['audio_name'])
                    c.set_value(self.ui.videoNameLine, s['video_name'])
                    c.set_value(self.ui.videoQualityCombo, str(s['height']))
                    c.set_value(self.ui.videoFPSCombo, str(s['fps']))

                    c.set_value(self.ui.showcaserChannelsCombo, [download_logic.get_channel_name(i) for i in s['showcasers']], 'all')
                    self.showcasersLinks = [i for i in s['showcasers']]
                except KeyError:
                    pass

                f.close()

    def save_data(self):
        with open('parameters.json', 'w') as wf:
            wf.write(json.dumps({
                'is_transition': self.logic.is_transition,
                'fade_speed': self.logic.fade_speed,
                'transition_duration': self.logic.transition_duration,
                'showcase_scale': self.logic.showcase_scale,
                'showcase_speed': self.logic.showcase_speed,
                'music_volume': self.logic.music_volume,
                'voice_volume': self.logic.voice_volume,
                'audio_name': self.logic.audio_name,
                'video_name': self.logic.video_name,
                'height': self.logic.height,
                'fps': self.logic.fps,
                'showcasers': self.showcasersLinks
            }))
            wf.close()

    def start_logic(self):
        self.logic.is_transition = c.get_value(self.ui.addTransitionsCheck)
        self.logic.fade_speed = c.get_value(self.ui.fadeSpeedSpin)
        self.logic.transition_duration = c.get_value(self.ui.transitionDurationSpin)
        self.logic.showcase_scale = c.get_value(self.ui.showcaseSizeSpin)
        self.logic.showcase_speed = c.get_value(self.ui.showcaseSpeedSpin)
        self.logic.music_volume = c.get_value(self.ui.musicVolumeSpin)
        self.logic.voice_volume = c.get_value(self.ui.voiceVolumeSpin)
        self.logic.add_audio = c.get_value(self.ui.audioOutCheck)
        self.logic.add_video = c.get_value(self.ui.videoOutCheck)
        self.logic.audio_name = c.get_value(self.ui.audioNameLine)
        self.logic.video_name = c.get_value(self.ui.videoNameLine)
        self.logic.height = int(c.get_value(self.ui.videoQualityCombo))
        self.logic.fps = int(c.get_value(self.ui.videoFPSCombo))

        self.save_data()

        result = c.message(title="Result", text=self.logic.main())

        if result.text() == "Done!":
            result.setIcon(QtWidgets.QMessageBox.Information)
        else:
            result.setIcon(QtWidgets.QMessageBox.Critical)

        result.exec_()

    def add_showcaser(self):
        self.showcasersLinks.insert(0, c.get_value(self.ui.showcaserNewLine))
        c.set_value(self.ui.showcaserChannelsCombo, download_logic.get_channel_name(c.get_value(self.ui.showcaserNewLine)), 'new')
        c.set_value(self.ui.showcaserNewLine, "")

        self.ui.showcaserChannelsCombo.setCurrentIndex(0)
        self.save_data()

    def download_showcases(self):
        c.message("Download",
            download_logic.download(
                int(c.get_value(self.ui.downloadMinutesSpin) * 60 + c.get_value(self.ui.downloadSecondsSpin)),
                c.get_value(self.ui.downloadQualityCombo),
                self.showcasersLinks[self.ui.showcaserChannelsCombo.currentIndex()],
                c.get_value(self.ui.showcaserRandomCheck)
            )
        ).exec_()

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Windows')
application = GMDEditor()
application.show()

sys.exit(app.exec())