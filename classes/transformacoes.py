class Pixel:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

class Mask:
    def __init__(self, size):
        self.size = size
        self.mask = []

    def put_mask(self, line):
        if self.actual_size <= self.size:
            self.mask.append(line)
        else:
            print("erro maskara completa")

class Transformacoes:
    def __init__(self, size, image, width, height):
        self.mask = Mask(size)
        self.image = image
        self.image_height = height
        self.image_width = width
        self.actual_pos = [0,0]

    def apply_erosion_esq(self):
        image = []
        for i in range(self.image_width):
            line = []
            for j in range(self.image_height):
                repetition = int(self.mask.size/2)
                sumy = -repetition
                should_paint = True
                for k in range(self.mask.size):
                    sumx = -repetition
                    for l in range(self.mask.size):
                        if (i+sumx < 0 or i+sumx >= self.image_width) or (j+sumy < 0 or j+sumy >= self.image_height):
                            #print("saiu - mask: "+str(self.mask.mask[k][l])+" pixel:"+str(1))
                            #print("sumx:"+str(sumx)+", sumy: "+str(sumy))
                            if self.mask.mask[k][l] == 0:
                                should_paint = False
                        else:
                            #print("mask: "+str(self.mask.mask[k][l])+"pixel: "+str(self.image[i+sumx][j+sumy]))
                            #print("sumx:"+str(sumx) + ", sumy"+str(sumy))

                            if self.mask.mask[k][l] == 1 and self.image[i+sumx][j+sumy] == 0:
                                should_paint = False
                                break
                            if self.mask.mask[k][l] == 0 and self.image[i+sumx][j+sumy] == 1:
                                should_paint = False
                                break
                        if should_paint == False:
                            break
                        sumx+=1
                    sumx = -repetition
                    sumy +=1
                if should_paint:
                    line.append(1)
                    #print("saiu\n")
                else:
                    #print("entrou\n")
                    line.append(self.image[i][j])
            #print(line)
            image.append(line)
        return image
    
    def apply_erosion(self):
        image = []
        for i in range(self.image_width):
            line = []
            for j in range(self.image_height):
                repetition = int(self.mask.size/2)
                sumy = -repetition
                should_paint = True
                for k in range(self.mask.size):
                    sumx = -repetition
                    for l in range(self.mask.size):
                        color_point = 1
                        if (i+sumx < 0 or i+sumx >= self.image_width) or (j+sumy < 0 or j+sumy >= self.image_height):
                            if self.mask.mask[k][l] == 0:
                                should_paint = False
                        else:
                            if self.mask.mask[k][l] == 2:
                                break
                            if self.mask.mask[k][l] == 0 and self.image[i+sumx][j+sumy] == 1:
                                should_paint = False
                                break
                        sumx+=1
                    if should_paint == False:
                        break
                    sumx = -repetition
                    sumy +=1
                if should_paint:
                    line.append(0)
                else:
                    line.append(1)
            image.append(line)
        return image
    
    def apply_closure(self):
        self.image = self.apply_dilation()
        return self.apply_erosion()
    
    def apply_intersection(self,img1,img2, width, height):
        image_final = []
        for i in range(width):
            line_pixel = []
            for j in range(height):
                if img1[i][j] == 0 and img2[i][j] == 0:
                    line_pixel.append(1)
                elif img1[i][j] == 1 and img2[i][j] == 1:
                    line_pixel.append(1)
                elif img1[i][j] == 0 and img2[i][j] == 1:
                    line_pixel.append(0)
                else:
                    line_pixel.append(1)
            image_final.append(line_pixel)
        return image_final
    
    def apply_dilation(self):
        image = []
        for i in range(self.image_width):
            line_pixel = []
            for j in range(self.image_height):
                repetition = int(self.mask.size/2)
                sumy = -repetition
                should_paint = False
                for k in range(self.mask.size):
                    sumx = -repetition
                    for l in range(self.mask.size):
                        if (i+sumx < 0 or i+sumx >= self.image_width) or (j+sumy < 0 or j+sumy >= self.image_height):
                            pass
                        else:
                            if self.mask.mask[k][l] == 2:
                                break
                            if self.mask.mask[k][l] == 0 and self.image[i+sumx][j+sumy] == 0:
                                should_paint = True
                                break
                        sumx+=1
                    if should_paint == True:
                        break
                    sumx = -repetition
                    sumy +=1
                if should_paint:
                    line_pixel.append(0)
                else:
                    line_pixel.append(1)
            image.append(line_pixel)
        return image                    
                                
    def remove_intersection(self, width, height, primary_image, secondary_image):
        final_image = []
        for i in range(width):
            line_pixel = []
            for j in range(height):
                if primary_image[i][j] == 0 and secondary_image[i][j] == 0:
                    line_pixel.append(1)
                else:
                    line_pixel.append(secondary_image[i][j])
            final_image.append(line_pixel)
        return final_image


