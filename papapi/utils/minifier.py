from glob import glob
import os
from urllib.parse import quote_plus
import asyncio

import aiohttp
import aiofiles

IGNORE = ["papaparse.js"]
API_URL = "https://www.toptal.com/developers/javascript-minifier/api/raw"
files = [
    file
    for file in glob(os.getcwd() + "/**/*.js", recursive=True)
    if ".min." not in file and not any(filename in file for filename in IGNORE)
]


async def minify_file(path_to_file: str, session: aiohttp.ClientSession):
    file = await aiofiles.open(path_to_file, "r")
    content = quote_plus(await file.read())
    await file.close()
    response = await session.post(
        API_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="input=" + content,
    )
    if response.status == 200:
        min_js_path = path_to_file.replace(".js", ".min.js")
        mified_content = (await response.content.read()).decode("utf-8")
        min_file = await aiofiles.open(min_js_path, "w")
        await min_file.write(mified_content)
        await min_file.close()
        print(f"Сделал {min_js_path}.")
    else:
        json = await response.json()
        text = ""
        for error in json["errors"]:
            text += f"Статус код: {error['status']}\n"
            text += f"Название ошибки: {error['title']}\n"
            text += f"Описание ошибки: {error['detail']}\n"
        print(text)


async def main():
    session = aiohttp.ClientSession()
    await asyncio.gather(*[minify_file(file, session) for file in files])
    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
