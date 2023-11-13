from PIL import Image

def main():
    image = Image.new("RGB", (400,200), (255,255,255))
    for i in range(100):
        for j in range(200):
            image.putpixel((i,j), (0,0,0))
    for i in range(200):
        for j in range(100):
            image.putpixel((i+100,j+50), (0,0,0))
    for i in range(100):
        for j in range(200):
            image.putpixel((i+300,j), (0,0,0))
    image.save("exemplo.bmp")
main()