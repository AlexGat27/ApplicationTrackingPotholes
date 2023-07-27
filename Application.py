import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
from Support_files.potholeDetectionProcess import *
from Support_files.Database import *


class App(tkinter.Tk):
    """Класс приложения"""
    TITLE = "Geosystem"

    #Конфигурация окна
    def _configure_window(self):
        self.title(self.__class__.TITLE)
        self.geometry("650x500+1000+100") 
        self.resizable(False, False)

    #Запись в консоль сообщения
    def recordConsole(self, record):
        self.console.config(state="normal")
        self.console.insert(tkinter.END, record)
        self.console.config(state="disabled")

    def checkConnectionBD(self):
        if self.database.isConnect:
            return True
        else:
            self.recordConsole("Ошибка. База данных не подключена\n\n")
            return False

    #Функция записи в таблицу
    def __recordimg_into_table(self, name):
        if self.database.isInDatabase(name):
            directory = tkinter.filedialog.askdirectory()
            media = os.listdir(directory)
            self.recordConsole("Идет процесс обработки папки с фото...\n")
            for med in media:
                image_path = os.path.join(directory, med).replace(os.sep, '/')
                succes = self.mediaProcess.imageProcessing(self.model, image_path, self.database, name)
                if succes: self.recordConsole("Фото {} обработано успешно\n".format(med))
                else: self.recordConsole("Ошибка обработки фото {}, такого разрешения не существует \n".format(med))
            self.recordConsole("Запись в таблицу {} совершена успешно\n\n".format(name))
        else:
            self.recordConsole("Ошибка, таблицы {} не существует\n\n".format(name))

    def __recordvid_into_table(self, name):
        if self.database.isInDatabase(name):
            video_path = tkinter.filedialog.askopenfilename()
            self.recordConsole("Идет процесс обработки видео...\n")
            succes = self.mediaProcess.videoProcessing(self.model, video_path, self.database, name)
            if succes: self.recordConsole("Запись видео {} в таблицу {} совершена успешно\n\n".format(video_path.split('/')[-1], name))
        else:
            self.recordConsole("Ошибка, таблицы {} не существует\n\n".format(name))


    def __export_table(self, name):
        path = tkinter.filedialog.askdirectory()
        self.database.export_table(path, name)
        self.recordConsole("Успешный экспорт таблицы {}\n\n".format(name))

    def __clear_table(self, name):
        succesful = self.database.clear_table(name)
        if succesful:
            self.recordConsole("Данные таблицы {} удалены\n\n".format(name))
        else:
            self.recordConsole("Данной таблицы не существует\n\n")

    def __buttons11_clicked(self):
        if not(self.database.isConnect):
            _host = self.name_host.get()
            _user = self.name_user.get()
            _password = self.name_password.get()
            _database = self.name_database.get()
            _port = self.name_port.get()
            result_connection = self.database.connect_to_bd(_host, _user, _password, _database, _port)
            self.recordConsole(result_connection + "\n\n")
        else:
            self.recordConsole("База данных уже подключена\n\n")

    def __buttons12_clicked(self):
        if not(self.checkConnectionBD()):
            return None
        self.database.disconnect_from_bd()
        self.recordConsole("Успешное отключение от базы данных\n\n")

    #Обработка нажатия кнопки выполнить действие с таблицей
    def __buttons2_clicked(self):
        if not(self.checkConnectionBD()):
            return None
        
        name = self.name_table.get()
        if self.creatOfDelete.get() == 1:
            self.database.create_table(name)
            self.recordConsole("Всевозможные таблицы созданы\n\n")
        elif self.creatOfDelete.get() == 2:
            self.database.drop_table(name)
            self.recordConsole("Всевозможные таблицы удалены\n\n")
        elif self.creatOfDelete.get() == 3:
            self.__clear_table(name)
        elif self.creatOfDelete.get() == 4:
            self.__export_table(name)
        elif self.creatOfDelete.get() == 5:
            self.__recordimg_into_table(name)
        elif self.creatOfDelete.get() == 6:
            self.__recordvid_into_table(name)
        else: 
            self.recordConsole("Ошибка, не выбрано действие\n\n")
    
    #Обработка нажатия кнопки вывода списка таблиц
    def __buttons3_clicked(self):
        if not(self.checkConnectionBD()):
            return None
        
        tables = self.database._getTables()[1]
        if len(tables) == 0:
            self.recordConsole("Таблиц в базе данных не существует\n\n")
            return None
        table_stroka = ''
        for i in tables:
            table_stroka += '{} '.format(i)
        self.recordConsole(table_stroka + "\n\n")
    
    #Обработка нажатия кнопки очистки консоли
    def __buttons4_clicked(self):
        self.console.config(state='normal')
        self.console.delete('1.0', tkinter.END)
        self.console.config(state='disabled')

    #Расположение элементов на своих местах
    def _create_and_pack_elements(self):
        pad = 3

        #№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
        root_frame1 = tkinter.Frame(self)
        root_frame1.pack(side="left", pady=pad, fill="both", padx=[15, 10])
        root_frame2 = tkinter.Frame(self)
        root_frame2.pack(side="left", fill="both", expand=True, pady=pad, padx=[10, 15])

        root_label1 = tkinter.Label(root_frame1, text="Подключение к базе данных")
        root_label1.pack(fill="x", pady=[pad, 10])

        self.name_host = tkinter.Entry(root_frame1)
        self.name_host.pack(fill="x", pady=[pad, 0])
        self.name_host.insert(0, Database.default_parametres_BD['host'])
        label1 = tkinter.Label(root_frame1, text="Имя хоста")
        label1.pack(fill="x", pady=[0, 5])
        
        self.name_user = tkinter.Entry(root_frame1)
        self.name_user.pack(fill="x", pady=[pad, 0])
        self.name_user.insert(0, Database.default_parametres_BD['user'])
        label2 = tkinter.Label(root_frame1, text="Имя пользователя")
        label2.pack(fill="x", pady=[0, 5])
        
        self.name_password = tkinter.Entry(root_frame1)
        self.name_password.pack(fill="x", pady=[pad, 0])
        self.name_password.insert(0, Database.default_parametres_BD['password'])
        label3 = tkinter.Label(root_frame1, text="Пароль")
        label3.pack(fill="x", pady=[0, 5])
        
        self.name_database = tkinter.Entry(root_frame1)
        self.name_database.pack(fill="x", pady=[pad, 0])
        self.name_database.insert(0, Database.default_parametres_BD['database'])
        label4 = tkinter.Label(root_frame1, text="Имя базы данных")
        label4.pack(fill="x", pady=[0, 5])
        
        self.name_port = tkinter.Entry(root_frame1)
        self.name_port.pack(fill="x", pady=[pad, 0])
        self.name_port.insert(0, Database.default_parametres_BD['port'])
        label5 = tkinter.Label(root_frame1, text="Имя порта (4 цифры)")
        label5.pack(fill="x", pady=[0, 5])

        self.connect_btn = tkinter.Button(root_frame1, text="Подключиться", command=self.__buttons11_clicked)
        self.connect_btn.pack(fill="x", pady=pad)
        self.connect_btn = tkinter.Button(root_frame1, text="Отключится", command=self.__buttons12_clicked)
        self.connect_btn.pack(fill="x", pady=pad)
        
        #№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№
        root_label2 = tkinter.Label(root_frame2, text="Взаимодействие с таблицей")
        root_label2.pack(fill="x", padx=pad, pady=pad)
        self.name_table = tkinter.Entry(root_frame2)
        self.name_table.pack(fill="x", padx=pad, pady=pad)

        radio_frame1 = tkinter.Frame(root_frame2)
        radio_frame1.pack(fill="x", padx=pad, pady=pad)
        radio_frame2 = tkinter.Frame(root_frame2)
        radio_frame2.pack(fill="x", padx=pad, pady=pad)
        self.creatOfDelete = tkinter.IntVar()
        self.create_radio = tkinter.Radiobutton(radio_frame1, text="Создание", variable=self.creatOfDelete, value=1)
        self.create_radio.pack(side="left", padx=pad, pady=pad)
        self.delete_radio = tkinter.Radiobutton(radio_frame1, text="Удаление", variable=self.creatOfDelete, value=2)
        self.delete_radio.pack(side="left", padx=pad, pady=pad)
        self.deleteRows_radio = tkinter.Radiobutton(radio_frame1, text="Очистка", variable=self.creatOfDelete, value=3)
        self.deleteRows_radio.pack(side="left", padx=pad, pady=pad)
        self.export_radio = tkinter.Radiobutton(radio_frame1, text="Экспорт", variable=self.creatOfDelete, value=4)
        self.export_radio.pack(side="left", padx=pad, pady=pad)
        self.recordimg_radio = tkinter.Radiobutton(radio_frame2, text="Запись фото", variable=self.creatOfDelete, value=5)
        self.recordimg_radio.pack(side="left", padx=pad, pady=pad)
        self.recordvid_radio = tkinter.Radiobutton(radio_frame2, text="Запись видео", variable=self.creatOfDelete, value=6)
        self.recordvid_radio.pack(side="left", padx=pad, pady=pad)
        
        self.create_delete_btn = tkinter.Button(root_frame2, text="Выполнить действие с таблицей", command=self.__buttons2_clicked)
        self.create_delete_btn.pack(fill="x", padx=pad, pady=pad+3)

        show_tables_btn = tkinter.Button(root_frame2, text="Вывести список таблиц", command=self.__buttons3_clicked)
        show_tables_btn.place(relheight=0.07, relwidth=0.5, relx=0, rely=0.92)
        clear_console_btn = tkinter.Button(root_frame2, text="Очистить консоль", command=self.__buttons4_clicked)
        clear_console_btn.place(relheight=0.07, relwidth=0.5, relx=0.5, rely=0.92)
        self.console = tkinter.Text(root_frame2)
        self.console.place(relheight=0.55, relwidth=1, relx=0, rely=0.35)
        self.console.config(state=tkinter.DISABLED)

    #Инициализация класса
    def __init__(self, model):
        super().__init__()
        self.mediaProcess = MediaProcessing()
        self.database = Database()
        self.model = model
        self._configure_window()
        self._create_and_pack_elements()
        

if __name__ == "__main__":
    model = YOLO('Yolo_model/HolesChecker.pt')
    app = App(model)
    app.mainloop()

