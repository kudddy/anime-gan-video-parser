from threading import Thread
from plugins.workers.crop_face_in_video.crop_face_send_id import start_listening_and_pars
from plugins.workers.crop_photo.crop_photo_worker import run_crop_worker
from plugins.workers.sendstat.generate_send import generate_send_stat


start_listening_and_pars_thread = Thread(target=start_listening_and_pars)
start_listening_and_pars_thread.start()

generate_send_stat_thread = Thread(target=generate_send_stat)
generate_send_stat_thread.start()

run_crop_worker_thread = Thread(target=run_crop_worker)
run_crop_worker_thread.start()










