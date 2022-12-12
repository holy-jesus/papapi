import os
from string import ascii_letters, digits
from random import choice
import asyncio
import glob

import aiofiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import base64
from zipfile import ZipFile
from io import BytesIO

from formatter import format

DEBUG = __name__ == "__main__"
BASE_PATH = os.getcwd()
TEMPLATES_PATH = BASE_PATH + "/templates/"
TEMP_DIR_PATH = "/tmp/"
for file in glob.glob(TEMP_DIR_PATH + "*.zip"):
    if len(file.split("/")[-1]) == 36:
        os.remove(file)
        print(file)

formatting = {}


class Image(BaseModel):
    csv: list
    template: str
    fields: dict


app = FastAPI(debug=DEBUG)
app.mount("/static", StaticFiles(directory="./static"), name="static")


async def open_template(filename: str):
    file = await aiofiles.open(TEMPLATES_PATH + filename, "r")
    content = await file.read()
    await file.close()
    return content


@app.get("/", response_class=HTMLResponse)
async def index():
    return await open_template("index.html")


@app.get("/second_step", response_class=HTMLResponse)
async def second_step():
    return await open_template("second_step.html")


@app.get("/third_step", response_class=HTMLResponse)
async def third_step():
    return await open_template("third_step.html")


@app.get("/result", response_class=HTMLResponse)
async def result():
    return await open_template("result.html")


@app.post("/preview")
def post_preview(image: Image):
    return {
        "image": format(base64.b64decode(image.template), image.csv, image.fields, True)
    }


def task_format(image, id):
    images = format(base64.b64decode(image.template), image.csv, image.fields)
    zip_io = BytesIO()
    zip_obj = ZipFile(zip_io, "w")
    for num, image in enumerate(images, start=1):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        zip_obj.writestr(f"{num}.png", buffered.getvalue())
    zip_obj.close()
    open(TEMP_DIR_PATH + id + ".zip", "wb").write(zip_io.getvalue())
    formatting[id] = True


@app.post("/format")
async def post_format(image: Image):
    id = "".join(choice(ascii_letters + digits) for i in range(32))
    asyncio.create_task(asyncio.to_thread(task_format, image, id))
    formatting[id] = False
    return {"id": id}


@app.get("/status")
def status(id: str):
    return {"done": formatting[id]}


@app.get("/download")
def download(id: str):
    if id in formatting:
        if formatting[id]:
            return FileResponse(TEMP_DIR_PATH + id + ".zip", filename="Дипломы.zip")
        else:
            # Значит человек пытается либо сломать сайт и пытается скачать ещё не сделанный архив
            # Либо произошёл баг
            ...
    else:
        return Response(content={"error": "Invalid ID"}, status_code=404)

if DEBUG:
    # For debug
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)
