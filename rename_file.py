import os
import re

# Путь к директории с файлами
dir_path = 'resize_map'

# Получение списка файлов
files = os.listdir(dir_path)
# Определение паттерна для извлечения координат
pattern = r"Hansen_GFC-2023-v1\.11_treecover2000_(\d+)([NS])_(\d+)([EW])\.tif"

# Функция для конвертации значений в индексы
def convert_coords(lat, lat_dir, lon, lon_dir):
    lat = int(lat) * (-1 if lat_dir == 'S' else 1)
    lon = int(lon) * (-1 if lon_dir == 'W' else 1)
    return (lat, lon)

# Создание списка кортежей (файл, широта, долгота)
coords = []
for file in files:
    match = re.match(pattern, file)
    if match:
        lat, lat_dir, lon, lon_dir = match.groups()
        coords.append((file, *convert_coords(lat, lat_dir, lon, lon_dir)))

# Сортировка списка по широте и долготе
coords.sort(key=lambda x: (-x[1], x[2]))

# Переименование файлов
for index, (file, _, _) in enumerate(coords, start=1):
    new_name = f"{index}.tif"
    os.rename(os.path.join(dir_path, file), os.path.join(dir_path, new_name))

print("Файлы успешно переименованы.")