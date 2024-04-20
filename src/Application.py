from src.View.ChildrenViews.ExcelGeneratorView import ExcelGeneratorView
from src.View.ChildrenViews.MediaProcessingView import MediaProcessingView
from src.View.ChildrenViews.HomeView import HomeView
import tkinter

#Класс приложения, объединяющий все страницы и запускающий главное окно
class App(tkinter.Tk):
    """Класс приложения"""
    TITLE = "Geosystem" 
    _text_opt = {'font':("Comic Sans MS", 13, "bold"), 'fg':"#000000", 'bg':"#EDFEFF"} #Базовые настройки текста
    _winNum = 0 #Текущая открытая страница
    views = [] #Здесь будут располагаться страницы

    #Конфигурация окна
    def __configure_window(self):
        self.title(self.__class__.TITLE)
        self.geometry("700x500+1000+100") 
        self.resizable(False, False)

    #Переключение страниц
    def __switchWindow(self, winNum):
        for view in self.views:
            view.forget()
        self._winNum = winNum
        self.views[self._winNum].tkraise()
        self.views[self._winNum].packFrame()
        print(winNum)

    def __create_and_pack_elements(self):
        options_frame = tkinter.Frame(self, bg=self._text_opt["bg"])
        options_frame.pack(side="top")
        options_frame.pack_propagate(False)
        options_frame.configure(width=700, height=30)

        self.views = [HomeView(), MediaProcessingView(), ExcelGeneratorView()]

        mediaProcessPage_btn = tkinter.Button(options_frame, text="MediaPage", font=self._text_opt['font'],
                                  fg=self._text_opt['fg'], bd=0, bg=self._text_opt['bg'], command=lambda: self.__switchWindow(1))
        mediaProcessPage_btn.pack(side="left", padx=[100,30])
        home_btn = tkinter.Button(options_frame, text="Home", font=self._text_opt['font'],
                                  fg=self._text_opt['fg'], bd=0, bg=self._text_opt['bg'], command=lambda: self.__switchWindow(0))
        home_btn.pack(side="left", padx=100)
        excelGeneratorPage_btn = tkinter.Button(options_frame, text="ExcelPage", font=self._text_opt['font'],
                                  fg=self._text_opt['fg'], bd=0, bg=self._text_opt['bg'], command=lambda: self.__switchWindow(2))
        excelGeneratorPage_btn.pack(side="left", padx=[30, 100])

    #Инициализация класса
    def __init__(self):
        super().__init__()
        self.__configure_window()
        self.__create_and_pack_elements()