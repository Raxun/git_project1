import sqlite3
import sys

from datetime import datetime
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QRadioButton, QButtonGroup, QAbstractItemView


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("log_in.ui", self)
        self.btn_create.clicked.connect(self.create_acc)
        self.btn_login.clicked.connect(self.login)
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)

    def create_acc(self):
        self.r = Registration()
        self.r.setFixedSize(690, 320)
        self.r.show()

    def login(self):
        con = sqlite3.connect("games_db.sqlite")
        self.lbl_pass.setText('')
        self.lbl_name.setText('')
        self.lbl_error.setText('')
        cur = con.cursor()
        user_name = self.lineEdit_name.text()
        password = self.lineEdit_pass.text()
        result = cur.execute("""SELECT name_account, password FROM accounts""").fetchall()
        for elem in result:
            if user_name == elem[0] and password == str(elem[-1]):
                self.ex = MyWidget(user_name, password)
                self.ex.setFixedSize(900, 600)
                self.ex.show()
                self.close()
            elif user_name == elem[0] and password != str(elem[-1]):
                self.lbl_pass.setText('Неверный пароль')
            elif user_name != elem[0] and password == str(elem[-1]):
                self.lbl_name.setText('Неверное имя')
            else:
                if self.lbl_pass.text() != 'Неверный пароль' and self.lbl_name.text() != 'Неверное имя' and \
                        elem == result[-1]:
                    self.lbl_error.setText('Такого аккаунта не существует!')


class MyWidget(QMainWindow):
    def __init__(self, user_name, password):
        super().__init__()
        uic.loadUi("main_window.ui", self)
        self.con = sqlite3.connect("games_db.sqlite")

        cur = self.con.cursor()

        self.user_name = user_name
        self.password = password
        self.genre = QButtonGroup()
        self.year = QButtonGroup()
        self.relevance = QButtonGroup()
        self.genre_search = ''
        self.year_search = ''
        self.relevance_search = ''

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
                self.gi.setFixedSize(1300, 900)
                self.gi.show()

    def open_profile(self):
        self.p = Profile(self.user_name, self.password)
        self.p.setFixedSize(1000, 260)
        self.p.show()


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registration.ui', self)
        self.con = sqlite3.connect("games_db.sqlite")
        self.user_name = ''
        self.password = ''
        self.button.clicked.connect(self.create_account)
        self.btn_home.clicked.connect(self.home)
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)

    def create_account(self):
        cur = self.con.cursor()
        name_new_acc = self.lineEdit_name.text()
        password_new_acc = self.lineEdit_pass.text()
        if name_new_acc == '' or password_new_acc == '':
            self.label_4.setText('Ошибка')
        else:
            limit_characters = 3
            whitespace, dash, underscore = 0, 0, 0
            result = cur.execute("""SELECT name_account, password FROM accounts""").fetchall()
            flag_name = True
            flag_password = True
            past_letter = ''
            for element in result:
                if name_new_acc != element[0]:
                    flag_name = True
                else:
                    flag_name = False
            if 1 <= len(name_new_acc) <= 12:
                for letter in name_new_acc:
                    if (97 <= ord(letter) <= 122 or 65 <= ord(letter) <= 90 or 48 <= ord(letter) <= 57) or \
                            (ord(letter) == 32 or ord(letter) == 45 or ord(letter) == 95) or (ord(name_new_acc[-1])
                                                                                              != 32):
                        if ord(letter) == 32:
                            if past_letter != '':
                                if ord(past_letter) == 32:
                                    self.lbl_errorn.setText('Нельзя ставить два пробела подряд')
                                elif letter == name_new_acc[-1]:
                                    self.lbl_errorn.setText('Нельзя ставить пробел в конце')
                            whitespace += 1
                            if whitespace > limit_characters:
                                flag_name = False
                                self.lbl_errorn.setText('Превышен лимит символа пробел, лимит - ' +
                                                        str(limit_characters))
                        elif ord(letter) == 45:
                            dash += 1
                            if dash > limit_characters:
                                flag_name = False
                                self.lbl_errorn.setText('Превышен лимит символа тире, лимит - ' + str(limit_characters))
                        elif ord(letter) == 95:
                            underscore += 1
                            if underscore > limit_characters:
                                flag_name = False
                                self.lbl_errorn.setText('Превышен лимит символа нижнее подчеркивание, лимит - ' +
                                                        str(limit_characters))
                    else:
                        flag_name = False
                        self.lbl_errorn.setText('Разрешено использование только латинский букв, цифр, пробелов, тире, '
                                                + 'нижних подчеркиваний ')
                    past_letter = letter
            else:
                flag_name = False
                self.lbl_errorn.setText('минимум 1 символ, максимум 12')

            if 8 <= len(password_new_acc) <= 12:
                for letter in name_new_acc:
                    if 97 <= ord(letter) <= 122 or 65 <= ord(letter) <= 90 or 48 <= ord(letter) <= 57:
                        pass
                    else:
                        flag_password = False
                        self.lbl_errorp.setText('Разрешено использование только латинских букв и цифр')
            else:
                self.lbl_errorp.setText('Длинна пароля должна быть не менее 8 символов и не более 12')

            if flag_name and flag_password:
                values1 = """INSERT INTO accounts (name_account, password)
                                VALUES (?, ?)"""
                values2 = (name_new_acc, password_new_acc)
                cur.execute(values1, values2)
                self.user_name = name_new_acc
                self.password = password_new_acc
                self.lbl_success.setText('Успешно')
            else:
                self.lbl_success.setText('Ошибка')
            self.con.commit()

    def home(self):
        self.close()


