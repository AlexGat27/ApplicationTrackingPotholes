import base64
import aiohttp
import asyncio
from PIL import Image
from src.Models.Camera import CameraSplitRequest, CameraImageProcessing

class MediaRequestsCtrl:

    def __init__(self) -> None:
        self.timeout = 20

    async def __send_data_to_server(self, url, data: dict, file_path=None):
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            for key, value in data.items():
                form.add_field(key, value)
            if file_path:
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                    file_base64 = base64.b64encode(file_content).decode('utf-8')
                    form.add_field('image', file_base64)
            try:
                async with session.post(url, data=form) as response:
                    response.raise_for_status()  # Проверка ошибок в ответе
                    return await response.json()
            except aiohttp.ClientError as e:
                print("Aiohttp client error:", e)
            except aiohttp.ClientResponseError as e:
                print("Aiohttp client response error:", e)
            except aiohttp.ClientTimeout as e:
                print("Aiohttp client timeout:", e)
            except Exception as e:
                print("Unexpected error:", e)

    async def __processImages(self, url: str, queue: asyncio.Queue):
        while True:
            data, med, future = await queue.get()
            result = await self.__send_data_to_server(url, data, med)
            future.set_result(result)
            queue.task_done()

    async def __handle_images(self, cameras: list[CameraImageProcessing], media_paths: list[str], queue: asyncio.Queue):
        futures = []
        for camera, med in zip(cameras, media_paths):
            future = asyncio.Future()
            await queue.put((camera.model_dump(), med, future))
            futures.append(future)
        results = await asyncio.gather(*futures)
        return results
    
    def __get_decimal_from_dms(dms):
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
        return degrees + minutes + seconds

    async def ImagesProcessing(self, url, media_paths, nameTable) -> list[asyncio.Future]:
        cameras: list[CameraImageProcessing] = []
        mediaList: list[str] = []
        for med in media_paths:
            img = Image.open(med)
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    if tag == 34853:
                        latitude = MediaRequestsCtrl.__get_decimal_from_dms(value[2])
                        longitude = MediaRequestsCtrl.__get_decimal_from_dms(value[4])
                        if value[1] == "S":
                            latitude *= -1
                        if value[3] == "W":
                            longitude *= -1
                        cameras.append(CameraImageProcessing(
                            nameTable = nameTable,
                            fieldOfView = str(60),
                            height = str(value[6]) if 6 in value.keys() else str(20),
                            camX = str(longitude), camY = str(latitude),
                            angleZ = str(0)
                        ))
                        mediaList.append(med)
                        break
        if len(mediaList) > 0:
            queue = asyncio.Queue()
            handle_images_task = asyncio.create_task(self.__handle_images(cameras, mediaList, queue))
            processing_task = asyncio.create_task(self.__processImages(url, queue))
            response = await handle_images_task
            await queue.join()
            processing_task.cancel()
            return response
        else: return None
    
    async def VideoSplit(self, url, cam: CameraSplitRequest):
        task = asyncio.create_task(self.__send_data_to_server(url, cam.model_dump()))
        return await asyncio.gather(task)