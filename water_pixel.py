import os
from PIL import Image

def count_colored_pixels(folder_path, output_file='waterPXL.txt', target_color='#9ebcd8'):
    # Конвертация цвета из Hex в RGB
    target_color_rgb = tuple(int(target_color.strip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    files_counter = 0  # Счетчик обработанных файлов

    # Открытие файла для записи результатов
    with open(output_file, 'w', encoding='utf-8') as file:
        # Проход по файлам в указанной папке
        for filename in sorted(os.listdir(folder_path)):
            # Только .png файлы
            if filename.endswith('.png'):
                file_path = os.path.join(folder_path, filename)
                color_count = 0
                # Открываем изображение
                with Image.open(file_path) as img:
                    for pixel in img.getdata():
                        if pixel[:3] == target_color_rgb:  # Игнорируем прозрачность если есть
                            color_count += 1

                # Запись результатов в файл
                file.write(f"{files_counter}\t{filename}\t{color_count}\n")  # Добавляем индекс файла
                files_counter += 1  # Увеличиваем счетчик обработанных файлов

                if files_counter % 10 == 0: 
                    print(f"Обработано файлов: {files_counter}")
                    
    print(f"Всего обработано файлов: {files_counter}")

count_colored_pixels('tiles_sha_256')