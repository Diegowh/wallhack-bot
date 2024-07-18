import io
import os
from discord import File
# from PIL import Image


class ImageLoader:
    def __init__(self):
        self.static_dir = "src\\static"

    def get_item_images(self, category: str, item: str) -> list[File]:
        img_dir = os.path.join(self.static_dir, category)
        files = []
        index = 0

        while True:
            filename = f"{category}_{item}{index}.png"
            filepath = os.path.join(img_dir, filename)

            if not os.path.isfile(filepath):
                break
            file = File(filepath, filename)
            files.append(file)
            index += 1

        return files

    # def resize_image(self, filepath: str, size: tuple[int, int], filename: str) -> File:
    #     with Image.open(filepath) as img:
    #         img = img.resize(size, Image.ANTIALIAS)
    #         buffer = io.BytesIO()
    #         img.save(buffer, format="PNG")
    #         buffer.seek(0)
    #         return File(fp=buffer, filename=filename)
