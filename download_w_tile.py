import requests
import os
from concurrent.futures import ThreadPoolExecutor

def download_tile(zoom, x, y, folder='tiles_sha'):
    """
    Скачивает один тайл по заданным координатам и сохраняет его с именем в формате y-x.png.
    """
    url = f"https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{zoom}/{x}/{y}"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f'{x}-{y}.png'
        with open(os.path.join(folder, filename), 'wb') as file:
            file.write(response.content)
        return True
    else:
        print(f"Ошибка загрузки тайла x={x}, y={y}")
        return False

def download_tiles(zoom, x_range, y_range, folder='tiles_photo_512'):
    """
    Скачивает тайлы в заданном диапазоне. Имена файлов соответствуют координатам тайлов.
    Использует многопоточность для ускорения загрузки.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Создаем список всех задач для загрузки
    tasks = [(zoom, x, y, folder) for x in range(*x_range) for y in range(*y_range)]
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda p: download_tile(*p), tasks)

# Конфигурация
zoom_level = 8  # Уровень масштабирования
x_range = (0, 512)  # Примерный диапазон для x на уровне 8
y_range = (0, 512)  # Примерный диапазон для y на уровне 8

# Запуск загрузки
download_tiles(zoom_level, x_range, y_range)