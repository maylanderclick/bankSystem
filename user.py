class User:
    def __init__(self, name, count):
        self.username = name
        self.count = count

    def deposit(self, summ):
        self.count = int(self.count) + int(summ)

    def withdraw(self, summ):
        self.count = int(self.count) - int(summ)

    def income(self, p):
        if self.count > 0:
            self.count = int(self.count * (100 + int(p)) / 100)

    def balance(self):
        return self.count
