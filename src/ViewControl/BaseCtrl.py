from src.Database import *
import json
import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog


class BaseCtrl():
    leftBG = '#E1E7E5'

    def __init__(self, console):
        self.console = console
        self.database = Database()

    def recordConsole(self, message):
         self.console.config(state="normal")
         self.console.insert(tkinter.END, message)
         self.console.config(state="disabled")

    def checkConnectionBD(self):
        if  self.database.isConnect:
            return True
        else:
            self.recordConsole("Ошибка. База данных не подключена\n\n")
            return False
        
    def clear_console(self):
         self.console.config(state='normal')
         self.console.delete('1.0', tkinter.END)
         self.console.config(state='disabled')

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
        self.recordConsole(table_stroka + "\n\n") 

    def set_tables_combobox(self):
        if not(self.database.isConnect):
            return None
        return self.database._getTables()[1]

