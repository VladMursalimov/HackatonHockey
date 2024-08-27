import os


def update_indices_in_txt_files(folder):
    # Получаем список всех .txt файлов в указанной папке
    txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]

    for filename in txt_files:
        file_path = os.path.join(folder, filename)

        # Открываем файл для чтения
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Обновляем индексы в каждой строке
        updated_lines = []
        for line in lines:
            parts = line.split()
            if parts:  # Проверяем, что строка не пустая
                # Извлекаем и обновляем первый элемент (индекс)
                index = int(parts[0]) + 6
                # Создаем новую строку с обновленным индексом
                updated_line = f"{index} " + " ".join(parts[1:]) + "\n"
                updated_lines.append(updated_line)

        # Записываем обновленные строки обратно в тот же файл
        with open(file_path, 'w') as f:
            f.writelines(updated_lines)

    print(f"Индексы успешно обновлены в папке: {folder}")


# Пример использования функции
folder_path = 'labels'  # Замените на путь к вашей папке с .txt файлами
update_indices_in_txt_files(folder_path)