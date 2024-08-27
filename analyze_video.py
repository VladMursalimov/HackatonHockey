import os
import numpy as np


def is_goal(boxes, player_class):
    # Определяем, что событие - это гол, если несколько игроков находятся близко друг к другу

    # Получаем координаты центров всех игроков
    player_boxes = [box for box in boxes if box[0] == player_class]
    if len(player_boxes) < 3:
        return False  # Слишком мало игроков, чтобы считать это голом

    # Вычисляем дистанции между всеми игроками
    centers = [(box[1], box[2]) for box in player_boxes]
    distances = []
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            dist = np.sqrt((centers[i][0] - centers[j][0]) ** 2 + (centers[i][1] - centers[j][1]) ** 2)
            distances.append(dist)

    # Если большинство игроков находятся близко друг к другу (например, меньше 0.1 от размера кадра), это гол
    if np.mean(distances) < 0.05:
        return True
    return False


def is_fight(boxes, referee_class=2, team_a_class=1, team_b_class=2):
    # Подсчёт количества игроков каждой команды
    num_team_a = sum(1 for box in boxes if box[0] == team_a_class)
    num_team_b = sum(1 for box in boxes if box[0] == team_b_class)

    # Подсчёт судей
    num_referees = sum(1 for box in boxes if box[0] == referee_class)

    # Драка возможна, если на кадре есть хотя бы 2 игрока из каждой команды и минимум 2 судьи
    if num_team_a >= 2 and num_team_b >= 2 and num_referees >= 2:
        return True
    return False


def analyze_frame(boxes):
    if is_goal(boxes, 1):
        return "Goal detected in team 1"
    elif is_goal(boxes, 0):
        return "Goal detected in team 2"
    elif is_fight(boxes):
        return "Fight detected"


def parse_annotation_file(filepath):
    boxes = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            cls = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            boxes.append((cls, x_center, y_center, width, height))
    return boxes


def process_dataset(dataset_dir):
    for annotation_file in os.listdir(dataset_dir):
        filepath = os.path.join(dataset_dir, annotation_file)
        boxes = parse_annotation_file(filepath)
        event = analyze_frame(boxes)
        if event is not None:
            print(f"File: {annotation_file} - {event}")


# Пример использования
dataset_dir = 'HackatonHockey-main/labels'
process_dataset(dataset_dir)
