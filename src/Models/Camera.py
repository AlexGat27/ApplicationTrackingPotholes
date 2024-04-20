from pydantic import BaseModel

class CameraImageProcessing(BaseModel):
    camX: float
    camY: float
    height: float
    nameTable: str
    fieldOfView: float
    angleZ: float

class CameraSplitRequest(BaseModel):
    video_path: str
    height: float
    fps: int
    fieldOfView: float
    speed: float
    defaultInterval: int