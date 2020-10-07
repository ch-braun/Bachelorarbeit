from PIL import Image
import os

os.chdir("Bachelorarbeit/")

jpgfile = Image.open("picture.jpg")

print(jpgfile.bits, jpgfile.size, jpgfile.format)

print(jpgfile.getexif())

print(len(list(jpgfile.getdata())))