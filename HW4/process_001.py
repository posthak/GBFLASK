"""" Асинхронная загрузка с использованием модуля asyncio """
import argparse
import asyncio
import aiofiles
import aiohttp
import time

# urls = [
#         'https://ssl.robocup.org/wp-content/uploads/2021/12/20160629-IMG_0283_1.jpg',
#         'https://s.studiobinder.com/wp-content/uploads/2021/01/Best-Black-and-white-pictures.jpg',
#         'https://burst.shopifycdn.com/photos/full-blue-moon.jpg'
#         ]

async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            filename = os.path.basename(url)
            f = await aiofiles.open(filename, mode='wb')
            await f.write(await response.read())
            await f.close()
    print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")

async def main():
    tasks = []
    parser = argparse.ArgumentParser(description='Process a list of URLs.')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='List of URLs to process')
    args = parser.parse_args()
    urls = args.urls
    for url in urls:
        task = asyncio.ensure_future(download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

start_time = time.time()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# задать список URL-адресов через аргументы командной строки
# python3 HW4/process_001.py https://burst.shopifycdn.com/photos/full-blue-moon.jpg https://s.studiobinder.com/wp-content/uploads/2021/01/Best-Black-and-white-pictures.jpg https://ssl.robocup.org/wp-content/uploads/2021/12/20160629-IMG_0283_1.jpg
