import aiohttp
import asyncio
import random

class MediaRequestsCtrl:

    @staticmethod
    async def __send_data_to_server(url, data: dict, file_path=None):
        req = aiohttp.FormData()
        if file_path is not None:
            print("абракадабра") 
            req.add_field('image', open(file_path, 'rb'))
        for key, value in data.items():
            req.add_field(key, value)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=req) as response:
                return await response.json()

    @staticmethod      
    async def ImagesProcessing(url, media_paths, nameTable, is_save_frame):
        tasks = []
        print(is_save_frame, bool(is_save_frame))
        data = {
            'is_save_frame': str(is_save_frame),
            'nameTable': nameTable,
            'fieldOfView': str(60),
            'height': str(30),
            'camX': str(random.uniform(3360000, 3400000)), 'camY': str(random.uniform(8370000, 8400000)),
            'angleZ': str(0)
        }
        for med in media_paths:
            tasks.append(asyncio.create_task(MediaRequestsCtrl.__send_data_to_server(url, data, med)))
        return await asyncio.gather(*tasks)

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
        print(data)
        task = asyncio.create_task(MediaRequestsCtrl.__send_data_to_server(url, data))
        return await asyncio.gather(task)