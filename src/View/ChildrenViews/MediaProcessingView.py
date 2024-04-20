from src.View.BaseView import BaseView
from src.Controllers.PageControllers.MediaProcessingCtrl import MediaProcessingCtrl
from src.Models.Camera import CameraSplitRequest
import tkinter as tk


class MediaProcessingView(BaseView):

    def __action_btn_clicked(self):
        nameTable = self.combobox.get()
        if self.record_change_val.get() == 1:
            self.mediaProcessCtrl.MediaProcessing(nameTable)
        elif self.record_change_val.get() == 2:
            camera = CameraSplitRequest(
                fieldOfView = tk.getdouble(self.cam_fieldOfView.get()),
                height = tk.getdouble(self.cam_height.get()),
                defaultInterval = tk.getint(self.cam_defaultInterval.get()),
                speed = tk.getdouble(self.cam_speed.get()),
                fps = tk.getint(self.cam_fps.get()),
                video_path = tk.filedialog.askopenfilename()
            )
            self.mediaProcessCtrl.SplitVideo(camera)
        else:
            self.mediaProcessCtrl.recordConsole("Не выбрано действие (обработать фото или видео)\n\n")

    def __switch_camera_options(self):
        if self.record_change_val.get() == 2:
            self.video_split_options.place(y=160, relwidth=0.9, relx=0.05, height=450)
            self.image_process_options.place_forget()
        elif self.record_change_val.get() == 1:
            self.image_process_options.place(y=160, relwidth=0.9, relx=0.05, height=450)
            self.video_split_options.place_forget()
    
    def __create_children_elements(self):
        record_radio_frame = tk.Frame(self.left_frame, bg=self.leftBG)
        record_radio_frame.place(y=10, relx=0.05, relwidth=0.9, height=150)
        self.record_change_val = tk.IntVar()
        image_radio = tk.Radiobutton(record_radio_frame, text="Обработка фото", variable=self.record_change_val,
                                           value=1, font=self.heading_font, bg=self.leftBG, command=self.__switch_camera_options)
        image_radio.pack(pady=[25, 0], side="top")

        video_split_radio = tk.Radiobutton(record_radio_frame, text="Нарезка видео", variable=self.record_change_val,
                                           value=2, font=self.heading_font, bg=self.leftBG, command=self.__switch_camera_options)
        video_split_radio.pack(pady=[0, 25], side="top")

        self.__create_videosplit_options()
        self.__create_imageprocess_options()

        label6 = tk.Label(self.right_frame, text="Название таблицы", font=self.heading_font)
        label6.pack(pady=5, fill="x")
        self.combobox = tk.ttk.Combobox(self.right_frame, values=self.mediaProcessCtrl.set_tables_combobox(),
                                              postcommand=lambda: self.combobox.configure(values=self.mediaProcessCtrl.set_tables_combobox()))
        self.combobox.pack(pady=5, fill="x", padx=5)
        
        self.__create_action_params()

    def __create_videosplit_options(self):
        self.video_split_options = tk.Frame(self.left_frame, bg=self.leftBG)
        # self.video_split_options.place(y=160, relwidth=0.9, relx=0.05, height=450)
        
        self.cam_height = tk.Entry(self.video_split_options)
        self.cam_height.pack(pady=[5, 0])
        self.cam_height.insert(0, "30")
        label1 = tk.Label(self.video_split_options, text="Высота камеры", bg=self.leftBG)
        label1.pack(pady=[0, 5])
        
        self.cam_fieldOfView = tk.Entry(self.video_split_options)
        self.cam_fieldOfView.pack(pady=[5, 0], fill='x', padx=5)
        self.cam_fieldOfView.insert(0, "60")
        label2 = tk.Label(self.video_split_options, text="Угол обзора", bg=self.leftBG)
        label2.pack(pady=[0, 5])
        
        self.cam_speed = tk.Entry(self.video_split_options)
        self.cam_speed.pack(pady=[5, 0], fill='x', padx=5)
        self.cam_speed.insert(0, "10")
        label3 = tk.Label(self.video_split_options, text="Скорость", bg=self.leftBG)
        label3.pack(pady=[0, 5])
        
        self.cam_fps = tk.Entry(self.video_split_options)
        self.cam_fps.pack(pady=[5, 0], fill='x', padx=5)
        self.cam_fps.insert(0, "30")
        label4 = tk.Label(self.video_split_options, text="Частота кадров", bg=self.leftBG)
        label4.pack(pady=[0, 5])

        self.cam_defaultInterval = tk.Entry(self.video_split_options)
        self.cam_defaultInterval.pack(pady=[5, 0], fill='x', padx=5)
        self.cam_defaultInterval.insert(0, "-1")
        label5 = tk.Label(self.video_split_options, text="Интервал по умолчанию", bg=self.leftBG)
        label5.pack(pady=[0, 5])

    def __create_imageprocess_options(self):
        self.image_process_options = tk.Frame(self.left_frame, bg=self.leftBG)
        # self.image_process_options.place(y=160, relwidth=0.9, relx=0.05, height=450)
        
        self.cam_fieldOfView = tk.Entry(self.image_process_options)
        self.cam_fieldOfView.pack(pady=[5, 0], fill='x', padx=5)
        self.cam_fieldOfView.insert(0, "60")
        label1 = tk.Label(self.image_process_options, text="Угол обзора", bg=self.leftBG)
        label1.pack(pady=[0, 5])

        self.cam_angleZ = tk.Entry(self.image_process_options)
        self.cam_angleZ.pack(pady=[5, 0], fill='x', padx=5)
        self.cam_angleZ.insert(0, "0")
        label2 = tk.Label(self.image_process_options, text="Угол поворота камеры Z", bg=self.leftBG)
        label2.pack(pady=[0, 5])

    def __create_action_params(self):
        action_table_btn = tk.Button(self.right_frame, text="Выполнить действие", command=self.__action_btn_clicked)
        action_table_btn.pack(fill='x', pady=5, padx=5)

        buttons_frame = tk.Frame(self.right_frame)
        buttons_frame.place(y=110, relx=0.01, relwidth=0.98, height=30)
        show_tables_btn = tk.Button(buttons_frame, text="Вывести все таблицы", command=self.mediaProcessCtrl.show_tables)
        show_tables_btn.place(relx=0, rely=0, relheight=1, relwidth=0.49)
        clear_console_btn = tk.Button(buttons_frame, text="Очистить консоль", command=self.mediaProcessCtrl.clear_console)
        clear_console_btn.place(relx=0.51, rely=0, relheight=1, relwidth=0.49)


    def __init__(self):
        super().__init__()
        self.mediaProcessCtrl = MediaProcessingCtrl(self.console)
        self.__create_children_elements()