import os
import sys
import requests
from uic.map import Ui_Form

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Example(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.run)
        self.label_error.hide()
        self.spn_el = 0.001

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.spn_el > 0.001:
                self.spn_el -= 0.05
        if event.key() == Qt.Key_PageUp:
            if self.spn_el < 5:
                self.spn_el += 0.05

    def run(self):
        try:
            self.label_error.hide()
            coords1 = self.coords1_input_lineEdit.text()
            coords2 = self.coords2_input_lineEdit.text()
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={coords2},{coords1}' \
                          f'&l=map&z=15&size=650,450&spn={self.spn_el},{self.spn_el}'
            response = requests.get(map_request)
            if response and response.status_code == 200:
                mp = 'map.png'
                with open(mp, 'wb') as file:
                    file.write(response.content)
                self.px = QPixmap('map.png')
                self.map_label.setPixmap(self.px)
                os.remove(mp)
                self.map_label.show()
            else:
                self.label_error.show()
                self.map_label.hide()
        except Exception:
            self.label_error.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
