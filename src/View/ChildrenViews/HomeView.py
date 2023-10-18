from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.HomeViewCtrl import *
from dotenv import load_dotenv
load_dotenv()

#Класс-вьювер для отображения домашнего окна 
class HomeView(BaseView):
    __default_parametres_BD = {
        'host':os.getenv('DB_HOST'),
        'user':os.getenv('DB_USER'),
        'password':os.getenv('DB_PASSWORD'),
        'database':os.getenv('DB_NAME'),
        'port':os.getenv('DB_PORT')
    }

    def __connect_btn_clicked(self):
        host = self.name_host.get()
        user = self.name_user.get()
        password = self.name_password.get()
        database = self.name_database.get()
        port = self.name_port.get()
        self.homeviewControl.connectToBD(host, user, password, database, port)

    def __action_btn_clicked(self):
        name = self.nametable_combobox.get()
        if self.creatOfDelete.get() == 1:
            self.homeviewControl.create_table(name)
        elif self.creatOfDelete.get() == 2:
            self.homeviewControl.drop_table(name)
        elif self.creatOfDelete.get() == 3:
            self.homeviewControl.clear_table(name)
        elif self.creatOfDelete.get() == 4:
            self.homeviewControl.export_table(name)
        else: 
            self.homeviewControl.recordConsole("Ошибка, не выбрано действие\n\n")

    def __create_and_pack_elements(self):
        #Расположение элементов подключения базы данных
        root_label1 = tkinter.Label(self.left_frame, text="Подключение\n к базе данных", bg=self.leftBG,
                                    font=("Bold", 13))
        root_label1.pack(pady=[50, 10])

        self.name_host = tkinter.Entry(self.left_frame)
        self.name_host.pack(pady=[5, 0])
        self.name_host.insert(0, self.__default_parametres_BD['host'])
        label1 = tkinter.Label(self.left_frame, text="Имя хоста", bg=self.leftBG)
        label1.pack(pady=[0, 5])
        
        self.name_user = tkinter.Entry(self.left_frame)
        self.name_user.pack(pady=[5, 0], fill='x', padx=5)
        self.name_user.insert(0, self.__default_parametres_BD['user'])
        label2 = tkinter.Label(self.left_frame, text="Имя пользователя", bg=self.leftBG)
        label2.pack(pady=[0, 5])
        
        self.name_password = tkinter.Entry(self.left_frame)
        self.name_password.pack(pady=[5, 0], fill='x', padx=5)
        self.name_password.insert(0, self.__default_parametres_BD['password'])
        label3 = tkinter.Label(self.left_frame, text="Пароль", bg=self.leftBG)
        label3.pack(pady=[0, 5])
        
        self.name_database = tkinter.Entry(self.left_frame)
        self.name_database.pack(pady=[5, 0], fill='x', padx=5)
        self.name_database.insert(0, self.__default_parametres_BD['database'])
        label4 = tkinter.Label(self.left_frame, text="Имя базы данных", bg=self.leftBG)
        label4.pack(pady=[0, 5])
        
        self.name_port = tkinter.Entry(self.left_frame)
        self.name_port.pack(pady=[5, 0], fill='x', padx=5)
        self.name_port.insert(0, self.__default_parametres_BD['port'])
        label5 = tkinter.Label(self.left_frame, text="Имя порта (4 цифры)", bg=self.leftBG)
        label5.pack(pady=[0, 5])

        self.connect_btn = tkinter.Button(self.left_frame, text="Подключиться", command=self.__connect_btn_clicked)
        self.connect_btn.pack(fill='x', pady=5, padx=5)
        self.disconnect_btn = tkinter.Button(self.left_frame, text="Отключится", command=lambda:self.homeviewControl.disconnectFromBD())
        self.disconnect_btn.pack(fill='x', pady=5, padx=5)

        #Расположение элементов домашней страницы
        label6 = tkinter.Label(self.right_frame, text="Название таблицы", font=("Bold", 13))
        label6.pack(pady=3)
        self.nametable_combobox = tkinter.ttk.Combobox(self.right_frame, values=self.homeviewControl.set_tables_combobox(),
                                              postcommand=lambda: self.nametable_combobox.configure(values=self.homeviewControl.set_tables_combobox()))
        self.nametable_combobox.pack(pady=3, fill="x", padx=5)

        radio_frame = tkinter.Frame(self.right_frame)
        radio_frame.pack(fill="x", padx=3, pady=3)
        self.creatOfDelete = tkinter.IntVar()
        create_radio = tkinter.Radiobutton(radio_frame, text="Создание", variable=self.creatOfDelete, value=1)
        create_radio.pack(side="left", padx=5)
        delete_radio = tkinter.Radiobutton(radio_frame, text="Удаление", variable=self.creatOfDelete, value=2)
        delete_radio.pack(side="left", padx=5)
        deleteRows_radio = tkinter.Radiobutton(radio_frame, text="Очистка", variable=self.creatOfDelete, value=3)
        deleteRows_radio.pack(side="left", padx=5)
        export_radio = tkinter.Radiobutton(radio_frame, text="Экспорт", variable=self.creatOfDelete, value=4)
        export_radio.pack(side="left", padx=5)

        self.action_table_btn = tkinter.Button(self.right_frame, text="Выполнить действие с таблицей", command=self.__action_btn_clicked)
        self.action_table_btn.pack(fill='x', pady=3, padx=5)

        buttons_frame = tkinter.Frame(self.right_frame)
        buttons_frame.place(y=120, relx=0.01, relwidth=0.98, height=27)
        show_tables_btn = tkinter.Button(buttons_frame, text="Вывести все таблицы", command=self.homeviewControl.show_tables)
        show_tables_btn.place(relx=0, rely=0, relheight=1, relwidth=0.49)
        clear_console_btn = tkinter.Button(buttons_frame, text="Очистить консоль", command=self.homeviewControl.clear_console)
        clear_console_btn.place(relx=0.51, rely=0, relheight=1, relwidth=0.49)

    def __init__(self):
        super().__init__()
        self.homeviewControl = HomeViewCtrl(self.console)
        self.__create_and_pack_elements()