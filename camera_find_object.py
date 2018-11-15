from camera import Camera
from PIL import Image
#from zumo_button import ZumoButton


class FindObject():  # DO NOT USE!

    def __init__(self, color=0, filename='image.png'):
        self.color = color  # 0:red, 1:green, 2:blue
        self.image = Image.open(filename)  # the image object
        self.match = 0  # from 0-1 how high color match
        self.xmax = self.image.size[0]  # width of image
        self.ymax = self.image.size[1]  # height of image
        self.array = None  # color distribution array
        self.zumo_button = ZumoButton()
        self.camera = Camera()

    def how_much_color(self, start, end):  # return a float [0-1] of how much of either R,G or B color
        total = (end - start) * self.ymax  # total number of pixels
        col = 0  # number of matching pixels
        for x in range(start, end):
            for y in range(self.ymax):
                p = self.image.getpixel((x, y))
                if p[self.color] == 255:
                    col += 1
        return col / total

    def how_much_color_array(self):  # divides the image into 8 columns and rund how_much_color for each colum
        array = []
        step = self.xmax // 8
        for i in range(8):
            start = step * i
            end = step * (i + 1)
            amount = self.how_much_color(start, end)
            array.append(float("{0:.2f}".format(amount)))  # runder av
        print(array)
        self.array = array  # eg [0.0, 0.0, 0.0, 0.05, 0.0, 0.24, 0.21, 0.0] where each entry is the amount of color in
        # the corresponging column

    def map_image2(self, func):  # applies the function to each RGB tuple, returning a new imgage with the function
        # applied
        im2 = self.image.copy()
        for i in range(self.xmax):
            for j in range(self.ymax):
                im2.putpixel((i, j), func(im2.getpixel((i, j))))
        return im2

    def keep_one_color(self, thresh=0.55):  # change one color to max (255, 0, 0) and the rest to (0,0,0)
        def wta(p):  # winner takes all, p is RGB-tuple
            s = sum(p)
            w = max(p)
            if s > 0 and w / s >= thresh and w == p[self.color]:
                return tuple([(255 if x == w else 0) for x in p])
            else:
                return (0, 0, 0)
        return self.map_image2(wta)

    # move to behaviour?
    def recomendation(self, threshold=0.05):  # motor recoomendation, maps self.array to degrees and left/right
        maxval = 0  # maximum value
        index = 0  # index of maxval
        for i in range(len(self.array)):  # find maxval and index of maxval in array
            if self.array[i] > maxval:
                maxval = self.array[i]
                index = i
        if maxval < threshold:
            return ('L, 60')
        direction = 'R' if index > 3 else 'L'
        degree = {0: 32, 1: 16, 2: 8, 3: 0, 4: 0, 5: 8, 6: 16, 7: 32}
        return (direction, degree[index])


# test method
def take_picture():
    cfo = FindObject(color=0, filename='image.png')
    for i in range(10):
        cfo.zumo_button.wait_for_press()
        image = cfo.camera.update()
        image.save('image{}.jpg'.format(i))



fo = FindObject(color=0, filename='image1.png')
fo.image = fo.keep_one_color(thresh=0.55)
fo.how_much_color_array()
print(fo.recomendation())
fo.image.show()

