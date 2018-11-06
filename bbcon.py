from behavior import Behavior


class Bbcon():
    def __init__(self):
        self.behaviors = []         # liste med behavior-objekter eks. [avoid collision, follow other robot, etc...]
        self.active_behaviors = []  # liste med aktive behavior-objekter
        self.motobs = []            # liste med motorobjekter
        self.arbitrator = None      # peker til arbitratoren?

    def add_behavior(self, behavior):
        assert isinstance(behavior, Behavior)
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def activate_behavior(self, behavior):
        assert isinstance(behavior, Behavior)
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        assert isinstance(behavior, Behavior)
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        for behavior in self.behaviors:
            behavior.consider_activation()
            if behavior.active_flag:
                self.activate_behavior(behavior)
        for behavior in self.active_behaviors:
            behavior.consider_deactivation()
            if not behavior.active_flag:
                self.deactivate_behavior(behavior)


