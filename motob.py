from motors import Motors
from arbitrator import Arbitrator


class Motob():
    # gjør om ('L',30) til motorinstruksjoner
    # instruksjoner for venstr og høyre hjul? range[-1,1]

    def __init__(self):
        self.motor = Motors()           # Lager et Motorobjekt?
        self.value = ()                 # Nyligste motor_recommendation sendt hit, ('L',30)
        self.default_motorverdi = 0.5

    def update(self, tuppel_motorrec_halt_request):
        if tuppel_motorrec_halt_request[1]:    # hvis halt request er true
            self.motor.stop()  # stopper?
            return
        self.value = tuppel_motorrec_halt_request[0] #setter self.value til motor recommendation
        self.operationalize() # utfører motor recommendation

    def grader_til_duration(self,grader):
        return -0.0000786445*grader*grader + 0.0155473*grader - 0.0212085  # ish ok

    def operationalize(self):  # set__value([l,r],duration)
        instruks = self.value[0]
        grader = self.value[1]
        if instruks == 'L':
            self.motor.set_value([-self.default_motorverdi, self.default_motorverdi], self.grader_til_duration(grader))
        elif instruks == 'R':
            self.motor.set_value([self.default_motorverdi, -self.default_motorverdi], self.grader_til_duration(grader))
        else: # eneste andre kommando er forwards, og den vil bare... ja kjøre
            self.motor.set_value([self.default_motorverdi, self.default_motorverdi]) # dur = None gir at den først
                                                                                    # kjører litt frem, og så fortsetter

