import asyncio

async def fetch_data(url, delay):
    await asyncio.sleep(delay)
    print(f"完成抓取{url}")
    return f"資料來自{url}"

async def main():
    urls = [("網站1",2), ("網站2", 1), ("網站3", 3)]
    tasks = [fetch_data(url, delay) for url, delay in urls]
    results = await asyncio.gather(*tasks)
    print("所有資料:", results)

asyncio.run(main())