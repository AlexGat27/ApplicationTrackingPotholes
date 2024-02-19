from src.View.BaseView import *
from src.Controllers.PageControllers.MediaProcessingCtrl import *

class MediaProcessingView(BaseView):

    def __action_btn_clicked(self):
        nameTable = self.combobox.get()
        isSaveFrame = self.isSaveFrames.get()
        if self.record_change_val.get() == 1:
            self.mediaProcessCtrl.MediaProcessing(nameTable, 1, isSaveFrame)
        elif self.record_change_val.get() == 2:
            self.mediaProcessCtrl.MediaProcessing(nameTable, 2, isSaveFrame)
        elif self.record_change_val.get() == 3:
            self.mediaProcessCtrl.SplitVideo()
        else:
            self.mediaProcessCtrl.recordConsole("Не выбрано действие (обработать фото или видео)\n\n")
    
    def __create_children_elements(self):
        record_radio_frame = tkinter.Frame(self.left_frame, bg=self.leftBG)
        record_radio_frame.place(y=10, relx=0.05, relwidth=0.9, height=150)
        self.record_change_val = tkinter.IntVar()
        image_radio = tkinter.Radiobutton(record_radio_frame, text="Обработка фото", variable=self.record_change_val,
                                           value=1, font=self.heading_font, bg=self.leftBG)
        image_radio.pack(pady=[25, 0], side="top")
        video_radio = tkinter.Radiobutton(record_radio_frame, text="Обработка видео", variable=self.record_change_val,
                                           value=2, font=self.heading_font, bg=self.leftBG)
        video_radio.pack(pady=[0, 0], side="top")
        video_split_radio = tkinter.Radiobutton(record_radio_frame, text="Нарезка видео", variable=self.record_change_val,
                                           value=3, font=self.heading_font, bg=self.leftBG)
        video_split_radio.pack(pady=[0, 25], side="top")

        check_frame = tkinter.Frame(self.left_frame, bg=self.leftBG)
        check_frame.place(y=160, relwidth=0.9, relx=0.05, height=450)
        self.isSaveFrames = tkinter.IntVar()
        check_save= tkinter.Checkbutton(check_frame, text='Сохранить изображения',variable=self.isSaveFrames,
                                    onvalue=True,offvalue=False, bg=self.leftBG)
        check_save.pack(pady=[0, 25], side="top")

        label6 = tkinter.Label(self.right_frame, text="Название таблицы", font=self.heading_font)
        label6.pack(pady=5, fill="x")
        self.combobox = tkinter.ttk.Combobox(self.right_frame, values=self.mediaProcessCtrl.set_tables_combobox(),
                                              postcommand=lambda: self.combobox.configure(values=self.mediaProcessCtrl.set_tables_combobox()))
        self.combobox.pack(pady=5, fill="x", padx=5)
        action_table_btn = tkinter.Button(self.right_frame, text="Выполнить действие", command=self.__action_btn_clicked)
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
        self.__create_children_elements()