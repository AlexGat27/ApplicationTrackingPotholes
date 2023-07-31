from Python.View.CheckDatabaseView import *
from Python.View.ExcelGeneratorView import *
from Python.View.GraphicMapView import *
from Python.View.MediaProcessingView import *

class App(tkinter.Tk):
    """Класс приложения"""
    TITLE = "Geosystem"
    __text_opt = {'font':('Bold', 12), 'fg':"#00BFFF", 'bg':"#EEE9E9"}
    __default_parametres_BD = {'host':'127.0.0.1', 'user':'postgres', 'password':'Shurikgat2704', 'database':'postgres', 'port':'5432'}

    #Конфигурация окна
    def __configure_window(self):
        self.title(self.__class__.TITLE)
        self.geometry("700x500+1000+100") 
        self.resizable(False, False)

    

    def __create_and_pack_elements(self):
        options_frame = tkinter.Frame(self, bg="#EEE9E9")
        options_frame.pack(side="top")
        options_frame.pack_propagate(False)
        options_frame.configure(width=700, height=30)

        home_btn = tkinter.Button(options_frame, text="Home", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'])
        home_btn.pack(side="left", padx=[50,12])
        checkDatabasePage_btn = tkinter.Button(options_frame, text="CheckPage", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'])
        checkDatabasePage_btn.pack(side="left", padx=12)
        mediaProcessPage_btn = tkinter.Button(options_frame, text="MediaPage", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'])
        mediaProcessPage_btn.pack(side="left", padx=12)
        excelGeneratorPage_btn = tkinter.Button(options_frame, text="ExcelPage", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'])
        excelGeneratorPage_btn.pack(side="left", padx=12)
        graphmapGeneratorPage_btn = tkinter.Button(options_frame, text="GraphicMapPage", font=self.__text_opt['font'],
                                  fg=self.__text_opt['fg'], bd=0, bg=self.__text_opt['bg'])
        graphmapGeneratorPage_btn.pack(side="left", padx=[12,50])

        main_frame = tkinter.Frame(self, highlightthickness=2, highlightbackground="black")
        main_frame.pack(side="top")
        main_frame.pack_propagate(False)
        main_frame.configure(width=700, height=470)

        root_label1 = tkinter.Label(main_frame, text="Подключение к базе данных")
        root_label1.pack(pady=[5, 10])

        self.name_host = tkinter.Entry(main_frame)
        self.name_host.pack(pady=[5, 0])
        self.name_host.insert(0, self.__default_parametres_BD['host'])
        label1 = tkinter.Label(main_frame, text="Имя хоста")
        label1.pack(pady=[0, 5])
        
        self.name_user = tkinter.Entry(main_frame)
        self.name_user.pack(pady=[5, 0])
        self.name_user.insert(0, self.__default_parametres_BD['user'])
        label2 = tkinter.Label(main_frame, text="Имя пользователя")
        label2.pack(pady=[0, 5])
        
        self.name_password = tkinter.Entry(main_frame)
        self.name_password.pack(pady=[5, 0])
        self.name_password.insert(0, self.__default_parametres_BD['password'])
        label3 = tkinter.Label(main_frame, text="Пароль")
        label3.pack(pady=[0, 5])
        
        self.name_database = tkinter.Entry(main_frame)
        self.name_database.pack(pady=[5, 0])
        self.name_database.insert(0, self.__default_parametres_BD['database'])
        label4 = tkinter.Label(main_frame, text="Имя базы данных")
        label4.pack(pady=[0, 5])
        
        self.name_port = tkinter.Entry(main_frame)
        self.name_port.pack(pady=[5, 0])
        self.name_port.insert(0, self.__default_parametres_BD['port'])
        label5 = tkinter.Label(main_frame, text="Имя порта (4 цифры)")
        label5.pack(pady=[0, 5])

        self.connect_btn = tkinter.Button(main_frame, text="Подключиться")
        self.connect_btn.pack(pady=5)
        self.connect_btn = tkinter.Button(main_frame, text="Отключится")
        self.connect_btn.pack(pady=5)

        self.checkDatabaseView = CheckDatabaseView(main_frame)
        self.excelGeneratorView = ExcelGeneratorView(main_frame)
        self.graphMapView = GraphicMapView(main_frame)
        self.mediaProcessView = MediaProcessingView(main_frame)

    #Инициализация класса
    def __init__(self):
        super().__init__()
        self.__configure_window()
        self.__create_and_pack_elements()