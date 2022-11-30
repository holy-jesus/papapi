from random import randint
from time import time
from typing import Any, Literal, Union, List, Dict
import base64
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError

# From https://stackoverflow.com/questions/70038903/


def break_fix(text, width, font, draw):
    """
    Fix line breaks in text.
    """
    if not text:
        return
    if isinstance(text, str):
        text = text.split()  # this creates a list of words

    lo = 0
    hi = len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        t = " ".join(text[:mid])  # this makes a string again
        _, _, w, h = draw.textbbox((0, 0), t, font=font)
        if w <= width:
            lo = mid
        else:
            hi = mid - 1
    t = " ".join(text[:lo])  # this makes a string again
    _, _, w, h = draw.textbbox((0, 0), t, font=font)
    yield t, w, h
    yield from break_fix(text[lo:], width, font, draw)


def fit_text(img, text, color, font, x_start_offset=0, x_end_offset=0, center=False):
    """
    Fit text into container after applying line breaks. Returns the total
    height taken up by the text, which can be used to create containers of
    dynamic heights.
    """
    width = img.size[0] - x_start_offset - x_end_offset
    draw = ImageDraw.Draw(img)
    pieces = list(break_fix(text, width, font, draw))
    height = sum(p[2] for p in pieces)
    y = (img.size[1] - height) // 2
    h_taken_by_text = 0
    for t, w, h in pieces:
        if center:
            x = (img.size[0] - w) // 2
        else:
            x = x_start_offset
        draw.text((x, y), t, font=font, fill=color)
        _, _, new_width, new_height = draw.textbbox((0, 0), t, font=font)
        y += h
        h_taken_by_text += new_height
    return h_taken_by_text


def generate_text_section(
    width, text, color, font, x_start_offset, x_end_offset, v_spacing
):
    """
    Generates an image for a text section.
    """
    # Calculate height using "fake" canvas
    img = Image.new("RGB", (width, 1), color="white")
    calc_height = fit_text(
        img, text.upper(), color, font, x_start_offset, x_end_offset, False
    )

    # Create real canvas and fit text
    img = Image.new("RGB", (width, calc_height + v_spacing), color="white")
    fit_text(img, text.upper(), color, font, x_start_offset, x_end_offset, False)

    return img


def percent_to_pixels(areas, size_of_image):
    return (size_of_image[0] * areas[0], size_of_image[1] * areas[1])


def format(template, csv, fields: Dict[str, Any], preview=False) -> List[Image.Image]:
    template = Image.open(BytesIO(template))
    images = []
    for entry in csv:
        start = time()
        new_image = template.copy()
        draw = ImageDraw.Draw(new_image)
        for name, value in entry.items():
            if "percentage" not in fields[name]:
                continue
            field = fields[name]
            font = ImageFont.truetype(field["font"], int(field["size"]))
            coordinates = percent_to_pixels(field["percentage"], template.size)
            draw.text(
                coordinates,
                text=value,
                fill=(0, 0, 0, 255),
                font=font,
                anchor="mm",
            )
        print(time() - start)
        if preview:
            buffered = BytesIO()
            new_image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue())

        images.append(new_image)
    return images


if __name__ == "__main__":
    image = open("Diploma.png", "rb")
    csv_file = open("test.csv", "r")
    color = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
    images = format(
        image,
        csv_file,
        {
            "ФИО": (
                0.5,
                0.5,
                0.5,
                0.5,
            ),
            "Место": (
                0.6177069028190262,
                0.5972659137562726,
                0.32181547022483903,
                0.24085927857201173,
            ),
        },
        {
            "ФИО": {"font": "Ubuntu-L.ttf", "color": color, "size": 300},
            "Место": {"font": "Ubuntu-L.ttf", "color": color, "size": 300},
        },
    )
    for image in images:
        image.show()
