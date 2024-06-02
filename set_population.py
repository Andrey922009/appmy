import pandas as pd
import geopandas as gpd
from shapely.geometry import box

# Чтение данных о тайлах
tiles_data = pd.read_csv('coordinat_tiles.csv', sep='\t', engine='python')
# Создаем GeoDataFrame для тайлов
geometry_tiles = [box(left, bottom, right, top) for left, bottom, right, top in zip(
    tiles_data['Долгота верхнего левого угла'],
    tiles_data['Широта нижнего правого угла'],
    tiles_data['Долгота нижнего правого угла'],
    tiles_data['Широта верхнего левого угла']
)]
tiles_gdf = gpd.GeoDataFrame(tiles_data, geometry=geometry_tiles)

# Чтение данных о населенных пунктах
towns_data = pd.read_csv('towns.csv', sep='\t', engine='python')
# Создаем GeoDataFrame для населенных пунктов
geometry_towns = gpd.points_from_xy(towns_data['Долгота'], towns_data['Широта'])
towns_gdf = gpd.GeoDataFrame(towns_data, geometry=geometry_towns)

# Сопоставление тайлов и населенных пунктов
joined = gpd.sjoin(towns_gdf, tiles_gdf, how="left", predicate='within')

# Вычисление суммы населения для каждого тайла
population_sums = joined.groupby('index_right')['Население'].sum(min_count=1).reset_index()

# Обеспечиваем, что все тайлы представлены в итоговом файле
result = tiles_gdf.merge(population_sums, how='left', left_index=True, right_on='index_right')
result['Население'] = result['Население'].fillna(0)  # Замена NaN на 0

# Удаляем временные или ненужные столбцы
result.drop(columns=['index_right', 'geometry'], inplace=True)

# Визуальная проверка результатов перед сохранением
print(result)

# Сохраняем результаты в CSV-файл
result.to_csv('output_population_sums.csv', index=False)

print("Результаты сохранены в файл 'output_population_sums.csv'")
