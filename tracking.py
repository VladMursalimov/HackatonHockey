import cv2
from ultralytics import YOLO
from sort import Sort  # Импортируем сортировщик для трекинга
import numpy as np

# Загрузка модели YOLOv8
model = YOLO('best.pt')  # Замените на путь к вашей модели

# Открытие видеофайла
video_path = 'short.mp4'  # Замените на путь к вашему видео
cap = cv2.VideoCapture(video_path)

# Получение информации о видео
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Создание объекта для записи видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_tracking.mp4', fourcc, fps, (width, height))

# Инициализация трекера
tracker = Sort()

# Обработка каждого кадра видео
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Выполнение предсказания с использованием YOLOv8
    results = model(frame)
    detections = []

    # Извлечение боксов и уверенности для каждого объекта
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            detections.append([x1, y1, x2, y2, confidence])

    # Преобразование в numpy для передачи в трекер
    detections = np.array(detections)

    # Обновление трекера
    tracks = tracker.update(detections)

    # Отображение треков
    for track in tracks:
        x1, y1, x2, y2, track_id = track[:5].astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'ID: {int(track_id)}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Запись аннотированного кадра в видеофайл
    out.write(frame)

    # Если хотите отображать видео в реальном времени (можно отключить в среде Kaggle)
    # cv2.imshow('YOLOv8 Object Tracking', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Освобождение ресурсов
cap.release()
out.release()
cv2.destroyAllWindows()

# Готовый файл будет сохранен как 'output_tracking.mp4'