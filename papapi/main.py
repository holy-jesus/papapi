import os

import aiofiles
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import base64
from zipfile import ZipFile
from io import BytesIO

from formatter import format

BASE_PATH = os.getcwd()
TEMPLATES_PATH = BASE_PATH + "/templates/"

class Image(BaseModel):
    csv: list
    template: str
    fields: dict

app = FastAPI(debug=True)
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
    return {"image": format(base64.b64decode(image.template), image.csv, image.fields, True)}   
    

@app.post("/format")
def post_format(image: Image):
    images = format(base64.b64decode(image.template), image.csv, image.fields)
    zip_io = BytesIO()
    zip_obj = ZipFile(zip_io, "w")
    for num, image in enumerate(images, start=1):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        zip_obj.writestr(f"{num}.png", buffered.getvalue())


if __name__ == "__main__":
    # For debug
    import uvicorn

    uvicorn.run(app, host="localhost", port=5000)