import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QRadioButton, QButtonGroup, QPushButton, QAbstractItemView


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.con = sqlite3.connect("games_db.sqlite")

        cur = self.con.cursor()

        self.genre = QButtonGroup()
        self.year = QButtonGroup()
        self.relevance = QButtonGroup()
        self.genre_search = ''
        self.year_search = ''
        self.relevance_search = ''

        self.user_name = ''
        self.password = ''

        result = cur.execute("""SELECT * FROM genres""").fetchall()
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(len(result) + 1)
        radiobtn = QRadioButton(str('0'))
        self.genre.addButton(radiobtn)
        radiobtn.setText('Все жанры')
        self.tableWidget_2.setCellWidget(0, 0, radiobtn)
        for j, elem in enumerate(result):
            radiobtn = QRadioButton(str(j + 1))
            self.genre.addButton(radiobtn)
            radiobtn.setText(elem[1])
            self.tableWidget_2.setCellWidget(j + 1, 0, radiobtn)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(209)
        self.tableWidget_2.verticalHeader().hide()
        self.tableWidget_2.horizontalHeader().hide()

        result = cur.execute("""SELECT DISTINCT years FROM games
                                ORDER BY years ASC""").fetchall()
        self.tableWidget_3.setColumnCount(1)
        self.tableWidget_3.setRowCount(len(result) + 1)
        radiobtn = QRadioButton(str('0'))
        self.year.addButton(radiobtn)
        radiobtn.setText('Все года')
        self.tableWidget_3.setCellWidget(0, 0, radiobtn)
        for j, elem in enumerate(result):
            radiobtn = QRadioButton(str(j + 1))
            radiobtn.setText(str(elem[0]))
            self.year.addButton(radiobtn)
            self.tableWidget_3.setCellWidget(j + 1, 0, radiobtn)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(209)
        self.tableWidget_3.verticalHeader().hide()
        self.tableWidget_3.horizontalHeader().hide()

        self.tableWidget_4.setColumnCount(1)
        self.tableWidget_4.setRowCount(2)
        sp = ['По возрастанию', 'По убыванию']
        for j in range(2):
            radiobtn = QRadioButton(str(j))
            radiobtn.setText(sp[j])
            self.relevance.addButton(radiobtn)
            self.tableWidget_4.setCellWidget(j, 0, radiobtn)
        self.tableWidget_4.horizontalHeader().setDefaultSectionSize(209)
        self.tableWidget_4.verticalHeader().hide()
        self.tableWidget_4.horizontalHeader().hide()
        self.btn_profile.clicked.connect(self.open_profile)
        self.btn_search.clicked.connect(self.search)
        self.con.commit()

    def search(self):
        if self.lineEdit_search.text() == '   Не найдено!':
            self.lineEdit_search.setText('')
        self.con = sqlite3.connect("games_db.sqlite")
        self.tableWidget_1.setColumnCount(0)
        for button in self.genre.buttons():
            if button.isChecked():
                if button.text() == 'Все жанры':
                    self.genre_search = ''
                else:
                    self.genre_search = button.text()
        for button in self.year.buttons():
            if button.isChecked():
                if button.text() == 'Все года':
                    self.year_search = ''
                else:
                    self.year_search = int(button.text())
        for button in self.relevance.buttons():
            if button.isChecked():
                self.relevance_search = button.text()
        cur = self.con.cursor()
        if self.relevance_search == 'По убыванию':
            result = cur.execute("""SELECT name_game, years, relevance, genre FROM games
                                ORDER BY relevance DESC""").fetchall()
        elif self.relevance_search == 'По возрастанию':
            result = cur.execute("""SELECT name_game, years, relevance, genre FROM games
                                ORDER BY relevance ASC""").fetchall()
        else:
            result = cur.execute("""SELECT name_game, years, relevance, genre FROM games""").fetchall()
        result_genre = cur.execute('''select * from genres''').fetchall()
        self.tableWidget_1.setRowCount(len(result))
        self.tableWidget_1.setColumnCount(4)
        self.tableWidget_1.verticalHeader().hide()
        self.tableWidget_1.horizontalHeader().hide()
        x = 0
        y = 0
        rowcount = 0
        sp = []
        flag_string = True
        for i, elem in enumerate(result):
            if elem[1] == self.year_search or self.year_search == '':
                if elem[0].lower() == self.lineEdit_search.text().lower() or self.lineEdit_search.text() == '':
                    for j, val in enumerate(elem):
                        if val == elem[0]:
                            val = elem[-1]
                            val = val.split()
                            for genre in val:
                                for genres in result_genre:
                                    if genres[0] == int(genre):
                                        sp.append(genres[-1])
                            if self.genre_search not in sp and self.genre_search != '':
                                flag_string = False
                            if flag_string:
                                self.tableWidget_1.setItem(x, 3, QTableWidgetItem(str(', '.join(sp))))
                            sp = []
                        else:
                            if flag_string:
                                if val != elem[-1]:
                                    self.tableWidget_1.setItem(x, y, QTableWidgetItem(str(val)))
                                else:
                                    self.tableWidget_1.setItem(x, 0, QTableWidgetItem(str(elem[0])))
                        y += 1
                        if y == 4 and flag_string:
                            rowcount += 1
                        if y == 1:
                            self.tableWidget_1.setItem(x, 0, QTableWidgetItem(elem[0]))
                else:
                    x -= 1
            else:
                x -= 1
            y = 0
            if flag_string:
                x += 1
            flag_string = True
        self.tableWidget_1.horizontalHeader().setDefaultSectionSize(167)
        if rowcount == 0:
            self.lineEdit_search.setText('   Не найдено!')
        self.tableWidget_1.setRowCount(rowcount)
        self.tableWidget_1.horizontalHeader().resizeSection(2, 55)
        self.tableWidget_1.horizontalHeader().resizeSection(1, 55)
        self.tableWidget_1.horizontalHeader().resizeSection(0, 220)
        self.tableWidget_1.horizontalHeader().resizeSection(3, 317)
        self.tableWidget_1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_1.itemDoubleClicked.connect(self.open_game_info)
        self.con.commit()

    def open_game_info(self, item):
        cur = self.con.cursor()
        result = cur.execute("""SELECT name_game FROM games""").fetchall()
        for i, elem in enumerate(result):
            if item.text() == elem[0]:
                self.gi = GameInfo(item, self.user_name, self.password)
                self.gi.show()

    def open_profile(self):
        if self.user_name != '' and self.password != '':
            self.p = Profile(self.user_name, self.password)
            self.p.show()
        else:
            self.r = Registration(self.user_name, self.password)
            self.r.show()


