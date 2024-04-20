from src.Controllers.PageControllers.BaseCtrl import BaseCtrl
from src.Controllers.MediaRequestsCtrl import MediaRequestsCtrl
from threading import Thread
import tkinter
import asyncio
import os
from src.Models.Camera import CameraSplitRequest, CameraImageProcessing

#Класс-обработчик медиафайлов
class MediaProcessingCtrl(BaseCtrl):
    #Поддерживаемые разрешения
    __support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']

    def __init__(self, console):
        super().__init__(console)
        self.medReqCtrl = MediaRequestsCtrl()
        self.__imageServiceURL = 'http://localhost:6002/imageProcessing'
        self.__splitURL = 'http://localhost:6002/videoSplit'

    #Нарезка видео
    def SplitVideo(self, cam: CameraSplitRequest):
        Thread(target=self.__split_video_async, args=(cam,)).start()
    
    #Функция проверки подключения, модели, таблицы перед обработкой медиафайлов
    def MediaProcessing(self, nameTable):
        if not(self.checkConnectionBD()):
            return None
        if self.database.isInDatabase(nameTable):
            directory = tkinter.filedialog.askdirectory()
            media_paths = [os.path.join(directory, med).replace(os.sep, '/') for med in os.listdir(directory)]
            self.recordConsole("Идет процесс обработки папки с фото...\n")
            Thread(target=self.__image_processing_async, args=(media_paths, nameTable,)).start()
        else:
            self.recordConsole("Ошибка, таблицы {} не существует\n\n".format(nameTable))

    def __save_to_db(self, nameTable: str, response: list):
        print(response)
        count = 0
        for imageInfo in response:
            for pothole in imageInfo:
                self.database.insert_potholes(nameTable, pothole['crs3857'], pothole['crs4326'], pothole['image_path'])
                count += 1
        self.recordConsole("В таблицу {} добавлено {} дорожных дефектов\n\n".format(nameTable, count))


    def __split_video_async(self, cam: CameraSplitRequest):
        if cam.video_path.split('.')[-1] in self.__support_vid_ext:
            self.recordConsole("Идет обработка видео...\n")
            response = asyncio.run(self.medReqCtrl.VideoSplit(self.__splitURL, cam))
            if response:
                self.recordConsole("Видео обработано успешно\n\n")
            else:
                self.recordConsole("Ошибка отправки запроса на сервер\n")
        else: self.recordConsole("Такого расширения видео не существует\n")

    def __image_processing_async(self, media_paths, nameTable):
        response = asyncio.run(self.medReqCtrl.ImagesProcessing(self.__imageServiceURL, media_paths, nameTable))
        if response:
            self.__save_to_db(nameTable, response)
        else:
            self.recordConsole("Ошибка отправки запроса на сервер")