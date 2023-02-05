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
        self.searchButton2.clicked.connect(self.run2)
        self.label_error.hide()
        self.spn_el = 0.001

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.spn_el > 0.05:
                self.spn_el -= 0.05
        elif event.key() == Qt.Key_PageUp:
            if self.spn_el < 20:
                self.spn_el += 0.05
        elif event.key() == Qt.Key_D:
            self.coords2 = str(float(self.coords2) + 1)
        elif event.key() == Qt.Key_W:
            self.coords1 = str(float(self.coords1) + 1)
        elif event.key() == Qt.Key_A:
            self.coords2 = str(float(self.coords2) - 1)
        elif event.key() == Qt.Key_S:
            self.coords1 = str(float(self.coords1) - 1)
        else:
            self.label_error.hide()
        try:
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={self.coords2},{self.coords1}' \
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

    def run(self):
        try:
            self.coords1 = self.coords1_input_lineEdit.text()
            self.coords2 = self.coords2_input_lineEdit.text()
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={self.coords2},{self.coords1}' \
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

    def run2(self):
        try:
            self.object = self.object_input_lineEdit.text()
            response = requests.get("http://geocode-maps.yandex.ru/1.x/?"
                                    "apikey=40d1649f-0493-4b70-98ba-98533de7710b&"
                                    f"geocode={self.object}&format=json")
            json_response = response.json()
            toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            coords = toponym['Point']['pos']
            coords = coords.split()
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}' \
                          f'&l=map&z=15&size=650,450&spn={self.spn_el},{self.spn_el}' \
                          f'&pt={coords[0]},{coords[1]},flag'
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
