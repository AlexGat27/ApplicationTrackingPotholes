import aiohttp
import asyncio
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

    async def __processImages(url: str, data: dict, queue: asyncio.Queue):
        while True:
            med, future = await queue.get()
            print(med)
            result = await MediaRequestsCtrl.__send_data_to_server(url, data, med)
            future.set_result(result)
            queue.task_done()

    async def __handle_images(media_paths: list[str], queue: asyncio.Queue):
        futures = []
        for med in media_paths:
            future = asyncio.Future()
            await queue.put((med, future))
            futures.append(future)
        results = await asyncio.gather(*futures)
        return results

    @staticmethod      
    async def ImagesProcessing(url, media_paths, nameTable, is_save_frame) -> list[asyncio.Future]:
        data = {
            'is_save_frame': str(is_save_frame),
            'nameTable': nameTable,
            'fieldOfView': str(60),
            'height': str(30),
            'camX': str(random.uniform(3360000, 3400000)), 'camY': str(random.uniform(8370000, 8400000)),
            'angleZ': str(0)
        }
        queue = asyncio.Queue()
        handle_images_task = asyncio.create_task(MediaRequestsCtrl.__handle_images(media_paths, queue))
        processing_task = asyncio.create_task(MediaRequestsCtrl.__processImages(url, data, queue))
        response = await handle_images_task
        await queue.join()
        processing_task.cancel()
        return response

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