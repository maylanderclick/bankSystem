import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import Ui_MainWindow
from user import User


class bankSystem (QtWidgets.QMainWindow):
    def __init__(self, User):
        super(bankSystem, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.users = {'Seregina': User('Seregina', 70147540)}
        self.output_inf = []

    def init_UI(self):
        self.setWindowTitle('Система управления счетами клиентов')
        self.ui.input_data.setPlaceholderText('Введите не больше 20 команд')
        self.ui.Calculate.clicked.connect(self.TxtEdit)
        self.ui.Clear.clicked.connect(self.TxtClear)

    def createUser(self, name, count):
        if self.users.get(name) == None:
            self.users[name] = User(name, int(count))
            return True
        return False

    # DEPOSIT name sum
    def deposit(self, args):
        _, name, summ = args

        if not self.createUser(name, summ):
            self.users[name].deposit(summ)

        result = f'{self.users[name].username} {self.users[name].count}\n'
        self.output_inf.append(result)

    # WITHDRAW name sum
    def withdraw(self, args):
        name = args[1]
        summ = int(args[2])

        if not self.createUser(name, 0-summ):
            self.users[name].withdraw(summ)

        result = f'{self.users[name].username} {self.users[name].count}\n'
        self.output_inf.append(result)

    # BALANCE name
    def balance(self, args):
        result = ''
        if len(args) == 1:
            for name in self.users.keys():
                result += f'{self.users[name].username} {self.users[name].balance()}\n'
        if len(args) == 2:
            _, name = args
            if self.users.get(name) == None:
                result += f'{name} NO CLIENT \n'
            else:
                result += f'{self.users[name].username} {self.users[name].balance()}\n'
        self.output_inf.append(result)

    # INCOME p
    def income(self, args):
        _, p = args
        result = ''

        for name in self.users.keys():
            self.users[name].income(p)
            result += f'{self.users[name].username} {self.users[name].count} \n'

        self.output_inf.append(result)

    # TRANSFER name1 name2 sum
    def transfer(self, args):
        _, name1, name2, summ = args

        self.createUser(name1, 0)
        self.createUser(name2, 0)

        self.users[name2].deposit(summ)
        self.users[name1].withdraw(summ)

        result = ''
        result += f'{self.users[name1].username} {self.users[name1].count}\n'
        result += f'{self.users[name2].username} {self.users[name2].count}\n'
        self.output_inf.append(result)

    # Для «очистки» левого и правого полей при нажатии кнопки "Clear"
    def TxtClear(self):
        self.output_inf = []
        self.ui.output_data.clear()
        self.ui.input_data.clear()

    def TxtEdit(self):
        self.input_data = self.ui.input_data.toPlainText()
        print(self.input_data)
        data = self.input_data.split('\n')
        data = list(filter(lambda i: i != '', data))
        print(data)

        if len(data) > 20:
            self.ui.output_data.insertPlainText("Введите не более 20 команд!")
            return

        for line in data:
            args = line.split()
            command = args[0]
            if command == 'DEPOSIT':
                self.deposit(args)
            if command == 'WITHDRAW':
                self.withdraw(args)
            if command == 'BALANCE':
                self.balance(args)
            if command == 'INCOME':
                self.income(args)
            if command == 'TRANSFER':
                self.transfer(args)

        # Вывод результата работы в поле справа
        for output_line in self.output_inf:
            self.ui.output_data.insertPlainText(f'{output_line}\n')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = bankSystem(User)
    application.show()

    sys.exit(app.exec())
