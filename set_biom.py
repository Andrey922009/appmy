import os
import cv2
import pandas as pd

def get_histogram(image_path):
    image = cv2.imread(image_path)
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    hist = cv2.calcHist([lab_image], [0, 1, 2], None, [65, 65, 65], [0, 256, 0, 256, 0, 256])
    return cv2.normalize(hist, hist).flatten()

def load_biome_samples(biomes, samples_folder='samples_test'):
    samples = {}
    for biome in biomes:
        image_path = os.path.join(samples_folder, f'{biome}.png')
        samples[biome] = get_histogram(image_path)
    return samples

def classify_tiles(tile_folder, biome_histograms):
    results = []
    tiles_files = [f for f in os.listdir(tile_folder) if f.endswith('.png')]
    for tile_file in tiles_files:
        tile_path = os.path.join(tile_folder, tile_file)
        tile_hist = get_histogram(tile_path)
        distances = {biome: cv2.compareHist(tile_hist, hist, cv2.HISTCMP_CORREL) for biome, hist in biome_histograms.items()}
        closest_biome = max(distances, key=distances.get)  # Используем max для корреляции
        results.append((tile_file, closest_biome))
    return results

def create_html(df, output_path, image_folder):
    # Функция для представления пути к изображению в HTML формате.
    def path_to_image_html(path):
        return f'<img src="{path}" width="128" >'

    # Копирование DataFrame для превращения пути файла в HTML-тэг img.
    df_html = df.copy()
    df_html['Filename'] = df_html['Filename'].apply(lambda x: os.path.join(image_folder, x))
    df_html['Filename'] = df_html['Filename'].apply(path_to_image_html)

    # Сохранение DataFrame в HTML
    html = df_html.to_html(escape=False)  # `escape=False` чтобы интерпретировать HTML тэги
    with open(output_path, 'w') as f:
        f.write(html)

def main():
    biomes = ['voda', 'sneg', 'sneg1', 'sneg2', 'sneg3', 'sneg4', 'kust', 'kust1', 'kust2', 'kust3', 'kust4', 'kust5', 'kust6', 'kust7', 'kust8', 'kust9', 'kust10', 'kust11', 'kust12', 'kust13', 'kust14', 'kust15', 'kust16', 'kust17', 'kust18', 'les', 'les1', 'les2', 'les3', 'les4', 'les5', 'les6', 'les7', 'les8', 'les9', 'les10', 'les11', 'les12', 'les13', 'les14', 'pust', 'pust1', 'pust2', 'pust3', 'pust4', 'pust5', 'pust6', 'pust7', 'pust8', 'pust9', 'pust10', 'pust11', 'pust12', 'bereg', 'bereg1', 'bereg2', 'bereg3', 'bereg4', 'bereg5', 'bereg6', 'bereg7', 'bereg8', 'bereg9', 'bereg10', 'bereg11', 'bereg12', 'bereg13']
    biome_histograms = load_biome_samples(biomes)
    result = classify_tiles('tiles_phy_128', biome_histograms)
    # Сохранение результатов в CSV
    df = pd.DataFrame(result, columns=['Filename', 'Predicted Biome'])
    df.to_csv('tile_biomes.csv', index=False)
    print("Классификация завершена, результаты сохранены в 'tile_biomes.csv'.")
    # Создание HTML файла
    create_html(df, 'tile_biomes.html', 'tiles_phy_128')

if __name__ == "__main__":
    main()