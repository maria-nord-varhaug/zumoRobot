from motors import Motors
from arbitrator import Arbitrator


class Motob():
    # gjør om ('L',30) til motorinstruksjoner
    # instruksjoner for venstr og høyre hjul? range[-1,1]

    def __init__(self, arbitrator):
        self.motor = Motors()           # Lager et Motorobjekt?
        self.value = ()                 # Nyligste motor_recommendation sendt hit
        self.arbitrator = arbitrator    # trenger å peke på arbitrator for å oppdatere?
        self.past_command = ''
        self.default_fart = 0.125

    def update(self):
        t = self.arbitrator.find_optimal_behavior()  # f.eks  (('L',30),False)
        if t[1]:    # hvis halt request er true
            self.motor.stop()  # stopper?
            self.past_command = 'S'
            return
        self.value = t[0]

    def operationalize(self):  # si default fart er 0.125
        #if self.past_command != 'F':
            if self.value[0] == 'L':
                self.motor.set_value([-self.default_fart, self.default_fart], self.value[1] / 10)
            elif self.value[0] == 'R':
                self.motor.set_value([self.default_fart, -self.default_fart], self.value[1] / 10)
            else:
                self.motor.set_value([self.default_fart, self.default_fart], self.value[1]/10)
        #else:
        #    if self.value[0] == 'L':
        #        pass
        #    elif self.value[0] == 'R':
        #        pass
        #    else:
        #        pass
        #self.past_command = self.value[0]

    # MED HJUL SOM ROTERER BEGGE VEIER hypotese

    # 360grader på 3 sekunder med fart på 0.5 (av max)
    # 120grader på 1 sekund
    # 30 grader på 1/4 sekund

    # 0.125 fart -> 360 grader på 12 sekunder?
    # 30 grader på 3 sekunder
    # 10 grader per sekund
