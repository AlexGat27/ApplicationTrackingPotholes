from src.Database.Queryes import SyncCore
import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog

#Базовый класс-контроллер для инициализации функций на всех страницах и связи страниц
class BaseCtrl():
    leftBG = '#E1E7E5' #hex-код цвета левого фрейма

    def __init__(self, console):
        self.console = console
        self.database = SyncCore()

    #Запись сообщения в консоль
    def recordConsole(self, message):
         self.console.config(state="normal")
         self.console.insert(tkinter.END, message)
         self.console.config(state="disabled")

    #Очистка консоли
    def clear_console(self):
         self.console.config(state='normal')
         self.console.delete('1.0', tkinter.END)
         self.console.config(state='disabled')

    #Проверка подключения к базе данных
    def checkConnectionBD(self):
        if  self.database.isConnect:
            return True
        else:
            self.recordConsole("Ошибка. База данных не подключена\n\n")
            return False

    #Демонстрация сущесвтующих таблиц в консоли
    def show_tables(self):
        if not(self.checkConnectionBD()):
            return None
        
        tables =  self.database._getTables()[1]
        if len(tables) == 0:
            self.recordConsole("Таблиц в базе данных не существует\n\n")
            return None
        table_stroka = ''
        for i in tables:
            table_stroka += '{} '.format(i)
        self.recordConsole("Таблицы в базе данных:\n" + table_stroka + "\n\n") 

    #Помещения сущесвтующих таблиц 
    def set_tables_combobox(self):
        if not(self.database.isConnect):
            return None
        return self.database.getTables()[1]

