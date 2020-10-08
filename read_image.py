from PIL import Image
import os
import time

os.chdir("Bachelorarbeit/")

jpgfile = Image.open("picture.jpg")

print(jpgfile.bits, jpgfile.size, jpgfile.format)

print(jpgfile.getexif())

before = time.time()

print(len(list(jpgfile.getdata())))

after = time.time()

print(after - before, "s")