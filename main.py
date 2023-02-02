import sys
import requests
from uic.map import Ui_Form

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPixmap


class Example(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.searchButton.clicked.connect(self.run)

    def run(self):
        coords1 = self.coords_input_lineEdit.text().split(', ')[0]
        coords2 = self.coords_input_lineEdit.text().split(', ')[1]
        map_request = f'http://static-maps.yandex.ru/1.x/?ll={coords2},{coords1}&l=sat&z=15&size=650,450'
        response = requests.get(map_request)
        mp = 'map.png'
        with open(mp, 'wb') as file:
            file.write(response.content)
        self.px = QPixmap('map.png')
        self.map_label.setPixmap(self.px)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
