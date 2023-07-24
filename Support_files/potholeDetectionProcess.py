import cv2
from ultralytics import YOLO
from datetime import datetime, timezone
import random
from Support_files.Database import *
import os

support_img_ext = ['bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm']
support_vid_ext = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv', 'webm']
street = ['Ushakova', 'Kirovogradskaia', 'Naximova', 'Zakamskaia', 'Ribalko', 'Astraxanskaia']

def videoProcessing(model, video_path, database, nametable, tofile=None):
    cap = cv2.VideoCapture(video_path)
    fps = 10
    cv2.SetCaptureProperty(cap, cv2.CV_CAP_PROP_FPS, fps)

    if tofile:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        frame_size = (frame_width,frame_height)
        output = cv2.VideoWriter(tofile,
            cv2.VideoWriter_fourcc('M','J','P','G'), fps, frame_size)
        
    while cap.isOpened():
        _, frame = cap.read()
        if _:
            results = model.track(frame, persist = True)
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)

            for i in range(len(results.boxes.id)):
                database.insert_to_table(nametable, random.choice(street), random.uniform(-100, 100), random.uniform(-100, 100), random.randint(1, 4))

            if tofile:
                for box, id in zip(boxes, ids):
                    frame = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                    frame = cv2.putText(
                        frame,
                        f"Id {id}",
                        (box[0], box[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                output.write(frame)
        else:
            break
    cap.release()
    if tofile: output.release()
    cv2.destroyAllWindows()

def imageProcessing(model, image_path, database, nametable, is_save_frame=True):
    result = model(image_path)[0]
    annotated_frame = result.plot()

    for i in range(len(result.boxes)):
        database.insert_to_table(nametable, 'Kirovogradskaya 34', random.uniform(-100, 100), random.uniform(-100, 100), random.randint(1, 4))

    if is_save_frame:
        name_folder = os.path.join(os.path.abspath(os.getcwd()), "Media", nametable)
        name_file = "annotate_"+image_path.split('/')[-1]
        for i in support_img_ext:
            if i in name_file:
                name_file = name_file.replace(i, 'jpg')
                break
        save_path = os.path.join(name_folder, name_file).replace(os.sep, '/')
        print(save_path)

        if not(os.path.exists(name_folder)):
            os.makedirs(save_path)
        cv2.imwrite(save_path, annotated_frame)
    return True

def mediaProcessing(model, media_path, database, nametable, is_save_frame=True):
    ext = media_path.split('.')[-1]
    if ext in support_img_ext:
        return imageProcessing(model, media_path, database, nametable, is_save_frame=True)
    elif ext in support_vid_ext:
        return videoProcessing(model, media_path, database, nametable, is_save_frame=True)
    else:
        return False












