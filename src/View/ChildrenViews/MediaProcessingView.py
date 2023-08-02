from src.View.BaseView import *
from src.ViewControl.ChildrenCtrl.MediaProcessingCtrl import *

class MediaProcessingView(BaseView):

    def __action_btn_clicked(self):
        pass
    
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

        label6 = tkinter.Label(self.right_frame, text="Название таблицы", font=("Bold", 13))
        label6.pack(pady=5, fill="x")
        self.combobox = tkinter.ttk.Combobox(self.right_frame)
        self.combobox.pack(pady=5, fill="x", padx=5)
        self.action_table_btn = tkinter.Button(self.right_frame, text="Запиcать в таблицу", command=self.__action_btn_clicked)
        self.action_table_btn.pack(fill='x', pady=5, padx=5)

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