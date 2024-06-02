from PIL import Image, ImageFile
import os

# Устанавливаем порог для decompression
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None  # Убираем ограничение на макс размер

def resize_images_in_folder(source_folder, output_folder, new_size=(2000, 2000)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith('.tif') or file_name.lower().endswith('.tiff'):
            input_path = os.path.join(source_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            try:
                with Image.open(input_path) as img:
                    img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
                    img_resized.save(output_path)

                print(f"Изображение {file_name} было успешно изменено и сохранено.")
            except Exception as e:
                print(f"_____________________Ошибка при обработке изображения {file_name}: {e}")

src_folder = 'downloaded_files'
out_folder = 'resize_map'

resize_images_in_folder(src_folder, out_folder)
