import os
import requests
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from time import time

# Функция для скачивания изображения
def download_image(url, folder):
    try:
        start_time = time()
        response = requests.get(url, stream=True)
        response.raise_for_status()
        filename = os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        end_time = time()
        print(f"Downloaded {filename} in {end_time - start_time:.2f} seconds")
        return filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

# Основная функция для многопоточной и многопроцессорной загрузки изображений
def download_images(urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    start_time = time()

    # Многопоточная загрузка с помощью ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(download_image, url, folder) for url in urls]
        for future in futures:
            future.result()  # Wait for all threads to complete

    # Многопроцессорная загрузка с помощью Pool
    with Pool(processes=4) as pool:
        results = [pool.apply_async(download_image, (url, folder)) for url in urls]
        for result in results:
            result.get()  # Wait for all processes to complete

    end_time = time()
    print(f"Total time: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    import sys
    urls = sys.argv[1:]
    folder = 'static/images'
    download_images(urls, folder)