from ultralytics import YOLO
import cv2
import os

modelpath = 'runs/detect/train23/weights/best.pt'


# Загрузка предобученной модели YOLOv8
def annotaion(modelpath):
    model = YOLO(modelpath)

    # Загрузка видео
    video_path = 'short.mp4'
    cap = cv2.VideoCapture(video_path)

    # Директории для сохранения аннотированных кадров и меток
    output_dir = 'annotated_frames'
    labels_dir = 'labels'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Детекция игроков с помощью YOLOv8
        results = model(frame)

        # Фильтрация только нужных классов (например, класс 0 - человек)
        filtered_boxes = [box for box in results[0].boxes if int(box.cls[0]) == 0]

        # Отрисовка bounding boxes только для игроков
        for box in filtered_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Координаты боксов
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Рисуем прямоугольник
            cv2.putText(frame, 'Player', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Подпись

        # Сохранение аннотированного кадра
        cv2.imwrite(f'{output_dir}/frame_{frame_count}.jpg', frame)

        # Экспорт аннотаций в формате YOLO
        with open(f'{labels_dir}/frame_{frame_count}.txt', 'w') as f:
            for box in filtered_boxes:
                cls = int(box.cls[0])
                x_center = box.xywh[0][0].item() / frame.shape[1]
                y_center = box.xywh[0][1].item() / frame.shape[0]
                width = box.xywh[0][2].item() / frame.shape[1]
                height = box.xywh[0][3].item() / frame.shape[0]
                label = f"{cls} {x_center} {y_center} {width} {height}\n"
                f.write(label)

        frame_count += 1

cap.release()
cv2.destroyAllWindows()

