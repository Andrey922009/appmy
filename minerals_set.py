import pandas as pd
import math

def latlon_to_tile_number(lat, lon, zoom=8):
    if abs(lat) > 89.999:
        lat = math.copysign(89.999, lat)

    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    try:
        xtile = int((lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    except ValueError:
        xtile, ytile = 0, 0
    return xtile, ytile

def tile_number_to_seq(xtile, ytile, tile_size=256):
    return ytile * tile_size + xtile + 1

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def process_resources(file_path, desired_resources, zoom_level=8, tile_size=256):
    dataframe = pd.read_csv(file_path, sep='\t', names=['latitude', 'longitude', 'resource'])

    tile_resources = {}

    for index, row in dataframe.iterrows():
        if not (is_float(row['latitude']) and is_float(row['longitude'])):
            print(f"Ошибка обработки строки {index}: Некорректные координаты.")
            continue

        if row['resource'].strip().lower() not in desired_resources:
            continue  # Пропускаем ресурсы, не входящие в список желаемых

        try:
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            xtile, ytile = latlon_to_tile_number(lat, lon, zoom=zoom_level)
            tile_seq = tile_number_to_seq(xtile, ytile, tile_size=tile_size)
            resource_info = row['resource'].strip()
            coords = f"({lat}, {lon})"  # Формирование строки с координатами
            if tile_seq not in tile_resources:
                tile_resources[tile_seq] = {'resources': [], 'coordinates': []}
            tile_resources[tile_seq]['resources'].append(resource_info)
            tile_resources[tile_seq]['coordinates'].append(coords)
        except Exception as e:
            print(f"Ошибка обработки строки {index}: {e}")
            continue

    total_tiles = tile_size ** 2
    result_data = []
    for tile_number in range(1, total_tiles + 1):
        if tile_number in tile_resources:
            resources_str = '; '.join(tile_resources[tile_number]['resources'])
            coordinates_str = '; '.join(set(tile_resources[tile_number]['coordinates']))  # Использование set для удаления дубликатов
            resources_count = len(tile_resources[tile_number]['resources'])
            result_data.append([tile_number, resources_str, resources_count, coordinates_str])
        else:
            result_data.append([tile_number, "", 0, ""])

    result_df = pd.DataFrame(result_data, columns=['Tile Number', 'Resources', 'Total Resources', 'Coordinates'])
    result_df.to_csv('output_tile_resources.csv', index=False, encoding='utf-8')
    return result_df

desired_resources = ['iron', 'limestone', 'copper', 'platinum', 'silver', 'tungsten', 'aluminum', 'gold', 'titanium', 'rare earth elements', 'uranium']

file_path = 'your_file_path_here.csv'
resulting_data = process_resources(file_path, desired_resources)
if resulting_data is not None:
    print(resulting_data.head())