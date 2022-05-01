'''requests==2.27.1'''

from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
import requests
import logging
import os


# Setting up the logger.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s: %(name)s: %(levelname)s: %(message)s')

file_handler = logging.FileHandler('Unsplash-Download.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class Unsplash:

    def __init__(self, search_term: str, imgs_to_download: int) -> None:
        self.search_term = search_term
        self.imgs_to_download = imgs_to_download
        self.page = 1
        self.count = 0
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36"
        }
        self.scrape_unsplash()

    def usplash_api_url(self):
        url = f'https://unsplash.com/napi/search?query={self.search_term}&per_page=20&page={self.page}&xp='
        return url

    def initiate_request(self):
        return requests.get(self.usplash_api_url(), headers=self.header)
    
    def json_data(self) -> dict:
        return self.initiate_request().json()
    
    def extract_img_urls(self) -> list:
        img_urls = list()
        while len(img_urls) < self.imgs_to_download:
            for i in self.json_data()["photos"]["results"]:
                if len(img_urls) == self.imgs_to_download:
                    break
                link = i['urls']['raw']
                link = link.partition('?')[0]
                img_urls.append(link)
            self.page += 1
        return img_urls

    def download_img(self, img_url: str):
        download_dir = f'{self.search_term}'
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        img_bytes = requests.get(img_url, headers=self.header).content
        img_name = img_url.split('/')[3]

        # An if statement to avoid downloading the ad photo (starts with "file" not "photo")
        if img_name[:5] == 'photo':
            img_name = f'{self.search_term}_{self.count + 1}.jpg'
            img_full_path = os.path.join(os.path.realpath(os.getcwd()),download_dir,img_name)
            with open(f'{img_full_path}', 'wb') as image:
                image.write(img_bytes)
                logger.info(f'"{img_name}" is now downloaded!')
                self.count += 1

    def scrape_unsplash(self):
        t1 = perf_counter()
        # Using threading to download the pictures more efficiently.
        with ThreadPoolExecutor() as executor:
            executor.map(self.download_img, self.extract_img_urls())
        t2 = perf_counter()
        elapsed_time = round(t2 - t1, 2)
        logger.info(f'{self.imgs_to_download} images of {self.search_term} have been downloaded in {elapsed_time} seconds')

if __name__ == "__main__":
    search_term = input("What pictures would you like to download? ")
    imgs_to_download = int(input("How many of that would you like to download? "))
    Car_Unsplash = Unsplash(search_term, imgs_to_download)