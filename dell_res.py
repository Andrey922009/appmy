import pandas as pd

def filter_resources(input_file_path, output_file_path, desired_resources):
    df = pd.read_csv(input_file_path, sep='\t', header=None, names=['Tile', 'Resources', 'Count'])
    
    df['Resources'] = df['Resources'].fillna('')
    def filter_resources_row(resources):
        if resources == '':
            return '', 0
        
        resources_list = resources.split(';')
        filtered_resources = [res.split(' (')[0].strip() for res in resources_list if any(desired in res for desired in desired_resources)]
        filtered_count = len(filtered_resources)  
        
        return '; '.join(filtered_resources), filtered_count

    new_data = df['Resources'].apply(filter_resources_row)
    df['Filtered Resources'] = new_data.apply(lambda x: x[0])
    df['Filtered Count'] = new_data.apply(lambda x: x[1])

    filtered_df = df[df['Filtered Count'] > 0]

    filtered_df.to_csv(output_file_path, sep='\t', index=False, columns=['Tile', 'Filtered Resources', 'Filtered Count'], header=False)
# Путь до исходного файла и путь сохранения результата
input_path = 'output_tile_resources.csv'
output_path = 'filtered_output.csv'

# Массив желаемых ресурсов
desired_resources = ['iron', 'limestone', 'copper', 'platinum', 'silver', 'tungsten', 'aluminum', 'gold', 'titanium', 'rare earth elements', 'uranium']


# Вызов функции
filter_resources(input_path, output_path, desired_resources)
