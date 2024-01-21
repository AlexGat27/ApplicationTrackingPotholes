from src.Controllers.PageControllers.BaseCtrl import *
from src.Controllers.MediaRequestsCtrl import MediaRequestsCtrl as MedReqCtrl
import asyncio

#Класс-обработчик медиафайлов
class MediaProcessingCtrl(BaseCtrl):
    #Поддерживаемые разрешения
    __support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']

    #Нарезка видео
    def SplitVideo(self):
        video_path = tkinter.filedialog.askopenfilename()
        if video_path.split('.')[-1] in self.__support_vid_ext:
            asyncio.run(MedReqCtrl.VideoSplit(self.__scplitURL, video_path))
            self.recordConsole("Видео обработано успешно")
        else: self.recordConsole("Такого расширения видео не существует")
    
    #Функция проверки подключения, модели, таблицы перед обработкой медиафайлов
    def MediaProcessing(self, nameTable, index=1, isSaveFrame=False):
        if not(self.checkConnectionBD()):
            return None
        if self.database.isInDatabase(nameTable):
            if index == 1:
                directory = tkinter.filedialog.askdirectory()
                media_paths = [os.path.join(directory, med).replace(os.sep, '/') for med in os.listdir(directory)]
                self.recordConsole("Идет процесс обработки папки с фото...\n")
                response = asyncio.run(MedReqCtrl.ImagesProcessing(self.__imageServiceURL, media_paths, nameTable, isSaveFrame))
            elif index == 2:
                video_path = tkinter.filedialog.askopenfilename()
                if video_path.split('.')[-1] in self.__support_vid_ext:
                    self.recordConsole("Идет процесс обработки видео...\n")
                    response = asyncio.run(MedReqCtrl.VideoProcessing(self.__videoServiceURL, video_path, nameTable, isSaveFrame))
                else: self.recordConsole("Такого расширения видео не существует")
            self.__save_to_db(nameTable, response)
            self.recordConsole("Запись в таблицу {} совершена успешно\n\n".format(nameTable))
        else:
            self.recordConsole("Ошибка, таблицы {} не существует\n\n".format(nameTable))

    def __save_to_db(self, nameTable, data):
        for d in data:
            for coords in d:
                self.database.insert_to_table(nameTable, coords['crs3857'], coords['crs4326'])

    def __init__(self, console):
        super().__init__(console)
        self.__imageServiceURL = 'http://localhost:6000/imageProcessing?platform=Application'
        self.__videoServiceURL = 'http://localhost:6000/videoProcessing?platform=Application'
        self.__scplitURL = 'http://localhost:6000/videoSplit?platform=Application'