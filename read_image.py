from PIL import Image
import os
import time

os.chdir("Bachelorarbeit/")

jpgfile = Image.open("picture.jpg")

print(jpgfile.getexif())

(width, height) = (jpgfile.width, jpgfile.height)

for i in range(4):

    print("--------------------------- Iteration:", i, "---------------------------")

    (width, height) = (width // 2, height // 2)

    jpgfile.thumbnail((width, height), Image.BILINEAR)

    print(jpgfile.bits, jpgfile.size, jpgfile.format)

    before = time.time()

    print(len(list(jpgfile.getdata())))

    after = time.time()

jpgfile.save("new_pic.jpg", "JPEG")