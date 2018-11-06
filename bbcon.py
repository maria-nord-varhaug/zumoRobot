from behavior import Behavior, DontCrash, FindColoredObject
from arbitrator import Arbitrator
from motob import Motob


class Bbcon():
    def __init__(self, motob):
        self.behaviors = []         # liste med behavior-objekter eks. [avoid collision, follow other robot, etc...]
        self.active_behaviors = []  # liste med aktive behavior-objekter
        assert isinstance(motob, Motob)
        self.arbitrator = None
        self.motob = motob
        self.camera_on = False
        self.follow_line = True
        self.object_found = False

    def set_arbitrator(self, arbitrator):
        assert isinstance(arbitrator, Arbitrator)
        self.arbitrator = arbitrator

    def add_behavior(self, behavior):  # add behavior to self.behaviors
        assert isinstance(behavior, Behavior)
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def activate_behavior(self, behavior):  # add behavior to self.active_behviors
        assert isinstance(behavior, Behavior)
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):  # remove behavior from self.active_behaviorr
        assert isinstance(behavior, Behavior)
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def should_camera_be_on(self):
        return self.camera_on

    def should_follow_line(self):
        return self.follow_line

    def run_one_timestep(self):  # main
        for behavior in self.behaviors:  # add behaviors that should be active to active behaviours
            behavior.consider_activation()
            if behavior.active_flag:
                self.activate_behavior(behavior)
        for behavior in self.active_behaviors:  # deactivate behaviors that should be deactiveted
            behavior.consider_deactivation()
            if not behavior.active_flag:
                self.deactivate_behavior(behavior)
        for behavior in self.active_behaviors: # updates active behaviors and their sensobs
            behavior.update()
        action_tuple = self.arbitrator.choose_action() # (motor_rec, winning_behavior.halt_request, winning_behavior)
        self.motob.update(action_tuple[:2])
        if isinstance(action_tuple[2], DontCrash):
            self.camera_on = True
            self.follow_line = False
        else:
            self.camera_on = False
            self.follow_line = True
        if isinstance(action_tuple[2], FindColoredObject) and action_tuple[0][1] == 0:
            self.object_found = True
        for behavior in self.behaviors:
            behavior.reset()
