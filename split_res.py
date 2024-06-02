import pandas as pd

# Загрузка данных из CSV файла
input_file = 'mineral.csv'
output_file = 'mineral_output.csv'

data = pd.read_csv(input_file, sep='\t') 

# Расширение DataFrame для каждого элемента в списке ископаемых
# Создаем новый DataFrame для хранения результатов
expanded_data = pd.DataFrame(columns=['Latitude', 'Longitude', 'commodity'])

for index, row in data.iterrows():
    minerals = row['commodity'].split(',') 
    for mineral in minerals:
        # Создаем новую строку с теми же координатами, но с одним ископаемым
        new_row = pd.DataFrame([{'Latitude': row['Latitude'], 'Longitude': row['Longitude'], 'commodity': mineral.strip()}])
        expanded_data = pd.concat([expanded_data, new_row], ignore_index=True)

# Сохранение измененных данных в новый CSV файл
expanded_data.to_csv(output_file, index=False, sep='\t')

print('Данные обработаны и сохранены в', output_file)
