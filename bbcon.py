class Bbcon():

    #For nå - kun tomme metoder

    def __init__(self):
        self.behaviors = []         # liste med behavior-objekter eks. [avoid collision, follow other robot, etc...]
        self.active_behaviors = []  # liste med aktive behavior-objekter
        self.sensobs = []           # liste med sensorobjekter
        self.motobs = []            # liste med motorobjekter
        self.arbitrator = None      # peker til arbitratoren?

    def add_behavior(self, behavior):
        pass

    def add_sensor(self, sensor):
        pass

    def activate_behavior(self, behavior):
        pass

    def deactivate_behavior(self, behavior):
        pass

    def run_one_timestep(self):
        pass