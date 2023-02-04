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
        self.search_name_pushButton.clicked.connect(self.geocod)
        self.label_error.hide()
        self.spn_el = 0.001

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.spn_el > 0.001:
                self.spn_el -= 0.05
        if event.key() == Qt.Key_PageUp:
            if self.spn_el < 5:
                self.spn_el += 0.05

    def run(self, coordsx='', coordsy='', pt=''):
        try:
            self.label_error.hide()
            if coordsx and coordsy:
                coords1 = coordsx
                coords2 = coordsy
            else:
                coords1 = self.coords1_input_lineEdit.text()
                coords2 = self.coords2_input_lineEdit.text()
            layer = self.layer_comboBox.currentText()
            if layer == 'Схема':
                layer = 'map'
            elif layer == 'Спутник':
                layer = 'sat'
            else:
                layer = 'sat,skl'
            print(pt)
            map_request = f'http://static-maps.yandex.ru/1.x/?ll={coords2},{coords1}' \
                          f'&l={layer}&z=15&size=650,450&spn={self.spn_el},{self.spn_el}{pt}'
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

    def geocod(self):
        address = '+'.join(self.input_name_lineEdit.text().split())

        map_req = 'http://geocode-maps.yandex.ru/1.x/' \
                  f'?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode={address}'
        response = requests.get(map_req).json()
        point = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
        self.run(point[1], point[0], f'&pt={point[0]},{point[1]}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
