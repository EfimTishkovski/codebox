import sys                          # обеспечивает доступ к некоторым переменным и функциям, взаимодействующим с интерпретатором python.
from PyQt5.uic import loadUi        # Модуль для работы c ui файлами из Qt Designer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from logik import *


class Main_window(QMainWindow):
    # Подключение действий в основний класс
    def _connectAction(self):
        self.openAction.triggered.connect(self.openfile)
        self.saveAction.triggered.connect(self.saveFile)
    # Действия в меню
    def _createActions(self):
        self.openAction = QAction('Открыть', self)
        self.saveAction = QAction('Сохранить', self)
    # Создание меню
    def _createMenuBar(self):
        menuBar = self.menuBar()
        # File menu
        fileMenu = QMenu("File", self)  # Создание объекта QMenu
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)

    # Функция обработки открытия файла
    def openfile(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Открыть файл', '', '*.txt')[0]   # Получение от пользователя имени файла для открытия
            if filename:
                f = open(filename, 'r', encoding='utf-8')
                with f:
                    data = f.read().strip()     # .strip() отсекает непечатные символы \n, иначе ошибка при считывании данных
                    self.input_textEdit.setText(data)
            self.statusBar().showMessage(f'данные считвны из файла: {filename}.')
        except:
            self.statusBar().showMessage('Ошибка открытия файла')

    # Функция обработки сохранения файла
    def saveFile(self):
        try:
            filename = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', '*txt')[0]   # Получение от пользователя имени файла для сохранения
            if filename:
                outfile = open(filename, 'w', encoding='utf-8')
                data = self.output_textEdit.toPlainText().split('\n')
                with outfile:
                    for line in data:
                        print(line, file=outfile)
            self.statusBar().showMessage(f'данные сохранены в файл:{filename}.')
        except:
            self.statusBar().showMessage('Ошибка сохранения файла')

    def __init__(self):
        super(Main_window, self).__init__()
        loadUi('design_codebox.ui', self)
        self._createActions()        # Подключение дествий в основной функции
        self._createMenuBar()        # Подключение строки меню в основной функции
        self._connectAction()        # Подключение действий при нажатии пунктов меню к основной функции
        self.clear_button_input.clicked.connect(self.clear_input)    # Обработчик кнопки очиски ввода
        self.clear_button_output.clicked.connect(self.clear_output)  # Обработчик кнопки очиски вывода
        self.encode_button.clicked.connect(self.run_encode)          # Обработчик кнопки запуска шифрования
        self.decode_button.clicked.connect(self.run_decode)          # обработчик кнопки запуска дешифровки
        self.Keyfild.setEchoMode(QtWidgets.QLineEdit.Password)       # По умолчанию ключ скрыт
        self.show_key_checkBox.clicked.connect(self.click_password)  # Обработчик смены состяния checkbox "Показать ключ"
        self.statusBar().showMessage('Готов')                        # Вывод сообщения в строке состояния

    # Функция отбражения окна предупреждения о пустом ключе
    def empty_key_messege(self):
        empty_key_box = QMessageBox()
        empty_key_box.setText('Ключ не может быть пустым')
        empty_key_box.setWindowTitle('Внимание!')
        empty_key_box.setIcon(QMessageBox.Warning)
        empty_key_box.exec_()

    # Функция отбражения окна предупреждения о пустом ключе
    def to_len_key_messege(self):
        empty_key_box = QMessageBox()
        empty_key_box.setText('Слишком длинный ключ! Ключ не более 20 символов')
        empty_key_box.setWindowTitle('Внимание!')
        empty_key_box.setIcon(QMessageBox.Warning)
        empty_key_box.exec_()

    # Функция скрытия/отображения ключа
    def click_password(self):
        if self.show_key_checkBox.isChecked():
            self.Keyfild.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.Keyfild.setEchoMode(QtWidgets.QLineEdit.Password)

    # Функция очистки окна ввода
    def clear_input(self):
        self.input_textEdit.clear()
        self.statusBar().showMessage('Готов')

    # Функция очистки окна вывода
    def clear_output(self):
        self.output_textEdit.clear()
        self.statusBar().showMessage('Готов')

    # Функция считывания пароля
    def password_func(self):
        password = self.Keyfild.text()   # Считывание из окна ключа
        if password == '' and self.randomkey_checkBox.isChecked() is False:  # Если поле пустое и флажок не нажат, выводится сообщение
            self.empty_key_messege()
            return password, False
        elif len(password) > 20:
            self.to_len_key_messege()
            return password, False
        elif password == '' and self.randomkey_checkBox.isChecked():      # Если поле пустое и флажок нажат, происходит генерация случайного ключа
            password = random_key(8)                                      # Генерация случайного пароля, длина 8 символов
            self.Keyfild.setText(password)
            return password, True
        else:
            return password, True  # если ключ введён, он считывается

    # Функция запуска шифрования
    def run_encode(self):
        key, flag_key = self.password_func()   # Получения ключа
        if flag_key:
            data = self.input_textEdit.toPlainText()                           # Получение текста из окна ввода
            data_mass = data.split('\n')                                       # Преобразование входных данных в массив, каждый элемент - строка ввода
            encode_data = list(map(lambda x: simple_code(x, key), data_mass))  # Шифрование
            self.output_textEdit.clear()                                       # Очистка выходного окна перед выводом результата
            for line in encode_data:
                line = line + '\n'                           # Добавление переноса строки в строке шифрованного текста
                self.output_textEdit.insertPlainText(line)   # Вывод построчно шифрованного текста
        self.statusBar().showMessage('Шифрование завершено') # Сообщение в статусбаре о завершениии шифрования

    # Функция запуска дешифрования
    def run_decode(self):
        key, flag_key = self.password_func()   # Получения ключа
        if flag_key:
            code_data = self.input_textEdit.toPlainText()  # Получение текста из окна ввода
            data_mass = code_data.split('\n')              # Преобразование входных данных в массив, каждый элемент - строка ввода
            #print(data_mass, type(data_mass))
            decode_data = list(map(lambda x: simple_decode(x, key), data_mass))  # Дешифрование
            self.output_textEdit.clear()              # Очистка выходного окна перед выводом результата
            for line in decode_data:
                line = line + '\n'                          # Добавление переноса строки в строке шифрованного текста
                self.output_textEdit.insertPlainText(line)  # Вывод построчно шифрованного текста
        self.statusBar().showMessage('Дешифровка завершена')

# Запуск приложения
app = QApplication(sys.argv)         # Новый объет приложения экземпляр класса Qtapplication, sys.arg - список аргументов ком. строки
window = Main_window()               # Создание экземпляра класса Main_window
widget = QtWidgets.QStackedWidget()  # Создание объекта класса QtWidgets
widget.addWidget(window)
widget.setWindowTitle('Codebox')     # Заголовок окна
widget.setFixedHeight(650)           # Фиксированная высота окна
widget.setFixedWidth(900)            # Фиксированная высота окна
widget.setWindowIcon(QIcon('Development.png'))
widget.show()                        # Пказать окно на экране
sys.exit(app.exec_())                # Запуск основного цикла приложения sys.exit() гарантирует чистый выход