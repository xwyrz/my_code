import os

from PIL import Image

root_dir = '/home/images/'


def iter_files(path):
    # 遍历根目录
    for root, dirs, files in os.walk(path):
        for file in files:
            file_name = os.path.join(root, file)
            print(file_name)
            change_image_wight(file_name)

            
# 转换为webp
def to_webp(pic_path):
    file_name, file_type = os.path.splitext(pic_path)
    if file_type in [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]:
        im = Image.open(pic_path)
        im.save(f"{file_name}.webp", "WEBP")
        print(f"{file_name}.webp - success saved!")
        # os.remove(pic_path)
        print(f"{pic_path} - success deleted!")

        
# 修改图片宽度并删除除图片外其他格式文件！
def change_image_wight(pic_path):
    file_name, file_type = os.path.splitext(pic_path)
    if file_type in [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".webp"]:
        new_width = 980
        try:
            img = Image.open(pic_path)
            wpercent = (new_width / float(img.size[0]))
            height_size = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((new_width, height_size), Image.ANTIALIAS)
            img.save(f"{file_name}.jpg")
        except Exception as e:
            print(e.__class__, e)
        if file_type != ".jpg":
            os.remove(pic_path)
            print(f"{pic_path} - success deleted!")


iter_files(root_dir)
