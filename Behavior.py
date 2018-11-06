from abc import abstractmethod
import Ultrasonic
import Reflectance_sensors





class Behavior(): #abstract class

    def __init__(self, bbcon):
        self.bbcon = Bbcon()
        self.motor_recommendations = ('F', 0)  #En motob. EKSEMPEL:(L, 30), en tuple som inneholder en character som enten er 'L', 'R', 'evtuenlt en til?' og andre verdi er antall grader et int tall.
        self.active_flag = False
        self.halt_request = False #avslutte oppførelse totalt
  # self.priority defineres i hver klasse og sier hvor viktig oppførselen generelt er
        self.match_degree = 0      #hvor viktig oppførselen er akkurat nå, regnes ut fra sensor info og regnes ut i Behavior.
        self.weight = 0    #self.priority * self.match.degree #sendes til Arbitrator, som indikere hvor viktig det
        # er å utføre denne oppførselen n ..

    @abstractmethod
    def consider_deactivation(self):
        pass

    @abstractmethod
    def consider_activation(self):
        pass

    def update(self):
        self.sense_and_act()
        self.weight = self.match_degree * self.priority

    @abstractmethod
    def sense_and_act(self): #skal legge inn motor recemendations, regne ut match_degree og sende halt_request
        pass


class Dont_crash(Behavior, Ultrasonic):

    def __init__(self, bbcon):
        super(Dont_crash, self).__init__(bbcon, 2)
        self.sensob = Ultrasonic()
        self.active_flag = True

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass


    def sense_and_act(self):
        if self.active_flag == True:
            dist = self.sensob.get_value() #get_value() method from Ultrasonic class returns distance in cm
            if dist <= 5:
                self.motor_recommendations = ('R', 180) #??? snu 180 grade rundt
                self.match_degree = 1000
            else:
                self.match_degree = 0
                self.motor_recommendations = ('F', )
            return self.motor_recommendations


class Follow_Line(Behavior, Reflectance_sensors):

    def __init__(self):
        super(Follow_Line, self).__init__(bbcon, 1)
        self.sensob = Reflectance_sensors()
        self.active_flag = True

    def sense_and_act(self):
        if self.active_flag == True:
            reflekt = self.sensob.get_value()
            degrees = {0:32, 1:16, 2:0, 3:0, 4:16, 5:32}
            grader = 0
            maxval = 0  # maximum value
            index = 2  # index of maxval
            for i in reflekt:
                reflekt[i] = 1-reflekt[i]
                grader += (degrees[i]*reflekt[i])
                if i != 2 and i != 3 and reflekt[i] > maxval:
                    maxval = reflekt[i]
                    index = i
            direction = 'R' if index > 3 else 'L'

    def consider_activation(self):
         if
            self.active_flag = True
             #skru på refleks sensor

    def consider_deactivation(self):
        if
            self.active_flag = False
            #skru av refleks sensor



class Find_colored_object(Behavior, FindObject):
    
    def __init__(self):
        super(Find_colored_object, self).__init__(bbcon, 1)
        self.sensob = FindObject()
        self.active_flag = False

    def sense_and_act(self):
        return self.sensob.recomendation

    def consider_deactivation(self):

        if self.sensob.get_value
            self.active_flag = False
            #skru av kamera

    def consider_activation(self):
         if
            self.active_flag = True
            #skru på Kamera
