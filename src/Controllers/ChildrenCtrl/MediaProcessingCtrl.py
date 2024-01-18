from src.Controllers.BaseCtrl import *
from ultralytics import YOLO
import numpy as np
import requests
import asyncio


#Класс-обработчик медиафайлов
class MediaProcessingCtrl(BaseCtrl):
    #Поддерживаемые разрешения
    __support_img_ext = ['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm', 'JPG'] 
    __support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']

    #Основной процесс обработки видео, записи стопкадров в папку Media/{nametable} и координат в таблицу
    def __videoProcessing(self, video_path, database, nameTable, is_save_frame):
        if video_path.split('.')[-1] in self.__support_vid_ext:
            data = {
                'is_save_frame': bool(is_save_frame),
                'nameTable': nameTable,
                'video_path': video_path
            }
            response = requests.post(self.videoServiceURL, data=data)
            for coords in response.json():
                database.insert_to_table(nameTable, coords['crs3857'], coords['crs4326'])
            return True
        else:
            return False


    #Основной процесс обработки фото, записи фотографии в папку Media/{nametable} и координат в таблицу
    def __imageProcessing(self, image_path, database, nameTable, is_save_frame):
        if image_path.split('.')[-1] in self.__support_img_ext:
            data = {
                'is_save_frame': bool(is_save_frame),
                'nameTable': nameTable
            }
            imageFile = {'image': open(image_path, 'rb')}
            response = requests.post(self.imageServiceURL, data=data, files=imageFile)
            for coords in response.json():
                database.insert_to_table(nameTable, coords['crs3857'], coords['crs4326'])
            return True
        else:
            return False

    #Функция проверки подключения, модели, таблицы перед обработкой медиафайлов
    def mediaProcessing(self, nameTable, index=1, isSaveFrame=False):
        if not(self.checkConnectionBD()):
            return None

        if self.database.isInDatabase(nameTable):

            if index == 1:
                directory = tkinter.filedialog.askdirectory()
                media = os.listdir(directory)
                self.recordConsole("Идет процесс обработки папки с фото...\n")
                for med in media:
                    image_path = os.path.join(directory, med).replace(os.sep, '/')
                    succes = self.__imageProcessing(image_path, self.database, nameTable, isSaveFrame)
                    if succes: self.recordConsole("Фото {} обработано успешно\n".format(med))
                    else: self.recordConsole("Ошибка обработки фото {}, такого разрешения не существует \n".format(med))
                self.recordConsole("Запись в таблицу {} совершена успешно\n\n".format(nameTable))

            elif index == 2:
                video_path = tkinter.filedialog.askopenfilename()
                self.recordConsole("Идет процесс обработки видео...\n")
                succes = self.__videoProcessing(self.model, video_path, self.database, nameTable, isSaveFrame)
                if succes: self.recordConsole("Запись видео {} в таблицу {} совершена успешно\n\n".format(video_path.split('/')[-1], nameTable))
        else:
            self.recordConsole("Ошибка, таблицы {} не существует\n\n".format(nameTable))

            # for i in range(len(result.boxes)):
            # time_detect = datetime.today()
            # database.insert_to_table(nametable, time_detect, random.choice(self.__street),
            #                           random.uniform(3360000, 3400000), random.uniform(8370000, 8400000), random.randint(1,4))
        # else:
            # print('Error:', response.status_code)

    def __init__(self, console):
        super().__init__(console)
        self.imageServiceURL = 'http://localhost:6000/imageProcessing?platform=Application'
        self.videoServiceURL = 'http://localhost:6000/videoProcessing?platform=Application'