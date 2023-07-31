import cv2
from ultralytics import YOLO
from datetime import datetime, timezone
import random
from Python.Database import *
import os
import numpy as np

class MediaProcessing:
    __support_img_ext = ['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm']
    __support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']
    __street = ['Ushakova', 'Kirovogradskaia', 'Naximova', 'Zakamskaia', 'Ribalko', 'Astraxanskaia']

    def videoProcessing(self, model, video_path, database, nametable, is_save_frame=True):
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
                            database.insert_to_table(nametable, random.choice(self.__street), random.uniform(-100, 100), random.uniform(-100, 100), random.randint(1, 4))
                            if is_save_frame:
                                name_file = "Annotated_" + video_path.split('/')[-1].split('.')[0] + '_' + str(id) + '.jpg'
                                tofile_path = os.path.join(name_folder, name_file)
                                for box, conf in zip(boxes, confidence):
                                    frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                                    frame = cv2.putText(frame, f"Conf {conf:0.2f}", (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                                cv2.imwrite(tofile_path, frame)
                if cv2.waitKey(30) == ord('q'):
                    break
            else:
                break
        cap.release()
        return len(ids)

    def imageProcessing(self, model, image_path, database, nametable, is_save_frame=True):
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
        
    def get_support_img_ext(self):
        return self.__support_img_ext
    def get_support_vid_ext(self):
        return self.__support_vid_ext
    












