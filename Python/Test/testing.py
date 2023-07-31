from Python.Database import *
from Python.potholeDetectionProcess import *
from ultralytics import YOLO
import psycopg2
from datetime import datetime, timezone
import random

# host='127.0.0.1'
# user='postgres'
# password='Shurikgat2704'
# database='postgres'
# port='5432'
# columns = '(time_detect, time_add, adress, latitude, longitude, pothole_class)'
# try:
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database,
#         port=port
#     )
#     connection.autocommit = True
#     cursor = connection.cursor()

#     for i in range(50):
#         today = datetime.now()
#         time_detect = datetime.today()
#         adress = random.choice(street)
#         latitude =  random.uniform(-100, 100)
#         longitude = random.uniform(-100, 100)
#         pothole_class = random.randint(1, 4)
#         cursor.execute(
#             f"INSERT INTO pothole {columns} VALUES (%s, %s, %s, %s, %s, %s)",
#             (time_detect, today, adress, latitude, longitude, pothole_class)
#         )
#     cursor.execute("SELECT * FROM pothole")
#     data = cursor.fetchall()
#     for d in data:
#         print(d)

# except (Exception, Error) as error:
#     print("[Info] Error while working with PostgreSQL: {}".format(error))
# finally:
#     cursor.close()
#     connection.close()

model = YOLO('C:/Users/sanya/Programs/Python/Graphic_App_for_detect/Yolo_model/HolesChecker.pt')
video_path = 'C:/Users/sanya/Programs/Python/Graphic_App_for_detect/Media/Video/pothole1.mp4'
cap = cv2.VideoCapture(video_path)
fps = 10
cap.set(cv2.CAP_PROP_FPS, fps)
while cap.isOpened():
    _, frame = cap.read()
    if _:
        results = model.track(source=frame, persist=True)
    
        for result in results:
            frame = result.plot()
            if result.boxes is None:
                continue   
            data = result.boxes.data
            boxes = result.boxes.xyxy
            ids = result.boxes.id
            print(ids)
            print(boxes)
            print(data)
            if boxes is None or ids is None:
                 continue
            boxes = boxes.cpu().numpy().astype(int)
            ids = ids.cpu().numpy().astype(int)
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
            # ids = result.boxes.id.cpu().numpy().astype(int)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
cap.release()
cv2.destroyAllWindows()