import concurrent.futures
import multiprocessing
import threading
import requests
import time

img_urls = [
 'https://cdn.pixabay.com/photo/2016/04/04/14/12/monitor-1307227_1280.jpg',
 'https://cdn.pixabay.com/photo/2018/07/14/11/33/earth-3537401_1280.jpg',
 'https://cdn.pixabay.com/photo/2016/06/09/20/38/woman-1446557_1280.jpg',
]

def download_image_thread(img_url):
     img_bytes = requests.get(img_url).content
     img_name = img_url.split('/')[9]
     with open(f'thread/{img_name}', 'wb') as img_file:
         img_file.write(img_bytes)
         print(f"{img_name} was downloaded")

def download_image_pool(img_url):
        img_bytes = requests.get(img_url).content
        img_name = img_url.split('/')[9]
        with open(f'pool/{img_name}', 'wb') as img_file:
            img_file.write(img_bytes)
            print(f"{img_name} was downloaded")

def download_image_multiprocess(img_url):
    img_bytes = requests.get(img_url).content
    img_name = img_url.split('/')[9]
    with open(f'multiprocess/{img_name}', 'wb') as img_file:
        img_file.write(img_bytes)
        print(f"{img_name} was downloaded")


def pool() -> float:
    """
    test the time it takes to download images using a thread pool
    :return:
    """
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image_pool, img_urls, )
    end = time.perf_counter()
    return round(end-start, 2)


def threads() -> float:
    """
    test the time it takes to download images using threads
    :return:
    """
    start = time.perf_counter()
    threads = []
    for img_url in img_urls:
        thread = threading.Thread(target=download_image_thread, args=(img_url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    end = time.perf_counter()
    return round(end-start, 2)


def multiprocessing() -> float:
    """
    test the time it takes to download images using multiprocessing
    :return:
    """
    start = time.perf_counter()
    for img in img_urls:
        p = multiprocessing.Process(target=download_image_multiprocess, args=('multiprocess', img))
        p.start()
    end = time.perf_counter()
    return round(end-start, 2)


if __name__ == '__main__':
    print(f"Time using thread pool: {pool()} seconds")
    print(f"Time using threads: {threads()} seconds")
    #print(f"Time using multiprocessing: {multiprocessing()} seconds")