class Profile(QMainWindow):
    def __init__(self, user_name, password):
        super().__init__()
        uic.loadUi('profile.ui', self)
        self.user_name = user_name
        self.password = password
        self.lineEdit_name.setText(self.user_name)
        self.lineEdit_pass.setText(self.password)
        self.changeinfo.clicked.connect(self.change_name)
        self.changeinfo.clicked.connect(self.change_name)

    def change_name(self):
        self.con = sqlite3.connect("games_db.sqlite")
        self.error_name.setText('')
        self.error_pass.setText('')
        cur = self.con.cursor()
        new_name_acc = self.lineEdit_name.text()
        new_password_acc = self.lineEdit_pass.text()

        if new_name_acc == '':
            self.error_name.setText('Пустое поле')
            if new_password_acc == '':
                self.error_pass.setText('Пустое поле')
        else:
            limit_characters = 3
            whitespace, dash, underscore = 0, 0, 0
            result = cur.execute("""SELECT name_account, password FROM accounts""").fetchall()
            flag_name = True
            flag_password = True
            past_letter = ''
            for element in result:
                if new_name_acc != element[0]:
                    flag_name = True
                else:
                    flag_name = False
            if 1 <= len(new_name_acc) <= 12:
                for letter in new_name_acc:
                    if (97 <= ord(letter) <= 122 or 65 <= ord(letter) <= 90 or 48 <= ord(letter) <= 57) or \
                            (ord(letter) == 32 or ord(letter) == 45 or ord(letter) == 95) or (ord(new_name_acc[-1])
                                                                                              != 32):
                        if ord(letter) == 32:
                            if past_letter != '':
                                if ord(past_letter) == 32:
                                    self.error_name.setText('Нельзя ставить два пробела подряд')
                                elif letter == new_name_acc[-1]:
                                    self.error_name.setText('Нельзя ставить пробел в конце')
                            whitespace += 1
                            if whitespace > limit_characters:
                                flag_name = False
                                self.error_name.setText('Превышен лимит символа пробел, лимит - ' +
                                                        str(limit_characters))
                        elif ord(letter) == 45:
                            dash += 1
                            if dash > limit_characters:
                                flag_name = False
                                self.error_name.setText('Превышен лимит символа тире, лимит - ' + str(limit_characters))
                        elif ord(letter) == 95:
                            underscore += 1
                            if underscore > limit_characters:
                                flag_name = False
                                self.error_name.setText('Превышен лимит символа нижнее подчеркивание, лимит - ' +
                                                        str(limit_characters))
                    else:
                        flag_name = False
                        self.error_name.setText('Разрешено использование только латинский букв, цифр, пробелов, тире, '
                                                + 'нижних подчеркиваний ')
                    past_letter = letter
            else:
                flag_name = False
                self.error_name.setText('минимум 1 символ, максимум 12')

            if 8 <= len(new_password_acc) <= 12:
                for letter in new_name_acc:
                    if 97 <= ord(letter) <= 122 or 65 <= ord(letter) <= 90 or 48 <= ord(letter) <= 57:
                        pass
                    else:
                        flag_password = False
                        self.error_pass.setText('Разрешено использование только латинских букв и цифр')
            else:
                self.error_pass.setText('Длинна пароля должна быть не менее 8 символов и не более 12')

            if flag_name and flag_password:
                values1 = """UPDATE accounts SET name_account=? WHERE name_account=?"""
                values2 = (new_name_acc, self.user_name)
                cur.execute(values1, values2)
                self.user_name = new_name_acc
                self.password = new_password_acc
                self.error_pass.setText('Успешно')
                self.error_name.setText('Успешно')

            else:
                self.error_pass.setText('Ошибка')
                self.error_name.setText('Ошибка')
            self.con.commit()

    def close(self):
        self.p = Profile(self.user_name, self.password)
        self.p.show()
        self.close()


