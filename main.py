from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from gui import Ui_GMDEditor
from logic import MainLogic
import sys
import os
import json

class GMDEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(GMDEditor, self).__init__()

        self.logic = MainLogic()

        self.ui = Ui_GMDEditor()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        self.ui.foldersButton.clicked.connect(self.setup_folders)
        self.ui.startButton.clicked.connect(self.start_logic)

        if os.path.exists('parameters.json'):
            with open('parameters.json', 'r', encoding='utf-8') as f:
                s = json.load(f)

                self.ui.addTransitionsCheck.setChecked(s['is_transition'])
                self.ui.fadeSpeedSpin.setValue(s['fade_speed'])
                self.ui.transitionDurationSpin.setValue(s['transition_duration'])
                self.ui.showcaseSizeSpin.setValue(s['showcase_scale'])
                self.ui.showcaseSpeedSpin.setValue(s['showcase_speed'])
                self.ui.musicVolumeSpin.setValue(s['music_volume'])
                self.ui.voiceVolumeSpin.setValue(s['voice_volume'])
                self.ui.audioNameLine.setText(s['audio_name'])
                self.ui.videoNameLine.setText(s['video_name'])
                self.ui.videoQualityCombo.setCurrentText(str(s['height']))
                self.ui.videoFPSCombo.setCurrentText(str(s['fps']))

                f.close()



    def check_folder(self, folder):
        cwd = os.getcwd()
        direct = os.path.join(cwd, folder)
        if not os.path.exists(direct): os.mkdir(direct)

    def setup_folders(self):
        self.check_folder("Voice")
        self.check_folder("Showcases")
        self.check_folder("Music")
        self.check_folder("TransitionMusic")
        self.check_folder("TransitionPreview")

    def start_logic(self):
        self.logic.is_transition = self.ui.addTransitionsCheck.isChecked()
        self.logic.fade_speed = self.ui.fadeSpeedSpin.value()
        self.logic.transition_duration = self.ui.transitionDurationSpin.value()
        self.logic.showcase_scale = self.ui.showcaseSizeSpin.value()
        self.logic.showcase_speed = self.ui.showcaseSpeedSpin.value()
        self.logic.music_volume = self.ui.musicVolumeSpin.value()
        self.logic.voice_volume = self.ui.voiceVolumeSpin.value()
        self.logic.add_audio = self.ui.audioOutCheck.isChecked()
        self.logic.add_video = self.ui.videoOutCheck.isChecked()
        self.logic.audio_name = self.ui.audioNameLine.text()
        self.logic.video_name = self.ui.videoNameLine.text()
        self.logic.height = int(self.ui.videoQualityCombo.currentText())
        self.logic.fps = int(self.ui.videoFPSCombo.currentText())

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
                'fps': self.logic.fps
            }))
            wf.close()

        result = QtWidgets.QMessageBox()
        result.setWindowTitle("Result")
        result.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result.setText(self.logic.main())

        if result.text() == "Done!":
            result.setIcon(QtWidgets.QMessageBox.Information)
        else:
            result.setIcon(QtWidgets.QMessageBox.Critical)

        result.exec_()


app = QtWidgets.QApplication(sys.argv)
app.setStyle('Windows')
application = GMDEditor()
application.show()

sys.exit(app.exec())