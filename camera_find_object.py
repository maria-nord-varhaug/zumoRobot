from camera import Camera
from PIL import Image


class FindObject():
    def __init__(self, color=0, filename='image.jpg'):
        self.color = color  # 0:red, 1:green, 2:blur
        self.image = Image.open(filename)  # the image object
        self.match = 0  # from 0-1 how high color match
        self.xmax = self.image.size[0]
        self.ymax = self.image.size[1]
        self.array = None
        # self.image.show()

    def how_much_color(self, start, end, color,):
        total = (end-start) * self.ymax
        col = 0
        for x in range(start, end):
            for y in range(self.ymax):
                p = self.image.getpixel((x, y))
                if p[color] == 255:
                    col += 1
        return col/total

    def how_much_color_array(self, color=0):
        array = []
        step = self.xmax//8
        for i in range(8):
            start = step*i
            end = step*(i+1)
            amount = self.how_much_color(start, end, color)
            array.append(float("{0:.2f}".format(amount)))  # runder av
        print(array)
        self.array = array

    def map_image2(self, func):
        im2 = self.image.copy()
        for i in range(self.xmax):
            for j in range(self.ymax):
                im2.putpixel((i, j), func(im2.getpixel((i, j))))
        return im2

    def keep_one_color(self, color=0, thresh=0.34):
        def wta(p):
            s = sum(p); w = max(p)
            if s > 0 and w/s >= thresh and w == p[color]:
                return tuple([(255 if x == w else 0) for x in p])
            else:
                return (0, 0, 0)
        return self.map_image2(wta)

    def recomendation(self, threshold=0.05):
        maxval = 0
        index = 0
        for i in range(len(self.array)):
            if self.array[i] > maxval:
                maxval = self.array[i]
                index = i
        if maxval < threshold:
            return ('L, 60')
        if index > 3: direction = 'R'
        else: direction = 'L'
        degree = {0:32, 1:16, 2:8, 3:0, 4:0, 5:8, 6:16, 7:32}
        return (direction, degree[index])


fo = FindObject(color=0, filename='image.jpg')
fo.image = fo.keep_one_color(thresh=0.9)
fo.how_much_color_array()
print(fo.recomendation())
fo.image.show()
