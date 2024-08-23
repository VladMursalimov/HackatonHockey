import cv2

# Открываем видео файл
video = cv2.VideoCapture('short.mp4')

frames = []
success, frame = video.read()
while success:
    frames.append(frame)
    success, frame = video.read()

video.release()

from ultralytics import YOLO

# Загрузка предобученной модели YOLOv8
model = YOLO('yolov8n.pt')  # Замените на yolov8m.pt или другую, если нужно

results_list = []

# Выполнение детекции объектов на каждом кадре
for frame in frames:
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # Получаем результаты
    results_list.append(detections)

def convert_to_yolo_format(detections, frame_width, frame_height):
    yolo_formatted_detections = []
    for det in detections:
        x_min, y_min, x_max, y_max, confidence, class_id = det
        x_center = (x_min + x_max) / 2 / frame_width
        y_center = (y_min + y_max) / 2 / frame_height
        width = (x_max - x_min) / frame_width
        height = (y_max - y_min) / frame_height
        yolo_formatted_detections.append([class_id, x_center, y_center, width, height, confidence])
    return yolo_formatted_detections

yolo_results = {}
frame_height, frame_width = frames[0].shape[:2]

for frame_id, detections in enumerate(results_list):
    yolo_results[frame_id] = convert_to_yolo_format(detections, frame_width, frame_height)


from ultralytics import YOLO

# Загрузка предобученной модели YOLOv8
model = YOLO('yolov8n.pt')  # Замените на yolov8m.pt или другую, если нужно

results_list = []

# Выполнение детекции объектов на каждом кадре
for frame in frames:
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # Получаем результаты
    results_list.append(detections)