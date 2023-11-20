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
    new_image.save("painted.bmp")

def img_to_binary_mat(image, width, height):
    mat_final = []
    for i in range(width):
        line = []
        for j in range(height):
            if (image[i][j].r+image[i][j].g+image[i][j].b) >= 1:
                line.append(1)
            else:
                line.append(0)
        mat_final.append(line)
    return mat_final

def mat_to_binary_img(mat,width, height):
    image_final = []
    for i in range(width):
        line_pixel = []
        for j in range(height):
            if mat[i][j] == 1:
                line_pixel.append(Pixel(255,255,255))
            if mat[i][j] == 0:
                line_pixel.append(Pixel(0,0,0))
        image_final.append(line_pixel)
    return image_final
                
def generate_structural_element(size,size_width, size_height):
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
                mask[i][j] = 0
    print(mask)
    return mask

def floodfill_Morfologico(image, pos_click, width, height, mask):
        final_image = []
        for i in range(width):
            line = []
            for j in range(height):
                line.append(1)
            final_image.append(line)
        final_image[pos_click[0]][pos_click[1]] = 0
        floodfill = Transformacoes(3,final_image,width, height)
        floodfill.mask.mask = mask
        while True:
            image_comp = []
            for i in range(width):
                line = []
                for j in range(height):
                    if final_image[i][j] == 0:
                        line.append(0)
                    else:
                        line.append(1)
                image_comp.append(line)
            final_image = floodfill.apply_dilation()
            final_image = floodfill.remove_intersection(width, height, image, final_image)
            cont_diff = 0
            different = False
            for i in range(width):
                for j in range(height):
                    if final_image[i][j] != image_comp[i][j]:
                        different = True
                        cont_diff += 1
            if different == False:
                print("entrei")
                break
            floodfill.image = final_image
        fused_images = []
        for i in range(width):
            line = []
            for j in range(height):
                if final_image[i][j] == 0 or image[i][j] == 0:
                    line.append(0)
                else:
                    line.append(1)
            fused_images.append(line)
        return fused_images


            
            



def main():
    image = Image.open("exemplo.bmp")
    mask_size = int(input("digite o tamanho da imagem estrutural: "))
    mask_width = int(input("digite a largura dos marcados: "))
    mask_height = int(input("digite a altura dos marcados"))
    width, height, readed_image = ler_image(image)
    readed_image = img_to_binary_mat(readed_image,width,height)
    final_image = floodfill_Morfologico(readed_image, [120,10], width, height, generate_structural_element(mask_size, mask_width, mask_height))
    final_image = mat_to_binary_img(final_image, width, height)
    form_image(width, height, final_image, image)


main()