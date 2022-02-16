import cv2
from asyncio import get_event_loop

from plugins.bot import ServiceBot, Bot

bot = Bot(token="2079006861:AAHbMFZld6q-edr5zPdxGaXNqLxQdtykiKY")

duration_target = 3


async def pars_video(file_id: str):
    resp = await bot.servicing.get_file(file_id=file_id)

    # генерируем url c видео для загрузки
    video_url = bot.servicing.generate_file_url(resp.result.file_path)

    # загружаем видео
    video = cv2.VideoCapture(video_url)

    # определяем параметры видео
    fps = video.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # определяем коэф продолжительности видео
    coefficient = duration / duration_target
    # если коэф > 1 то режем видео иначе ничего не делаем
    if coefficient > 1:
        target_count_frames = frame_count / coefficient
    else:
        target_count_frames = frame_count

    print('кол-во кадров после обрезки: ' + str(target_count_frames))

    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration / 60)
    seconds = duration % 60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

    # TODO обрезаем видео до 10 секунд и убираем каждый второй кадр

    success, image = video.read()
    count = 0
    file_ids_arr = []
    while success:
        # пропускаем каждый второй кадры для оптимизации
        if count % 2 == 0:
            # convert to jpeg and save in variable
            image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
            # получаем видео от telegram
            resp = bot.messaging.send_photo(chat_id=81432612, image_bytes=image_bytes)
            # записываем в массив id файлов с самым большим разрешением
            # этот массив мы должны передать на обработку
            file_ids_arr.append(resp.result.get_file_id())

        # переходим к следующему кадру
        success, image = video.read()
        print('Read a new frame: ', success)
        count += 1

        if count >= target_count_frames:
            break

    return file_ids_arr
