import asyncio
import os
import re

import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import tqdm

BASE_URL = "https://link.springer.com/"
BASE_FOLDER = "Springer"
CONN_LIMIT = 100
TIMEOUT = 3600


def create_folders(books):
    for topic in books["English Package Name"].unique():
        os.makedirs(f"{BASE_FOLDER}/{topic}", exist_ok=True)


def get_valid_title(value):
    value = re.sub(r"[\:\/\®]+", "-", value)
    return value


async def download_book(session, book, href, ext):
    async with session.get(f"{BASE_URL}/{href}") as response:
        topic = book["English Package Name"]
        title = get_valid_title(book["Book Title"])
        filename = f'{title}, {book["Author"]}, {book["Edition"]}.{ext}'
        filepath = f"{BASE_FOLDER}/{topic}/{filename}"
        if not os.path.exists(filepath):
            with open(filepath, "wb") as fh:
                fh.write(await response.content.read())


async def fetch(session, book):
    async with session.get(book["OpenURL"]) as response:
        text = await response.text()
        soup = BeautifulSoup(text, "html.parser")
        a_pdf = soup.find("a", class_="test-bookpdf-link")
        a_epub = soup.find("a", class_="test-bookepub-link")
        if a_pdf:
            href_pdf = a_pdf.get("href")
            await download_book(session, book, href_pdf, "pdf")
        if a_epub:
            href_ebook = a_epub.get("href")
            await download_book(session, book, href_ebook, "epub")


async def main():
    tout = aiohttp.ClientTimeout(total=TIMEOUT)
    conn = aiohttp.TCPConnector(limit=CONN_LIMIT)
    async with aiohttp.ClientSession(connector=conn, timeout=tout) as session:
        tasks = [fetch(session, book) for _, book in books.iterrows()]
        for task in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await task


if __name__ == "__main__":
    books = pd.read_csv("./books.csv")
    create_folders(books)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
