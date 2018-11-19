from abc import ABC, abstractmethod
from reflectance_sensors import ReflectanceSensors
from camera_find_object import FindObject
from ultrasonic import Ultrasonic
from camera import Camera
from PIL import Image


class Sensob(ABC):
    def __init__(self, sensor):
        self.sensor = sensor

    @abstractmethod
    def update(self):
        pass

    def reset(self):
        self.sensor.reset()


class CameraSensob(Sensob):
    def __init__(self, sensor, color=0, filename='image.png'):
        super(CameraSensob, self).__init__(sensor)
        self.color = color  # 0:red, 1:green, 2:blue
        self.image = None   # Image.open(filename)  # the image object
        self.match = 0  # from 0-1 how high color match
        self.xmax = None  # self.image.size[0]  # width of image
        self.ymax = None  # self.image.size[1]  # height of image
        self.array = None  # color distribution array
        self.camera = Camera()
        self.filename = filename

    def update(self):
        self.camera.update()
        self.image = Image.open(self.filename)
        self.xmax = self.image.size[0]
        self.ymax = self.image.size[1]
        self.image = self.keep_one_color(thresh=0.55)
        self.how_much_color_array()
        return self.array
        # returns array eg [0.0, 0.0, 0.0, 0.05, 0.0, 0.24, 0.21, 0.0]

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

    def keep_one_color(self, thresh=0.60):  # change one color to max (255, 0, 0) and the rest to (0,0,0)
        def wta(p):  # winner takes all, p is RGB-tuple
            s = sum(p)
            w = max(p)
            if s > 0 and w / s >= thresh and w == p[self.color]:
                return tuple([(255 if x == w else 0) for x in p])
            else:
                return (0, 0, 0)
        return self.map_image2(wta)

    def reset(self):
        self.camera.reset()


class UltrasonicSensob(Sensob):
    def __init__(self, sensor):
        assert isinstance(sensor, Ultrasonic)
        super(UltrasonicSensob, self).__init__(sensor)

    def update(self):
        return self.sensor.update()
        # returns the distance to object in cm


class ReflectanceSensob(Sensob):
    def __init__(self, sensor):
        assert isinstance(sensor, ReflectanceSensors)
        super(ReflectanceSensob, self).__init__(sensor)

    def update(self):
        return self.sensor.update()
        # returns array eg [1.0, 1.0, 0.5, 0.3, 0.9, 0.7]
