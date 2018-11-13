from arbitrator import Arbitrator
from bbcon import Bbcon
from behavior import DontCrash, FollowLine, FindColoredObject
from motob import Motob
from reflectance_sensors import ReflectanceSensors
from sensobs import CameraSensob, UltrasonicSensob, ReflectanceSensob
from ultrasonic import Ultrasonic
from zumo_button import ZumoButton
import RPi.GPIO as GPIO


def main():
    motob = Motob()
    bbcon = Bbcon(motob)
    arbitrator = Arbitrator(bbcon)
    bbcon.set_arbitrator(arbitrator)

     # sensorer og sensob
    ult_sensor = Ultrasonic()
    ref_sensor = ReflectanceSensors(auto_calibrate=False)
    reflectance_sensob = ReflectanceSensob(ref_sensor)
    ultrasonic_sensob = UltrasonicSensob(ult_sensor)
    camera_sensob = CameraSensob(None, color=2)

    #behaviors
    dont_crash = DontCrash(bbcon, ultrasonic_sensob)
    follow_line = FollowLine(bbcon, reflectance_sensob)
    find_object = FindColoredObject(bbcon, camera_sensob)

    bbcon.add_behavior(dont_crash)
    #bbcon.add_behavior(follow_line)
    #bbcon.add_behavior(find_object)
    try:
        ZumoButton().wait_for_press()
        while not bbcon.object_found:  # Kjører helt til vi finner objektet
            bbcon.run_one_timestep()
    except KeyboardInterrupt:
        motob.motor.stop()
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()








