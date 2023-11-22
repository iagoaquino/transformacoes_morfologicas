from PIL import Image
from classes.transformacoes import Pixel
from classes.transformacoes import Mask
from classes.transformacoes import Transformacoes
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

def form_image(width,height,image):
    new_image = Image.new("RGB",(width, height), (255,255,255))
    for i in range(width):
        for j in range(height):
            new_image.putpixel((i,j), (image[i][j].r,image[i][j].g,image[i][j].b))
    new_image.save("painted.bmp")

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
    
def fuse_images(images, width, height):
    final_image = []
    for i in range(width):
        line = []
        for j in range(height):
            line.append(1)
        final_image.append(line)
    
    for i in range(len(images)):
        for j in range(width):
            for k in range(height):
                    if images[i][j][k] == 0:
                        final_image[j][k] = 0
                    
    return final_image

def subtract_images(image1, image2, width, height):
    image_subed = []
    for i in range(width):
        line = []
        for j in range(height):
            if image1[i][j] == 0 and image2[i][j] == 0:
                line.append(1)
            else:
                line.append(image1[i][j])
        image_subed.append(line)
    return image_subed

def main():
    image = Image.open("exemplo.bmp")
    width, height, readed_image = ler_image(image)
    mat = img_to_binary_mat(readed_image, width, height)
    mask = [[1,0,1],[0,0,0],[1,0,1]]
    transform = Transformacoes(3,mat, width, height)
    transform.mask.mask = mask
    images = []
    final_before = []
    for i in range(width):
        line = []
        for j in range(height):
            line.append(mat[i][j])
        final_before.append(line)

    keep_going = True

    while keep_going:
        final_image = []
        for i in range(width):
            line = []
            for j in range(height):
                line.append(1)
            final_image.append(line)
        
        final_image = transform.apply_erosion()
        transform.image = final_image
        new_image = transform.apply_dilation()
        images.append(subtract_images(final_before, new_image, width, height))
        final_before = []

        for i in range(width):
            line = []
            for j in range(height):
                line.append(0)
            final_before.append(line)
        for i in range(width):
            for j in range(height):
                final_before[i][j] = final_before[i][j] + final_image[i][j]
        found_black = False
        cont_black = 0

        for i in range(width):
            for j in range(height):
                if final_before[i][j] == 0:
                    found_black = True
                    cont_black+=1

        print("achei: "+str(cont_black))
        if found_black == False:
            keep_going = False
            break

    result_image = fuse_images(images, width, height)
    result_image = mat_to_binary_img(result_image, width, height)
    form_image(width, height, result_image)

        

    
main()
