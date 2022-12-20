from random import randint
from time import time
from typing import Any, Tuple, List, Dict
import base64
from io import BytesIO
import os.path

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError


def getbbox(text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int, int]:
    _, _, w, word_h = font.getbbox(text)
    h = word_h
    if "\n" in text:
        h = word_h * (text.count("\n") + 1)
        all_w = []
        for word in text.split("\n"):
            w, _, _ = getbbox(word, font)
            all_w.append(w)
        w = max(all_w)
    return w, h, word_h


def start_point(text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    x, y, _, _ = font.getbbox(text)
    return -x, -y


def break_text(
    text: str, font: ImageFont.FreeTypeFont, allowed_width: int, allowed_height: int
) -> Tuple[str, int, int]:
    if isinstance(text, str):
        splitted = text.split()
    text = ""
    for num, word in enumerate(splitted):
        width, height, word_height = getbbox(text + word, font)
        if num == 0:
            if (
                width > allowed_width
                or word_height * (text.count("\n") + 2) > allowed_height
            ):
                return None, width, height
        if width > allowed_width:
            width, height, word_height = getbbox(text[:-1] + "\n" + word, font)
            if height > allowed_height:
                text = text + " ".join(splitted[num:])
                width, height, word_height = getbbox(text, font)
                if width < allowed_width:
                    return text, width, height
                else:
                    return None, width, height
            text = text[:-1] + "\n" + word + " "
        else:
            text += word + " "
    if width > allowed_width:
        return None, width, height
    return text[:-1], width, height


def fit_text(
    text: str,
    font: ImageFont.FreeTypeFont,
    allowed_width: int,
    allowed_height: int,
    unbreakable: bool = None,
) -> Tuple[ImageFont.FreeTypeFont, str]:
    text = text.strip()
    width, height, _ = getbbox(text, font)
    if width > allowed_width and not unbreakable:
        # Если ширина текста слишком большая, разбиваем текст на несколько частей
        new_text, width, height = break_text(text, font, allowed_width, allowed_height)
        if new_text:
            text = new_text
        else:
            return fit_text(text, font, allowed_width, allowed_height, True)
    elif (width > allowed_width or height > allowed_height) or unbreakable is not None:
        # Если текст слишком большой по ширине и высоте, то уменьшаем текст разбивая
        # его на несколько частей
        start = 0
        end = font.size
        while True:
            font_range = range(start, end)
            if len(font_range) == 1:
                font_size = font_range[0]
                break
            font_size = font_range[len(font_range) // 2]
            new_font = font.font_variant(size=font_size)
            width, height, _ = getbbox(text, new_font)
            if height > allowed_height and width > allowed_width:
                # Если у нас шрифт слишком большой, то просто уменьшаем его
                end = font_size
            elif width > allowed_width:
                # Если ширина текста слишком большая, разбиваем текст на несколько частей
                new_text, width, height = break_text(
                    text, new_font, allowed_width, allowed_height
                )
                if new_text:  # Если пришёл текст, значит подходит по размерам.
                    text = new_text
                else:  # Если нет, то слишком большой шрифт, уменьшаем.
                    end = font_size
            elif height <= allowed_height and width <= allowed_width:
                # Если у нас слишком маленький шрифт, то увеличиваем его.
                # Кстати, чёрт его знает почему, но если убрать <=, то он просто
                # не выходит из цикла и я понять не могу почему.
                start = font_size
            elif height >= allowed_height and width <= allowed_width:
                end = font_size
            else:
                # Вот этого точно не должно произойти
                raise Exception("BRUH")
        font = font.font_variant(size=font_size)
    return font, text


def percent_to_pixels(areas, size_of_image):
    return (
        size_of_image[0] * areas['start'][0],
        size_of_image[1] * areas['start'][1],
        size_of_image[0] * areas['end'][0],
        size_of_image[1] * areas['end'][1],
    )


def get_font_path(font_name):
    for path in ("/tmp/font/", "./static/fonts/"):
        if os.path.exists(path + font_name):
            return path + font_name


def format(template, csv, fields: Dict[str, Any], preview=False) -> List[BytesIO]:
    template = Image.open(BytesIO(template))
    images = []
    for entry in csv[:-1]:
        new_image = template.copy()
        draw = ImageDraw.Draw(new_image)
        for name, value in entry.items():
            if not fields[name]["percentage"]:
                continue
            field = fields[name]
            font = ImageFont.truetype(get_font_path(field["font"]), int(field["size"]))
            x, y, w, h = percent_to_pixels(field["percentage"], template.size)
            top = min(y, h)
            left = min(x, w)
            height = max(y, h)
            width = max(x, w)
            font, text = fit_text(value, font, width - left, height - top)
            draw.text(
                (left, top),
                text=text,
                fill=fields[name]["color"],
                font=font,
            )
        if preview:
            new_image.thumbnail((1024, 1024), Image.ANTIALIAS)
            buffered = BytesIO()
            new_image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue())
        buffered = BytesIO()
        new_image.save(buffered, "PNG")
        images.append(buffered)
    return images
