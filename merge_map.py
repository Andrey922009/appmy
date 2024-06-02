import rasterio
import numpy as np
import os
from rasterio.merge import merge
from rasterio.plot import show

# файлы тайлов
directory = "downloaded_files"

# Список всех TIFF
all_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]

# Чтение и добавление в список
src_files_to_mosaic = []
for fp in all_files:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

# Объединение файлов
mosaic, out_trans = merge(src_files_to_mosaic)

# Сохранение
out_meta = src.meta.copy()

# Обновление метаданных
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans,
                 "compress": "lzw"})

# Запись результата в новый файл
with rasterio.open('output.tif', 'w', **out_meta) as dest:
    dest.write(mosaic)

# Проверка результата
if True:  # True, визуализировать результат
    show(mosaic, cmap='terrain')