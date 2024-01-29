"""" Обычная синхронная загрузка """
import argparse
import requests
import time

# urls = [
#         'https://ssl.robocup.org/wp-content/uploads/2021/12/20160629-IMG_0283_1.jpg',
#         'https://s.studiobinder.com/wp-content/uploads/2021/01/Best-Black-and-white-pictures.jpg',
#         'https://burst.shopifycdn.com/photos/full-blue-moon.jpg'
#         ]

def download(urls):
    for url in urls:
        response = requests.get(url)
        filename = url.strip().split('/')[-1].strip()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description='Process a list of URLs.')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='List of URLs to process')
    args = parser.parse_args()
    download(args.urls)

start_time = time.time()
if __name__ == '__main__':
    main()

# задать список URL-адресов через аргументы командной строки
# python3 HW4/process_004.py https://burst.shopifycdn.com/photos/full-blue-moon.jpg https://s.studiobinder.com/wp-content/uploads/2021/01/Best-Black-and-white-pictures.jpg https://ssl.robocup.org/wp-content/uploads/2021/12/20160629-IMG_0283_1.jpg
