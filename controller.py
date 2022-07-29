from PyQt5 import QtWidgets
import os


def message(title, text):
    box = QtWidgets.QMessageBox()
    box.setWindowTitle(title)
    box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    box.setText(text)

    box.setIcon(QtWidgets.QMessageBox.Information)

    return box


def get_value(object):
    if isinstance(object, QtWidgets.QCheckBox):
        return object.isChecked()
    if isinstance(object, QtWidgets.QDoubleSpinBox):
        return object.value()
    if isinstance(object, QtWidgets.QLineEdit):
        return object.text()
    if isinstance(object, QtWidgets.QComboBox):
        return object.currentText()


def set_value(object, value, combo_element='cur'):
    if isinstance(object, QtWidgets.QCheckBox):
        return object.setChecked(value)
    if isinstance(object, QtWidgets.QDoubleSpinBox):
        return object.setValue(value)
    if isinstance(object, QtWidgets.QLineEdit):
        return object.setText(value)
    if isinstance(object, QtWidgets.QComboBox):
        if combo_element == 'cur':
            return object.setCurrentText(value)
        if combo_element == 'all':
            object.clear()
            return object.insertItems(0, value)
        if combo_element == 'new':
            return object.insertItem(0, value)


def check_folder(folder):
    cwd = os.getcwd()
    direct = os.path.join(cwd, folder)
    if not os.path.exists(direct): os.mkdir(direct)


def setup_folders():
    check_folder("Voice")
    check_folder("Showcases")
    check_folder("Music")
    check_folder("TransitionMusic")
    check_folder("TransitionPreview")