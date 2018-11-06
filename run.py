from arbitrator import Arbitrator
from bbcon import Bbcon
from behavior import Behavior, DontCrash, FollowLine, FindColoredObject
from camera import Camera
from motob import Motob
from motors import Motors
from reflectance_sensors import ReflectanceSensors
from sensobs import Sensob, CameraSensob, UltrasonicSensob, ReflectanceSensob
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton


def main():

    motob = Motob()
    bbcon = Bbcon(motob)
    arbitrator = Arbitrator(bbcon)
    bbcon.set_arbitrator(arbitrator)

    #sensorer og sensob
    ult_sensor = Ultrasonic()
    ref_sensor = ReflectanceSensors()
    reflectance_sensob = ReflectanceSensob(ref_sensor)
    ultrasonic_sensob = UltrasonicSensob(ult_sensor)
    camera_sensob = CameraSensob(None)

    #behaviors
    dont_crash = DontCrash(bbcon, ultrasonic_sensob)
    follow_line = FollowLine(bbcon, reflectance_sensob)
    find_object = FindColoredObject(bbcon, camera_sensob)

    bbcon.add_behavior(dont_crash)
    bbcon.add_behavior(follow_line)
    bbcon.add_behavior(find_object)










