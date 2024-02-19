import aiohttp
import asyncio
from PIL import Image
import random

class MediaRequestsCtrl:

    async def __send_data_to_server(url, data: dict, file_path=None):
        req = aiohttp.FormData()
        if file_path is not None:
            req.add_field('image', open(file_path, 'rb'))
        for key, value in data.items():
            req.add_field(key, value)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=req) as response:
                return await response.json()

    async def __processImages(url: str, queue: asyncio.Queue):
        while True:
            data, med, future = await queue.get()
            print(med)
            result = await MediaRequestsCtrl.__send_data_to_server(url, data, med)
            future.set_result(result)
            queue.task_done()

    async def __handle_images(dataList: list[dict], media_paths: list[str], queue: asyncio.Queue):
        futures = []
        for data, med in zip(dataList, media_paths):
            future = asyncio.Future()
            await queue.put((data, med, future))
            futures.append(future)
        results = await asyncio.gather(*futures)
        return results
    
    def __get_decimal_from_dms(dms):
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
        return degrees + minutes + seconds

    @staticmethod      
    async def ImagesProcessing(url, media_paths, nameTable) -> list[asyncio.Future]:
        dataList: list[dict] = []
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
                        dataList.append({
                            'nameTable': nameTable,
                            'fieldOfView': str(60),
                            'height': str(value[6]) if 6 in value.keys() else str(20),
                            'camX': str(longitude), 'camY': str(latitude),
                            'angleZ': str(0)
                        })
                        mediaList.append(med)
                        break
        if len(mediaList) > 0:
            queue = asyncio.Queue()
            handle_images_task = asyncio.create_task(MediaRequestsCtrl.__handle_images(dataList, mediaList, queue))
            processing_task = asyncio.create_task(MediaRequestsCtrl.__processImages(url, queue))
            response = await handle_images_task
            await queue.join()
            processing_task.cancel()
            return response
        else: return None

    @staticmethod  
    async def VideoProcessing(url, video_path, nameTable, is_save_frame):
        data = {
            'is_save_frame': str(bool(is_save_frame)),
            'nameTable': nameTable,
            'video_path': video_path,
        }
        task = asyncio.create_task(MediaRequestsCtrl.__send_data_to_server(url, data))
        return await asyncio.gather(task)
    
    @staticmethod
    async def VideoSplit(url, video_path):
        data = {
            'video_path': video_path,
            'frameLimit': 50
        }
        task = asyncio.create_task(MediaRequestsCtrl.__send_data_to_server(url, data))
        return await asyncio.gather(task)