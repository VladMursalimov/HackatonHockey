import cv2
import os

def video_to_frames(videopath):
    # Путь к видеофайлу
    video_path = 'hockey_match.mp4'

    # Создаем папку для сохранения кадров
    output_folder = 'frames'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Загружаем видео
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    save_every_n_frames = 10  # Сохраняем каждый 10-й кадр

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % save_every_n_frames == 0:
            frame_filename = os.path.join(output_folder, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()

cv2.destroyAllWindows()
