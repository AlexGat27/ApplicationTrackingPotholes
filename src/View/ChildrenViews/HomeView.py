from src.View.BaseView import *

class HomeView(BaseView):
    __default_parametres_BD = {'host':'127.0.0.1', 'user':'postgres', 'password':'Shurikgat2704', 'database':'postgres', 'port':'5432'}

    def __create_and_pack_elements(self):
        super().create_and_pack_elements()
        root_label1 = tkinter.Label(self.left_frame, text="Подключение\n к базе данных", bg=self.leftBG,
                                    font=("Bold", 13))
        root_label1.pack(pady=[50, 10])

        self.name_host = tkinter.Entry(self.left_frame)
        self.name_host.pack(pady=[5, 0])
        self.name_host.insert(0, self.__default_parametres_BD['host'])
        label1 = tkinter.Label(self.left_frame, text="Имя хоста", bg=self.leftBG)
        label1.pack(pady=[0, 5])
        
        self.name_user = tkinter.Entry(self.left_frame)
        self.name_user.pack(pady=[5, 0])
        self.name_user.insert(0, self.__default_parametres_BD['user'])
        label2 = tkinter.Label(self.left_frame, text="Имя пользователя", bg=self.leftBG)
        label2.pack(pady=[0, 5])
        
        self.name_password = tkinter.Entry(self.left_frame)
        self.name_password.pack(pady=[5, 0])
        self.name_password.insert(0, self.__default_parametres_BD['password'])
        label3 = tkinter.Label(self.left_frame, text="Пароль", bg=self.leftBG)
        label3.pack(pady=[0, 5])
        
        self.name_database = tkinter.Entry(self.left_frame)
        self.name_database.pack(pady=[5, 0])
        self.name_database.insert(0, self.__default_parametres_BD['database'])
        label4 = tkinter.Label(self.left_frame, text="Имя базы данных", bg=self.leftBG)
        label4.pack(pady=[0, 5])
        
        self.name_port = tkinter.Entry(self.left_frame)
        self.name_port.pack(pady=[5, 0])
        self.name_port.insert(0, self.__default_parametres_BD['port'])
        label5 = tkinter.Label(self.left_frame, text="Имя порта (4 цифры)", bg=self.leftBG)
        label5.pack(pady=[0, 5])

        self.connect_btn = tkinter.Button(self.left_frame, text="Подключиться")
        self.connect_btn.pack(fill='x', pady=5, padx=5)
        self.connect_btn = tkinter.Button(self.left_frame, text="Отключится")
        self.connect_btn.pack(fill='x', pady=5, padx=5)

    def __init__(self):
        super().__init__()
        self.packFrame()
        self.__create_and_pack_elements()