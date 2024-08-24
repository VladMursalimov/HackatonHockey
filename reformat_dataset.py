import os
import pandas as pd

# Путь к папке с файлами
input_folder = 'datasets/data/val/labels'
output_folder = 'processed_labels_val'

# Создаем выходную папку, если она не существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Проходим по каждому файлу в папке
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):  # Обрабатываем только текстовые файлы
        file_path = os.path.join(input_folder, filename)

        # Загрузка данных из файла
        with open(file_path, 'r') as file:
            lines = [line.split() for line in file]

        df = pd.DataFrame(lines)

        # Удаляем строки, где первый элемент равен '1'
        df = df[df[0] != '1']

        # Заменяем строки, где первый элемент равен '2', на тип '1'
        df.loc[df[0] == '2', 0] = '1'

        # Сохраняем обработанные данные в новый файл
        output_file_path = os.path.join(output_folder, filename)
        df.to_csv(output_file_path, index=False, header=False, sep=' ')

        print(f'Processed {filename}')

print('Processing complete.')
