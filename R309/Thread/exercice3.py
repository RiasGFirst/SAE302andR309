import time
import concurrent.futures
import requests

img_urls = [
 'https://cdn.pixabay.com/photo/2016/04/04/14/12/monitor-1307227_1280.jpg',
 'https://cdn.pixabay.com/photo/2018/07/14/11/33/earth-3537401_1280.jpg',
 'https://cdn.pixabay.com/photo/2016/06/09/20/38/woman-1446557_1280.jpg',
]

def download_image(img_url):
     img_bytes = requests.get(img_url).content
     img_name = img_url.split('/')[9]
     print(img_name)
     with open(img_name, 'wb') as img_file:
         img_file.write(img_bytes)
         print(f"{img_name} was downloaded")


if __name__ == '__main__':
     start = time.perf_counter()
     with concurrent.futures.ThreadPoolExecutor() as executor:
         executor.map(download_image, img_urls)
         end = time.perf_counter()
