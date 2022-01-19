import os

from PIL import Image

# root dir
root_dir = '/'


def iter_files(path):
    # 遍历根目录
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name = os.path.join(root, file)
            print(file_name)
            to_webp(file_name)


def to_webp(pic_path):
    file_name, file_type = os.path.splitext(pic_path)
    if file_type in [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]:
        im = Image.open(pic_path)
        im.save(f"{file_name}.webp", "WEBP")
        print(f"{file_name}.webp - success saved!")
        os.remove(pic_path)
        print(f"{pic_path} - success deleted!")


iter_files(root_dir)
