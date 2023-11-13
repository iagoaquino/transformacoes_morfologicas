from classes.transformacoes import Pixel
from classes.transformacoes import Mask
from classes.transformacoes import Transformacoes
from PIL import Image

def ler_image(image):
    final_image = []
    for i in range(image.width):
        line_pixels = []
        for j in range(image.height):
            r,g,b = image.getpixel((i,j))
            pixel = Pixel(r,g,b)
            line_pixels.append(pixel)
        final_image.append(line_pixels)
    return image.width, image.height, final_image

def form_image(width,height,image,image_compare):
    new_image = Image.new("RGB",(width, height), (255,255,255))
    for i in range(width):
        for j in range(height):
            new_image.putpixel((i,j), (image[i][j].r,image[i][j].g,image[i][j].b))
    new_image.show()

def image_comp(image1,image2):
    image3 = []
    for i in range(image1.width):
        line_image = []
        for j in range(image1.height):
            r1,g1,b1 = image1.getpixel((i,j))
            r2,g2,b2 = image2.getpixel((i,j))
            if r1 == r2:
                line_image.append(Pixel(255,255,255))
            else:
                pixel = Pixel(0,0,0)
                pixel.r,pixel.g,pixel.b = image1.getpixel((i,j))
                line_image.append(pixel)
        image3.append(line_image)
    return image3

def generate_structural_image(size,size_width, size_height):
    mask = []
    for i in range(size):
        line_result = []
        for j in range(size):
            line_result.append(1)
        mask.append(line_result)

    for i in range(size):
        for j in range(size):
            if i <= (int(size/2)) + int(size_width) and i >= (int(size/2)) - int(size_width) or j <= (int(size/2)) + int(size_height) and j >= (int(size/2)) - int(size_height):
                mask[i][j] = 0
            if i == int(size/2) and j == int(size/2):
                print("entrei")
                mask[i][j] = 0
    print(mask)
    return mask


            


def main():
    image = Image.open("exemplo.bmp")
    mask_size = int(input("digite o tamanho da imagem estrutural: "))
    mask_width = int(input("digite a largura dos marcados: "))
    mask_height = int(input("digite a altura dos marcados"))
    width, height, readed_image = ler_image(image)
    conv = Transformacoes(mask_size,readed_image, width, height)
    conv.mask.mask = generate_structural_image(mask_size, mask_width, mask_height)
    final_image = conv.apply_erosion()
    form_image(width, height, final_image, image)


main()