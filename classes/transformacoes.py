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
    
    def apply_erosion(self):
        image = []
        for i in range(self.image_width):
            line_pixel = []
            for j in range(self.image_height):
                repetition = int(self.mask.size/2)
                sumy = -repetition
                should_paint = True
                for k in range(self.mask.size):
                    sumx = -repetition
                    for l in range(self.mask.size):
                        color_point = 1
                        if (i+sumx < 0 or i+sumx >= self.image_width) or (j+sumy < 0 or j+sumy >= self.image_height):
                            color_point = 1
                        else:
                            if self.image[i+sumx][j+sumy].r > 0:
                                color_point = 1
                            else:
                                color_point = 0
                        
                        if self.mask.mask[k][l] == 0 and color_point == 1:
                            should_paint = False
                            break
                        sumx+=1
                    if should_paint == False:
                        break
                    sumx = -repetition
                    sumy +=1
                if should_paint:
                    line_pixel.append(Pixel(0,0,0))
                else:
                    line_pixel.append(Pixel(255,255,255))
            image.append(line_pixel)
        return image

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
                        color_point = 1
                        if (i+sumx < 0 or i+sumx >= self.image_width) or (j+sumy < 0 or j+sumy >= self.image_height):
                            color_point = 1
                        else:
                            if self.image[i+sumx][j+sumy].r > 0:
                                color_point = 1
                            else:
                                color_point = 0
                        
                        if self.mask.mask[k][l] == 0 and color_point == 0:
                            should_paint = True
                            break
                        sumx+=1
                    if should_paint == True:
                        break
                    sumx = -repetition
                    sumy +=1
                if should_paint:
                    line_pixel.append(Pixel(0,0,0))
                else:
                    line_pixel.append(Pixel(255,255,255))
            image.append(line_pixel)
        return image
                    
                        
                                
                            
    def applyconv(self):
        image = []
        for i in range(self.image_width):
            line_result = []
            for j in range(self.image_height):
                repetition = int(self.mask.size/2)
                result = Pixel(0,0,0)
                sumy = -repetition
                for k in range(self.mask.size):
                    sumx = -repetition
                    
                    for l in range(self.mask.size):
                        if (i+sumx < 0 or i+sumx >= self.image_width) or (j+sumy < 0 or j+sumy >= self.image_height):
                            result.r+= 0
                            result.g+= 0
                            result.b+= 0
                        else:
                            #print("rgb("+str(self.image[i+sumx][j+sumy].r) +", "+ str(self.image[i+sumx][j+sumy].g)+ ", "+str(self.image[i+sumx][j+sumy].r)+")")
                            #print("pos("+str(k)+", "+str(l)+")"+str(self.mask.mask[k][l]) +"*"+str(self.image[i+sumx][j+sumy].r)+" (sumx:"+str(sumx)+": sumy"+str(sumy))
                            result.r += self.image[i+sumx][j+sumy].r * self.mask.mask[k][l]
                            result.g += self.image[i+sumx][j+sumy].g * self.mask.mask[k][l]
                            result.b += self.image[i+sumx][j+sumy].b * self.mask.mask[k][l]
                        sumx+=1
                    sumy+=1
                    sumx= -repetition
                line_result.append(result)
            image.append(line_result)
        return image



