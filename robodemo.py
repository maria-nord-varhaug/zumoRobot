__author__ = 'keithd'

from time import sleep
import random
import imager2 as IMR
from reflectance_sensors import ReflectanceSensors
from camera import Camera
from motors import Motors
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
from sensobs import UltrasonicSensob, ReflectanceSensob, CameraSensob
import RPi.GPIO as GPIO


## BE SURE TO RUN THESE DEMOS ON THE FLOOR or to have plenty of people guarding
## #  the edges of a table if it is run there.

# This just moves the robot around in a fixed dance pattern.  It uses no sensors.

def dancer():
    ZumoButton().wait_for_press()
    m = Motors()
    m.forward(.2,3)
    m.backward(.2,3)
    m.right(.5,3)
    m.left(.5,3)
    m.backward(.3,2.5)
    m.set_value([.5,.1],10)
    m.set_value([-.5,-.1],10)


# This tests the UV (distance) sensors.  The robot moves forward to within 10 cm of the nearest obstacle.  It
# then does a little dancing before backing up to approximately 50 cm from the nearest obstacle.

def explorer(dist=10):
    ZumoButton().wait_for_press()
    m = Motors(); u = Ultrasonic()
    while u.update() > dist:
        m.forward(.2,0.2)
    m.backward(.1,.5)
    m.left(.5,3)
    m.right(.5,3.5)
    sleep(2)
    while u.update() < dist*5:
        m.backward(.2,0.2)
    m.left(.75,5)



def random_step(motors,speed=0.25,duration=1.0):
    dir = random.choice(['forward','backward','left','right'])
    eval('Motors.'+ dir)(motors,speed,duration)

# This moves around randomly until it gets to a dark spot on the floor (detected with the infrared belly sensors).
# It then rotates around, snapping pictures as it goes.  It then pastes all the pictures together into a
# panoramo view, many of which may be created per "vacation".

def tourist(steps=25,shots=5,speed=.25):
    ZumoButton().wait_for_press()
    rs = ReflectanceSensors(); m = Motors(); c = Camera()
    for i in range(steps):
        random_step(m,speed=speed,duration=0.5)
        vals = rs.update()
        if sum(vals) < 1:  # very dark area
            im = shoot_panorama(c,m,shots)
            im.dump_image('vacation_pic'+str(i)+'.jpeg')

def shoot_panorama(camera,motors,shots=5):
    s = 1
    im = IMR.Imager(image=camera.update()).scale(s,s)
    rotation_time = 3/shots # At a speed of 0.5(of max), it takes about 3 seconds to rotate 360 degrees
    for i in range(shots-1):
        motors.right(0.5,rotation_time)
        im = im.concat_horiz(IMR.Imager(image=camera.update()))
    return im


def spin():  # attemts to spin around 360 degrees
    ZumoButton().wait_for_press()
    motors = Motors()
    motors.set_value((-0.5, 0.5), 1)

def vsvingrask():
    speed = 0.5
    ZumoButton().wait_for_press()
    motors = Motors()
    motors.set_value((speed/2,speed/2),1)
    motors.set_value((0.3,-0.3),1)
    motors.set_value((speed/2, speed/2), 1)

def vsvingsakte():
    speed = 0.5
    ZumoButton().wait_for_press()
    motors = Motors()
    motors.set_value((speed / 2, speed / 2), 1)
    motors.set_value((speed, -speed), 0.1)
    motors.set_value((speed / 2, speed / 2), 1)

def sving(speed,dur):
    ZumoButton().wait_for_press()
    motors = Motors()
    motors.set_value((speed / 2, speed / 2), 1)
    motors.set_value((speed, -speed), dur)
    motors.set_value((speed / 2, speed / 2), 1)

def avstand():
    ult_sensor = Ultrasonic()
    ultrasonic_sensob = UltrasonicSensob(ult_sensor)
    for i in range(0,100):
        print(ultrasonic_sensob.update())
        sleep(0.1)

def underside(auto_C=False,max=100000,min=0):
    try:
        ref_sensor = ReflectanceSensors(auto_calibrate=auto_C,min_reading=min,max_reading=max)
        reflectance_sensob = ReflectanceSensob(ref_sensor)
        while True:
            print(reflectance_sensob.update())
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

def camera():
    camera_sensob = CameraSensob(None, color=0)
    for i in range(0, 15):
        ZumoButton().wait_for_press()
        print('\nPicture:')
        image = camera_sensob.update()
        image.save('image{}.jpg'.format(i))


