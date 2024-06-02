import requests
import os

def download_files(url_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)  # Создать папку, если она не существует

    with open(url_file, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()  # Удаление пробельных символов с начала и конца строки
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Вызвать исключение, если в ответе ошибка HTTP

                # Определение имени файла для сохранения
                file_name = os.path.basename(url)
                save_path = os.path.join(target_folder, file_name)

                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"Файл {file_name} сохранён в {save_path}")
            except requests.RequestException as e:
                print(f"Ошибка при загрузке {url}: {e}")

# Запуск функции с указанием файла и папки для сохранения
download_files('file_url_treecover.txt', 'downloaded_files')