from src.Controllers.BaseCtrl import *

#Класс контроллер для домашней страницы
class HomeViewCtrl(BaseCtrl):
    #Подключение к базе данных
    def connectToBD(self, _host, _user, _password, _database, _port):
        if not(self.database.isConnect):
            if _host and _user and _password and _database and _port:
                result_connection = self.database.connect_to_bd(_host, _user, _password, _database, _port)
                self.recordConsole(result_connection + "\n\n")
            else:
                self.recordConsole("Ошибка, введены не все данные\n\n")
        else:
            self.recordConsole("База данных уже подключена\n\n")

    #Отключение от базы данных
    def disconnectFromBD(self):
        if not(self.checkConnectionBD()):
            return None
        self.database.disconnect_from_bd()
        self.recordConsole("Успешное отключение от базы данных\n\n")

    #Очистка таблицы
    def clear_table(self, name):
        if not(self.checkConnectionBD()):
            return None
        succesful = self.database.clear_table(name)
        if succesful:
            self.recordConsole("Данные таблицы {} удалены\n\n".format(name))
        else:
            self.recordConsole("Данной таблицы не существует\n\n")

    #Удаление таблицы
    def drop_table(self, name):
        if not(self.checkConnectionBD()):
            return None
        self.database.drop_table(name)
        self.recordConsole("Всевозможные таблицы удалены\n\n")

    #Создание таблицы
    def create_table(self, name):
        if not(self.checkConnectionBD()):
            return None
        self.database.create_table(name)
        self.recordConsole("Всевозможные таблицы созданы\n\n")

    #Экспорт таблицы
    def export_table(self, name):
        if not(self.checkConnectionBD()):
            return None
        path = tkinter.filedialog.askdirectory()
        self.database.export_table(path, name)
        self.recordConsole("Успешный экспорт таблицы {}\n\n".format(name))