class GameInfo(QMainWindow):
    def __init__(self, item, user_name, password):
        super().__init__()
        uic.loadUi("game_info.ui", self)
        self.user_name = user_name
        self.password = password
        self.name_game = item.text()
        self.label_name.setText(self.name_game)
        self.btn_past = ''
        self.listLineEdit = []
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
        self.btn_a.clicked.connect(self.answer_quest)
        self.btn_c.clicked.connect(self.comment)
        self.btn_send.clicked.connect(self.send)
        delegate = AlignDelegate(self.comments)
        self.comments.setItemDelegate(delegate)
        self.con.commit()

    def comment(self):
        self.btn_past = 'comment'
        cur = self.con.cursor()
        result = cur.execute("SELECT name_com, comment, date FROM comments WHERE name_game=?",
                             (self.name_game,)).fetchall()
        self.comments.setRowCount(len(result))
        self.comments.setColumnCount(3)
        self.comments.verticalHeader().hide()
        self.comments.horizontalHeader().hide()
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                item = self.cell(val)
                self.comments.setItem(i, j, item)
        self.comments.horizontalHeader().resizeSection(2, 167)
        self.comments.horizontalHeader().resizeSection(1, 960)
        self.comments.horizontalHeader().resizeSection(0, 160)
        self.comments.itemDoubleClicked.connect(self.del_come)
        self.con.commit()

    def answer_quest(self):
        self.con = sqlite3.connect("games_db.sqlite")
        self.btn_past = 'answer/quest'
        cur = self.con.cursor()
        result = cur.execute("SELECT name_com, question, date,  name_ans, answer, date_ans FROM ans_ques "
                             "WHERE name_game=?",
                             (self.name_game,)).fetchall()

        self.comments.setColumnCount(3)
        self.comments.verticalHeader().hide()
        self.comments.horizontalHeader().hide()
        x = 0
        self.listLineEdit = []
        self.comments.setRowCount(len(result) * 2)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j < 2:
                    item = self.cell(val)
                    self.comments.setItem(x, j, item)
                else:
                    if val != '':
                        if j - 3 == 0:
                            val = 'Ответил: ' + val
                        item = self.cell(val)
                        self.comments.setItem(x + 1, j - 3, item)
                    else:
                        if j - 3 == 0:
                            item = self.cell('Ответить:')
                            self.comments.setItem(x + 1, j - 3, item)
                        elif j - 3 == 1:
                            self.comments.setItem(x + 1, j - 3, QTableWidgetItem('Чтобы дать ответ дважды кликните на'
                                                                                 ' данное поле, затем нажмите "enter"'))
                        elif j - 3 == 2:
                            item = self.cell('Макс. 100 символов')
                            self.comments.setItem(x + 1, j - 3, item)
                        else:
                            item = self.cell(val)
                            self.comments.setItem(x + 1, j - 3, item)
            x += 2
        self.comments.horizontalHeader().resizeSection(2, 167)
        self.comments.horizontalHeader().resizeSection(1, 920)
        self.comments.horizontalHeader().resizeSection(0, 200)
        self.comments.itemChanged.connect(self.send_answer)
        self.con.commit()

    def send_answer(self, item):
        self.con = sqlite3.connect("games_db.sqlite")
        text = item.text()
        cur = self.con.cursor()
        if 1 <= len(text) <= 100:
            result = cur.execute("SELECT id FROM ans_ques WHERE name_game=?",
                                 (self.name_game,)).fetchall()
            for i, elem in enumerate(result):
                if item.row() - 2 == i:
                    datetime_string = str(datetime.now())
                    values1 = """UPDATE ans_ques SET name_ans = ?, answer = ?, date_ans = ? WHERE id = ?"""
                    values2 = (self.user_name, text, datetime_string[:-10], elem[0])
                    cur.execute(values1, values2)
                    #self.answer_quest()
            self.con.commit()

    def cell(self, val):
        item = QTableWidgetItem()
        item.setText(val)
        item.setFlags(Qt.ItemIsEditable)
        return item

    def del_come(self, item):
        cur = self.con.cursor()
        result = cur.execute("""SELECT id, name_com, comment FROM comments""").fetchall()
        for i, elem in enumerate(result):
            if str(item.text()) == str(elem[-1]) and elem[1] == self.user_name:
                del_id = elem[0]
                cur.execute("""DELETE from comments where id = ?""", (del_id, ))
                self.con.commit()
                self.con = sqlite3.connect("games_db.sqlite")
                cur = self.con.cursor()
                result = cur.execute("SELECT name_com, comment, date FROM comments WHERE name_game=?",
                                     (self.name_game,)).fetchall()
                self.comments.setRowCount(len(result))
                for n, element in enumerate(result):
                    for j, val in enumerate(element):
                        self.comments.setItem(n, j, QTableWidgetItem(str(val)))
        self.con.commit()

    def send(self):
        cur = self.con.cursor()
        if self.btn_past == 'comment':
            if self.line_com.text() != 'Максимум 80 символов, минимум 1':
                if 1 <= len(self.line_com.text()) <= 100 and self.line_com.text() != 'Максимум 100 символов':
                    datetime_string = str(datetime.now())
                    values1 = """INSERT INTO comments (name_game, name_com, comment, date)
                                    VALUES (?, ?, ?, ?)"""
                    values2 = (str(self.name_game), str(self.user_name), str(self.line_com.text()),
                               str(datetime_string[:-10]))
                    cur.execute(values1, values2)
                    self.line_com.setText('')
                    self.con.commit()
                else:
                    self.line_com.setText('Максимум 100 символов, минимум 1')
                self.con = sqlite3.connect("games_db.sqlite")
                cur = self.con.cursor()
                result = cur.execute("SELECT name_com, comment, date FROM comments WHERE name_game=?",
                                     (self.name_game,)).fetchall()
                self.comments.setRowCount(len(result))
                for i, elem in enumerate(result):
                    for j, val in enumerate(elem):
                        self.comments.setItem(i, j, QTableWidgetItem(str(val)))
            self.con.commit()
        elif self.btn_past == 'answer/quest':
            if 1 <= len(self.line_com.text()) <= 100 and self.line_com.text() != 'Максимум 100 символов':
                datetime_string = str(datetime.now())
                values1 = """INSERT INTO ans_ques (name_game, name_com, question, date,  name_ans, answer, date_ans)
                                VALUES (?, ?, ?, ?, ?, ?, ?)"""
                values2 = (self.name_game, self.user_name, self.line_com.text(), datetime_string[:-10], '', '', '')
                cur.execute(values1, values2)
                self.line_com.setText('')
                self.con.commit()
            else:
                self.line_com.setText('Максимум 100 символов, минимум 1')
            self.answer_quest()
            self.con.commit()
        else:
            self.line_com.setText('Выберите категорию')

    def home(self):
        self.close()


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.setFixedSize(700, 300)
    ex.show()
    sys.exit(app.exec())
