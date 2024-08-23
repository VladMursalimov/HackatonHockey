from ultralytics import YOLO
import cv2

# Загрузка предобученной модели YOLOv8 (например, v8n - "nano" версия)
model = YOLO('yolov8n.pt')  # Замените на более тяжелую модель ('yolov8s.pt', 'yolov8m.pt' и т.д.) при необходимости


cap = cv2.VideoCapture('hockey_match.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame)  # Предсказание детекции
    annotated_frame = results.render()  # Отрисовка результатов

    cv2.imshow('Hockey Detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
