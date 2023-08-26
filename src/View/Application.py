from src.View.ChildrenViews.ExcelGeneratorView import *
from src.View.ChildrenViews.MediaProcessingView import *
from src.View.ChildrenViews.HomeView import *

#Класс приложения, объединяющий все страницы и запускающий главное окно
class App(tkinter.Tk):
    """Класс приложения"""
    TITLE = "Geosystem" 
    __text_opt = {'font':("Comic Sans MS", 13, "bold"), 'fg':"#000000", 'bg':"#EDFEFF"} #Базовые настройки текста
    __winNum = 0 #Текущая открытая страница
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
        self.__winNum = winNum
        self.views[self.__winNum].tkraise()
        self.views[self.__winNum].packFrame()
        print(winNum)

    def __create_and_pack_elements(self):
        options_frame = tkinter.Frame(self, bg=self.__text_opt["bg"])
        options_frame.pack(side="top")
        options_frame.pack_propagate(False)
        options_frame.configure(width=700, height=30)

        self.views = [HomeView(), MediaProcessingView(), ExcelGeneratorView()]

        # checkDatabasePage_btn = tkinter.Button(options_frame, text="CheckPage", font=self.__text_opt['font'],
        #                           fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'], command=lambda: self.__switchWindow(1))
        # checkDatabasePage_btn.pack(side="left", padx=12)
        mediaProcessPage_btn = tkinter.Button(options_frame, text="MediaPage", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'], command=lambda: self.__switchWindow(1))
        mediaProcessPage_btn.pack(side="left", padx=[100,30])
        home_btn = tkinter.Button(options_frame, text="Home", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'], command=lambda: self.__switchWindow(0))
        home_btn.pack(side="left", padx=100)
        excelGeneratorPage_btn = tkinter.Button(options_frame, text="ExcelPage", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'], command=lambda: self.__switchWindow(2))
        excelGeneratorPage_btn.pack(side="left", padx=[30, 100])
        # graphmapGeneratorPage_btn = tkinter.Button(options_frame, text="GraphicMapPage", font=self.__text_opt['font'],
        #                           fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'], command=lambda: self.__switchWindow(4))
        # graphmapGeneratorPage_btn.pack(side="left", padx=[12,50])

    #Инициализация класса
    def __init__(self):
        super().__init__()
        self.__configure_window()
        self.__create_and_pack_elements()