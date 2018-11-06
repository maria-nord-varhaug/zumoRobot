from abc import abstractmethod
import Ultrasonic
import Reflectance_sensors


class Behavior(): #abstract class

    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.motor_recommendations = ('F', 0)  #En motob. EKSEMPEL:(L, 30), en tuple som inneholder en character som enten er 'L', 'R', 'evtuenlt en til?' og andre verdi er antall grader et int tall.
        self.active_flag = False
        self.halt_request = False #avslutte oppførelse totalt
        self.match_degree = 0      #hvor viktig oppførselen er akkurat nå, regnes ut fra sensor info og regnes ut i Behavior.
        self.weight = 0    #self.priority * self.match_degree #sendes til Arbitrator, som indikere hvor viktig det
        # er å utføre denne oppførselen n ..

    @abstractmethod
    def consider_deactivation(self):
        pass

    @abstractmethod
    def consider_activation(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def sense_and_act(self): #skal legge inn motor recemendations, regne ut match_degree og sende halt_request
        pass


class DontCrash(Behavior):

    def __init__(self, bbcon, ultrasonicsensob):
        super(DontCrash, self).__init__(bbcon)
        self.sensob = ultrasonicsensob
        self.active_flag = True
        self.dist = None
        self.priority = 1

    def update(self):
        self.dist = self.sensob.update()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def consider_deactivation(self):
        pass

    def consider_activation(self):
        pass

    def sense_and_act(self):
        if self.active_flag == True:
            if self.dist > 20:
                self.match_degree = 0
                self.motor_recommendations = ('F',)
            elif self.dist <= 5:
                self.match_degree = 1
                self.motor_recommendations = ('R', 180)
            else:
                self.match_degree = 1-((self.dist-5)/20)
                self.motor_recommendations = ('R', 180)


class FollowLine(Behavior):

    def __init__(self, bbcon, reflectancesensob):
        super(FollowLine, self).__init__(bbcon)
        self.sensob = reflectancesensob
        self.active_flag = True
        self.reflectvalues = None
        self.weight = 0.5

    def update(self):
        self.reflectvalues = self.sensob.update()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self, threshold = 0.05):
        if self.active_flag == True:
            degrees = {0:20, 1:7, 2:0, 3:0, 4:7, 5:20}
            maxval = 0  # maximum value
            index = 0  # index of maxval
            for i in range(len(self.reflectvalues)):  # find maxval and index of maxval in array
                self.reflectvalues[i] = 1 - reflekt[i]
                if self.reflectvalues[i] > maxval:
                    maxval = self.reflectvalues[i]
                    index = i
            if maxval < threshold:
                self.motor_recommendations = ('L, 45')
                self.match_degree = 0
            else:
                direction = 'R' if index > 3 else 'L'
                self.motor_recommendations = (direction, degrees[index])
                self.match_degree = 1

    def consider_activation(self):
        self.bbcon.turn_on_reflectance()
        self.bbcon.turn_off_camera()
        self.active_flag = True

    def consider_deactivation(self):
        self.bbcon.turn_off_reflectance()
        self.bbcon.turn_on_camera()
        self.active_flag = False


class FindColoredObject(Behavior):
    
    def __init__(self, bbcon, camerasensob):
        super(FindColoredObject, self).__init__(bbcon)
        self.sensob = camerasensob
        self.active_flag = False
        self.array = None
        self.weight = 0.8

    def update(self):
        self.array = self.sensob.update()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self, threshold = 0.05):
        maxval = 0  # maximum value
        index = 0  # index of maxval
        for i in range(len(self.array)):  # find maxval and index of maxval in array
            if self.array[i] > maxval:
                maxval = self.array[i]
                index = i
        if maxval < threshold:
            self.motor_recommendations = ('L, 60')
            self.match_degree = 0
        else:
            direction = 'R' if index > 3 else 'L'
            degree = {0: 32, 1: 16, 2: 8, 3: 0, 4: 0, 5: 8, 6: 16, 7: 32}
            self.motor_recommendations = (direction, degree[index])
            self.match_degree = 1

    def consider_deactivation(self):
        self.bbcon.turn_off_camera()
        self.bbcon.turn_on_reflectance()
        self.active_flag = True

    def consider_activation(self):
        self.bbcon.turn_on_camera()
        self.bbcon.turn_off_reflectance()
        self.active_flag = False
