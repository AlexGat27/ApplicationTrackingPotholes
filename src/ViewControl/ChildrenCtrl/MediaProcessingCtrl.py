from src.ViewControl.BaseCtrl import *
import cv2
from ultralytics import YOLO
import random
import datetime
import numpy as np

#Класс-обработчик медиафайлов
class MediaProcessingCtrl(BaseCtrl):
    #Поддерживаемые разрешения
    __support_img_ext = ['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm', 'JPG'] 
    __support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']
    #Рандомные улицы
    __street = ['Ushakova', 'Kirovogradskaia', 'Naximova', 'Zakamskaia', 'Ribalko', 'Astraxanskaia']

    #Основной процесс обработки видео, записи стопкадров в папку Media/{nametable} и координат в таблицу
    def __videoProcessing(self, model, video_path, database, nametable, is_save_frame=True):
        if video_path.split('.')[-1] in self.__support_vid_ext:
            cap = cv2.VideoCapture(video_path)

            if is_save_frame:
                name_folder = os.path.join(os.path.abspath(os.getcwd()), "Media", nametable)
                if not(os.path.exists(name_folder)):
                    os.mkdir(name_folder)

            ids = []
            while cap.isOpened():
                _, frame = cap.read()
                if _:
                    results = model.track(frame, persist = True)[0]
                    if results.boxes.id is not None:
                        boxes_data = results.boxes.data.cpu().numpy()
                        boxes = np.asarray([box[:4] for box in boxes_data], dtype=int)
                        confidence = [conf[4] for conf in boxes_data]
                        for id in results.boxes.id.cpu().numpy().astype(int):
                            if id not in ids: 
                                ids.append(id)
                                time_add = datetime.now()
                                time_detect = datetime.today()
                                database.insert_to_table(nametable,time_detect, time_add, random.choice(self.__street),
                                                          random.uniform(-100, 100), random.uniform(-100, 100), random.randint(1, 4))
                                if is_save_frame:
                                    name_file = "Annotated_" + video_path.split('/')[-1].split('.')[0] + '_' + str(id) + '.jpg'
                                    tofile_path = os.path.join(name_folder, name_file)
                                    for box, conf in zip(boxes, confidence):
                                        frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                                        frame = cv2.putText(frame, f"Conf {conf:0.2f}", (box[0], box[1]),
                                                             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                                    cv2.imwrite(tofile_path, frame)
                    if cv2.waitKey(30) == ord('q'):
                        break
                else:
                    break
            cap.release()
            return len(ids)

    #Основной процесс обработки фото, записи фотографии в папку Media/{nametable} и координат в таблицу
    def __imageProcessing(self, model, image_path, database, nametable, is_save_frame=True):
        if image_path.split('.')[-1] in self.__support_img_ext:
            result = model(image_path)[0]

            for i in range(len(result.boxes)):
                database.insert_to_table(nametable, random.choice(self.__street), random.uniform(-100, 100), random.uniform(-100, 100), random.randint(1, 4))

            if is_save_frame:
                annotated_frame = result.plot()
                name_folder = os.path.join(os.path.abspath(os.getcwd()), "Media", nametable)
                name_file = "annotate_" + image_path.split('/')[-1].split('.')[0] + ".jpg"
                save_path = os.path.join(name_folder, name_file).replace(os.sep, '/')

                if not(os.path.exists(name_folder)):
                    os.makedirs(name_folder)
                cv2.imwrite(save_path, annotated_frame)
            return True
        else:
            return False
        
    #Установка модели
    def set_model(self, model_path):
        if model_path.split('.')[-1] == 'pt':
            self.model = YOLO(model_path)
            self.recordConsole("Модель YOLO успешно загружена\n\n")
            return True
        else:
            self.recordConsole("Ошибка, такой модели не существует\n\n")
            return False

    #Функция проверки подключения, модели, таблицы перед обработкой медиафайлов
    def mediaProcessing(self, name, index=1):
        if not(self.checkConnectionBD()):
            return None
        
        if self.model is None:
            self.recordConsole("Не выбрана модель\n\n")
            return None

        if self.database.isInDatabase(name):

            if index == 1:
                directory = tkinter.filedialog.askdirectory()
                media = os.listdir(directory)
                self.recordConsole("Идет процесс обработки папки с фото...\n")
                for med in media:
                    image_path = os.path.join(directory, med).replace(os.sep, '/')
                    succes = self.__imageProcessing(self.model, image_path, self.database, name)
                    if succes: self.recordConsole("Фото {} обработано успешно\n".format(med))
                    else: self.recordConsole("Ошибка обработки фото {}, такого разрешения не существует \n".format(med))
                self.recordConsole("Запись в таблицу {} совершена успешно\n\n".format(name))

            elif index == 2:
                video_path = tkinter.filedialog.askopenfilename()
                self.recordConsole("Идет процесс обработки видео...\n")
                succes = self.__videoProcessing(self.model, video_path, self.database, name)
                if succes: self.recordConsole("Запись видео {} в таблицу {} совершена успешно\n\n".format(video_path.split('/')[-1], name))
        else:
            self.recordConsole("Ошибка, таблицы {} не существует\n\n".format(name))

    def __init__(self, console):
        super().__init__(console)
        self.model = YOLO(os.path.join('Yolo_model', os.listdir('Yolo_model')[0]))