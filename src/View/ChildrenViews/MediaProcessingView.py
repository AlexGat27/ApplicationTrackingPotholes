from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.MediaProcessingCtrl import *

class MediaProcessingView(BaseView):
    __tables = []

    def __set_model(self):
        model_path = tkinter.filedialog.askopenfilename()
        succesful = self.mediaProcessCtrl.set_model(model_path)
        if succesful:
            self.model_entry.config(state="normal")
            self.model_entry.insert(0, model_path.split('/')[-1])
            self.model_entry.config(state="disabled")

    def __action_btn_clicked(self):
        name = self.combobox.get()
        if self.record_change_val.get() == 1:
            self.mediaProcessCtrl.image_into_table(name)
        elif self.record_change_val.get() == 2:
            self.mediaProcessCtrl.video_into_table(name)
        else:
            self.mediaProcessCtrl.recordConsole("Не выбрано действие (обработать фото или видео)\n\n")
    
    def __create_and_pack_elements(self):
        record_radio_frame = tkinter.Frame(self.left_frame, bg=self.leftBG)
        record_radio_frame.place(y=10, relx=0.05, relwidth=0.9, height=140)
        self.record_change_val = tkinter.IntVar()
        image_radio = tkinter.Radiobutton(record_radio_frame, text="Обработка фото", variable=self.record_change_val,
                                           value=1, font=self.default_font, bg=self.leftBG)
        image_radio.pack(pady=[25, 0], side="top")
        video_radio = tkinter.Radiobutton(record_radio_frame, text="Обработка видео", variable=self.record_change_val,
                                           value=2, font=self.default_font, bg=self.leftBG)
        video_radio.pack(pady=[0, 25], side="bottom")

        self.model_frame = tkinter.Frame(self.left_frame, bg=self.leftBG)
        self.model_frame.place(y=160, relwidth=0.9, relx=0.05, height=450)
        model_label = tkinter.Label(self.model_frame, text="Название модели", font=self.default_font, bg=self.leftBG)
        model_label.pack(pady=5, fill="x")
        self.model_entry = tkinter.Entry(self.model_frame)
        self.model_entry.pack(pady=5, fill="x")
        self.model_entry.insert(0, os.listdir('Yolo_model')[0])
        self.model_entry.config(state="disabled")
        set_model_btn = tkinter.Button(self.model_frame, text="Загрузить модель", command=self.__set_model)
        set_model_btn.pack(fill='x', pady=5) 

        label6 = tkinter.Label(self.right_frame, text="Название таблицы", font=self.default_font)
        label6.pack(pady=5, fill="x")
        self.combobox = tkinter.ttk.Combobox(self.right_frame, values=self.__tables,
                                              postcommand=lambda: self.combobox.configure(values=self.mediaProcessCtrl.set_tables_combobox()))
        self.combobox.pack(pady=5, fill="x", padx=5)
        action_table_btn = tkinter.Button(self.right_frame, text="Запиcать в таблицу", command=self.__action_btn_clicked)
        action_table_btn.pack(fill='x', pady=5, padx=5)

        buttons_frame = tkinter.Frame(self.right_frame)
        buttons_frame.place(y=110, relx=0.01, relwidth=0.98, height=30)
        show_tables_btn = tkinter.Button(buttons_frame, text="Вывести все таблицы", command=self.mediaProcessCtrl.show_tables)
        show_tables_btn.place(relx=0, rely=0, relheight=1, relwidth=0.49)
        clear_console_btn = tkinter.Button(buttons_frame, text="Очистить консоль", command=self.mediaProcessCtrl.clear_console)
        clear_console_btn.place(relx=0.51, rely=0, relheight=1, relwidth=0.49)

    def __init__(self):
        super().__init__()
        self.mediaProcessCtrl = MediaProcessingCtrl(self.console)
        self.__create_and_pack_elements()