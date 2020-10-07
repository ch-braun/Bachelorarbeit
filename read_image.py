from PIL import Image
jpgfile = Image.open("picture.jpg")

print(jpgfile.bits, jpgfile.size, jpgfile.format)