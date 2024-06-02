import os
from PIL import Image

def combine_tiles(input_folder='tiles_photo_512', output_folder='tiles_photo_256', tile_size=(256, 256)):
    """
    Комбинирует тайлы 2x2 в одно изображение, уменьшая размер сетки в два раза, с оптимизацией использования памяти.
    """
   # Создание директории ввода, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    combined_image_size = (tile_size[0] * 2, tile_size[1] * 2)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            parts = filename.split('-')
            x, y = int(parts[0]), int(parts[1].split('.')[0])

            parent_x = x // 2
            parent_y = y // 2

            # Определяем позицию внутри нового изображения, исправляем перепутанные тайлы
            position_x = x % 2
            position_y = y % 2
            
            # Переключаем местами перепутанные тайлы: верхний правый и нижний левый
            if position_x == 1 and position_y == 0:
                position_x, position_y = 0, 1
            elif position_x == 0 and position_y == 1:
                position_x, position_y = 1, 0

            key = (parent_x, parent_y)

            with Image.open(os.path.join(input_folder, filename)) as tile:
                if key not in globals():
                    globals()[key] = Image.new('RGB', combined_image_size)
        
                pos_x = position_x * tile_size[0]
                pos_y = position_y * tile_size[1]
                globals()[key].paste(tile, (pos_x, pos_y))

                # Считаем количество тайлов в изображении
                if 'count_' + str(key) not in globals():
                    globals()['count_' + str(key)] = 1
                else:
                    globals()['count_' + str(key)] += 1

                # Если добавлены все тайлы, сохраняем изображение и освобождаем память
                if globals()['count_' + str(key)] == 4:
                    output_file = os.path.join(output_folder, f'{parent_x}-{parent_y}.png')
                    globals()[key].save(output_file)
                    print(f'Saved {output_file}')
                    globals()[key].close()
                    del globals()[key]
                    del globals()['count_' + str(key)]

# Вызов функции
combine_tiles()