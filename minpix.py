from PIL import Image
import os

def resize_images(directory):
    # Перебор всех файлов в директории
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            filepath = os.path.join(directory, filename)
            with Image.open(filepath) as img:
                # Проверяем, что размеры исходного изображения 512x512
                if img.size == (256, 256):
                    # Изменение размера изображения
                    img_resized = img.resize((128, 128), Image.Resampling.LANCZOS)
                    # Сохранение измененного изображения
                    img_resized.save(filepath)
                    print(f'Resized {filename}')
                else:
                    print(f'Skipped {filename} (not 512x512)')

# Указываем путь к директории с изображениями
directory_path = 'tiles_phy_128'
resize_images(directory_path)
