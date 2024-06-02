import math

zoom_level = 8
num_tiles = 2 ** zoom_level

with open('tile_coordinates.txt', 'w', encoding='utf-8') as file:
    file.write("Номер тайла\tШирота верхнего левого угла\tДолгота верхнего левого угла\tШирота нижнего правого угла\tДолгота нижнего правого угла\n")
    for y in range(num_tiles):
        for x in range(num_tiles):
            # Расчет верхнего левого угла
            lon_left = x / num_tiles * 360.0 - 180.0
            lat_top = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / num_tiles))))
            # Расчет нижнего правого угла
            lon_right = (x + 1) / num_tiles * 360.0 - 180.0
            lat_bottom = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / num_tiles))))
            
            # Формирование номера тайла
            tile_number = y * num_tiles + x
            
            # Формирование строки с данными тайла
            file.write(f"{tile_number}\t{lat_top}\t{lon_left}\t{lat_bottom}\t{lon_right}\n")
