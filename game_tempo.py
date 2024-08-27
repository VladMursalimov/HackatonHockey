import os
import cv2
import numpy as np


def calculate_game_tempo(txt_folder, frame_rate):
    # Словарь для хранения предыдущих координат игроков
    previous_positions = {}
    # Словарь для хранения скорости игроков
    speeds = {}

    # Получаем список всех .txt файлов в указанной папке
    txt_files = sorted([f for f in os.listdir(txt_folder) if f.endswith('.txt')])

    for txt_file in txt_files:
        # Определяем путь к .txt файлу
        txt_file_path = os.path.join(txt_folder, txt_file)

        # Открываем файл .txt и читаем аннотации с использованием кодировки utf-8
        with open(txt_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Перебираем строки аннотаций
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # Пропускаем строки с недостаточным количеством данных

            cls = int(parts[0])  # Класс объекта
            x_center = float(parts[1])  # Центр X
            y_center = float(parts[2])  # Центр Y

            # Используем класс для создания уникального ключа для каждого игрока
            player_id = f"Player{cls}"

            # Если это первый кадр для игрока, инициализируем его позицию
            if player_id not in previous_positions:
                previous_positions[player_id] = (x_center, y_center)
                speeds[player_id] = 0.0  # Начальная скорость
                continue

            # Вычисляем расстояние перемещения
            prev_x, prev_y = previous_positions[player_id]
            distance = np.sqrt((x_center - prev_x) ** 2 + (y_center - prev_y) ** 2)

            # Вычисляем скорость (в пикселях в секунду)
            speed = distance * frame_rate  # Скорость = расстояние * частота кадров

            # Обновляем позиции и скорость
            previous_positions[player_id] = (x_center, y_center)
            speeds[player_id] = speed

    return speeds


# Пример использования функции
txt_folder_path = 'labelsAndImages/labelsMerged'  # Замените на путь к вашей папке с .txt файлами
frame_rate = 30  # Замените на частоту кадров вашего видео (например, 30 FPS)

speeds = calculate_game_tempo(txt_folder_path, frame_rate)

# Вывод скоростей игроков
for player, speed in speeds.items():
    print(f"{player}: Скорость = {speed:.2f} пикселей/сек")