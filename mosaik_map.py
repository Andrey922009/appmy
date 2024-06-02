from PIL import Image
import os

# Путь к директории с изображениями
directory = 'resize_map'

# Количество изображений в ряду и столбце
num_columns = 36
num_rows = 14

# Считываем список изображений, сортируем его по названиям
file_list = sorted(os.listdir(directory), key=lambda x: int(''.join(filter(str.isdigit, x))))
images = [Image.open(os.path.join(directory, filename)) for filename in file_list if filename.endswith('.tif')]

if len(images) != num_columns * num_rows:
    raise ValueError("Количество изображений не соответствует ожидаемому (504)")

# Предполагается, что все изображения имеют одинаковый размер
width, height = images[0].size

total_width = width * num_columns
total_height = height * num_rows
collage = Image.new('L', (total_width, total_height))  # 'L' означает 8-битные оттенки серого

# Копирование изображений в коллаж
for index, image in enumerate(images):
    if image.mode != 'L':
        image = image.convert('L')
    x = index % num_columns * width  # Координата X для текущего изображения
    y = index // num_columns * height  # Координата Y для текущего изображения
    collage.paste(image, (x, y))

# Сохранение итогового изображения
output_path = os.path.join(directory, 'collage.png')
collage.save(output_path, format='PNG')
print(f"Коллаж сохранен как {output_path}")