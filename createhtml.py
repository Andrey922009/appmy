import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Чтение данных из CSV
data = pd.read_csv('csvforhtml.csv', delimiter='\t')
print(data.columns)  # Вывод названий колонок для проверки

# Добавление HTML тегов для изображений в колонку Filename
data['Filename'] = data['Filename'].apply(lambda x: f'<img src="tiles_phy_128/{x}" alt="{x}" width="64" height="64">')

# Подготовка Jinja2 для генерации HTML
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

# Рендеринг HTML с данными
html_output = template.render(table=data.to_html(escape=False, index=False))

# Сохранение HTML в файл
with open('outputx.html', 'w', encoding='utf-8') as file:
    file.write(html_output)

print("HTML файл успешно создан!")