class Registration(QMainWindow):
    def __init__(self, user_name, password):
        super().__init__()
        uic.loadUi('registration.ui', self)
        self.con = sqlite3.connect("games_db.sqlite")
        self.user_name = user_name
        self.password = password



    def create_account(self):
        print('sdfdf')
        cur = self.con.cursor()
        '''
        name_new_acc = self.lineEdit_name.text()
        password_new_acc = self.lineEdit_pass.text()
        print(name_new_acc, password_new_acc)
        new_acc = cur.execute("""INSERT INTO accounts
                              (name_account, password)
                              VALUES (?, ?)""").fetchall()'''


class Profile(QMainWindow):
    def __init__(self, user_name, password):
        super().__init__()
        uic.loadUi('profile.ui', self)
        self.con = sqlite3.connect("games_db.sqlite")
        self.user_name = user_name
        self.password = password


class GameInfo(QMainWindow):
    def __init__(self, item, user_name, password):
        super().__init__()
        uic.loadUi("game_info.ui", self)
        self.user_name = user_name
        self.password = password
        self.name_game = item.text()
        self.label_name.setText(self.name_game)
        self.con = sqlite3.connect("games_db.sqlite")

        cur = self.con.cursor()

        result = cur.execute("""SELECT * FROM games""").fetchall()

        sp_icon_games = ['Genshin Impact', 'Honkai Impact 3rd', 'The Crew 2', 'Rocket League']

        for i, elem in enumerate(result):
            if elem[1] == self.name_game:
                self.label_image.setText(self.name_game)
                pixmap = QPixmap(elem[-2])
                if self.name_game in sp_icon_games:
                    pixmap = pixmap.scaled(280, 280)
                    self.label_image.move(10, -40)
                else:
                    pixmap = pixmap.scaled(290, 390)
                self.label_image.setPixmap(pixmap)
                self.textBrowser.setText(elem[-1])
        self.btn_home.clicked.connect(self.home)
        self.con.commit()

    def home(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
