from time import time
import csv
import os

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError


class Formatter:
    def __init__(
        self,
        path_to_image: str | bytes,
        path_to_csv_file: str | bytes,
        areas: dict[str, tuple],
        font: str = None,
        font_size: int = 32,
    ) -> None:
        if isinstance(path_to_image, str):
            if not os.path.isfile(path_to_image):
                raise FileNotFoundError("No such image.")
        self.image: Image.Image = Image.open(path_to_image)
        if isinstance(path_to_csv_file, str):

            if not os.path.isfile(path_to_csv_file):
                raise FileNotFoundError("No such csv file.")
            elif os.path.isfile(path_to_csv_file):
                csv_file = open(path_to_csv_file, "r")
        else:
            csv_file = path_to_csv_file
        self.csv_list = self.__read_csv(csv_file)
        self._font_size = font_size
        if font is None:
            self._font_filename = "Ubuntu-L.ttf" if os.name == "Linux" else "arial.ttf"
            self._font = ImageFont.truetype(self._font_filename, self._font_size)
        else:
            self._font_filename = font
            self._font = ImageFont.truetype(font, self._font_size)
        print(self.csv_list)
        self.areas = areas

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, value: int):
        if value >= 0:
            self._font_size = value
            if self._font_filename:
                self._font = ImageFont.truetype(self._font_filename, self._font_size)

        else:
            raise ValueError("Font size cant be negative")
    
    @property
    def font(self):
        return self._font_filename

    @font.setter
    def font(self, value: str):
        self._font = ImageFont.truetype(value, self.font_size)
        self._font_filename = value

    @staticmethod
    def __read_csv(csv_file: bytes) -> list[dict]:
        csv_list = []
        reader = csv.reader(csv_file)
        first_row = next(reader)
        for row in reader:
            csv_dict = {}
            for num in range(len(first_row)):
                csv_dict[first_row[num]] = row[num]
            csv_list.append(csv_dict)
        return csv_list

    def format(self, text = None) -> list[Image.Image] | Image.Image:
        size = self.image.size
        images = []
        for entry in self.csv_list:
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            for name, value in entry.items():
                percent = self.areas[name]
                size_of_element = (
                    size[0] * percent[0],
                    size[1] * percent[1],
                    size[0] * percent[2],
                    size[1] * percent[3],
                )
                draw.text(
                    (size_of_element[0], size_of_element[1]),
                    text=text or value,
                    fill=(0, 0, 0),
                    font=self._font,
                )
            if text:
                return new_image
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
    # image = formatter.make_preview("Ubuntu-L.ttf", 300
