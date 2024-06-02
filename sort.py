def parse_filename(filename):
    parts = filename.split('-')
    row = int(parts[0])
    col = int(parts[1].split('.')[0])
    return row, col

def sort_file(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Удаление пробелов и создание списка кортежей с индексацией исходя из имени файла
    entries = [(parse_filename(line.split(',')[0]), line.strip()) for line in lines]

    # Сортировка первым числом (строка), затем вторым числом (столбец)
    entries.sort(key=lambda x: (x[0][0], x[0][1]))

    # Запись в выходной файл с добавлением порядкового номера
    with open(output_file, 'w') as file:
        for index, (_, line) in enumerate(entries, start=1):
            file.write(f"{index},{line}\n")

# Указать пути к исходному и конечному файлами
input_filepath = 'pixw.txt'
output_filepath = 'pixwsort.txt'
sort_file(input_filepath, output_filepath)