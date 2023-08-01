from ultralytics import YOLO
from src.View.Application import App

if __name__ == "__main__":
    model = YOLO('Yolo_model/HolesChecker.pt')
    app = App()
    app.mainloop()