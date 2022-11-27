from typing import Literal
from time import time
import csv
import os

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError


class Formatter:
    def __init__(
        self,
        path_to_image: str | bytes,
        path_to_csv_file: str | bytes,
    ) -> None:
        if isinstance(path_to_image, str):
            if not os.path.isfile(path_to_image):
                raise FileNotFoundError("No such image.")
        self.image: Image.Image = Image.open(path_to_image)
        self.csv_list = self.__read_csv(path_to_csv_file)
        self.fields = {}

    def set_field(
        self,
        name: str,
        value: dict[Literal["font", "size", "percentage"], str | int | tuple],
    ):
        percentage = value["percentage"]
        size = self.image.size
        coord_of_element = (size[0] * percentage[0], size[1] * percentage[1])
        value["coordinates"] = coord_of_element
        del value["percentage"]
        self.fields[name] = value

    def get_preview_for_field(self, name: str, text: str = None) -> Image.Image:
        if text is None:
            text = "Тестовый текст"
        field = self.fields[name]
        font = ImageFont.truetype(field["font"], field["size"])
        new_image = self.image.copy()
        draw = ImageDraw.Draw(new_image)
        draw.text(
            xy=field["coordinates"],
            text=text,
            fill=(255, 255, 255),
            font=font,
        )
        return new_image

    def get_columns(self) -> tuple[str]:
        return tuple(self.csv_list[0].keys())

    @staticmethod
    def __read_csv(csv_file: bytes) -> list[dict]:
        csv_list = []
        reader = csv.reader(csv_file)
        first_row = next(reader)
        print(first_row)
        for row in reader:
            print(row)
            csv_dict = {}
            for num in range(len(first_row)):
                csv_dict[first_row[num]] = row[num]
            csv_list.append(csv_dict)
        if not csv_list:
            raise ValueError("You can't pass blank csv file")
        return csv_list

    def format(self) -> list[Image.Image] | Image.Image:
        size = self.image.size
        images = []
        for entry in self.csv_list:
            new_image = self.image.copy()
            print(self.fields)
            draw = ImageDraw.Draw(new_image)
            for name, value in entry.items():
                d = self.fields[name]
                font = ImageFont.truetype(d["font"], int(d["size"]))
                draw.text(
                    (d["coordinates"]),
                    text=value,
                    fill=(0, 0, 0),
                    font=font,
                )
            images.append(new_image)
        return images


if __name__ == "__main__":
    image = open("Diploma.png", "rb")
    formatter = Formatter(
        image,
        "convertcsv.csv",
        {
            "Name": (
                0.18694348694515306,
                0.16599761090773785,
                0.3100826145395584,
                0.24248670612993078,
            ),
            "Test": (
                0.6177069028190262,
                0.5972659137562726,
                0.32181547022483903,
                0.24085927857201173,
            ),
        },
        "Ubuntu-L.ttf",
        256,
    )
    formatter.font = "Ubuntu-L.ttf"
    print(formatter.font)
    formatter.font_size = 300
    for image in formatter.format():
        image.show()
