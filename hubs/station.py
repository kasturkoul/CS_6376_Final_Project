from enum import Enum

class StationState(Enum):
    # Station signal is Green, Red, or the train has Exited 
    GREEN = 1 # Outter signal -- train can enter station 
    RED = 2 # Outter signal -- train cannot enter station 
    EXIT = 3 # Inner signal --  Tell the train to leave 
    BOARD = 4 # Inner signal -- Passengers are boarding - train is at the station (wait for timer)
    WAIT = 5 # Inner signal -- No train at station - passengers are waiting for train 

class ArriveEvent(Enum):
    # State of train arriving or leaving (or entering the station)
    ARRIVE = 1
    LEAVE = 2
    ENTER = 3

class Station:
    def __init__(self, delay):
        self.timer = 0
        self.occupied = False
        self.near = False
        self.delay = delay

    def step(self, out):
        if self.occupied and out == ArriveEvent.ENTER:
            raise Exception("Station: Safety violation")

        self.timer += 1 # Increase the timer by 1 in each step
        outersignal = StationState.RED # Set the signal to RED by default
        innersignal = StationState.WAIT # Tell passengers to wait for train

        if out == ArriveEvent.ARRIVE and not self.occupied: # If a train leaves and the station is not occuied 
            outersignal = StationState.GREEN # signal is GREEN
        elif out == ArriveEvent.ARRIVE and self.occupied: # If a train leaves and the station is occupied
            outersignal = StationState.RED # signal is RED
            self.near = True # Set near to True
        
        if out == ArriveEvent.LEAVE: # If the train leaves the station
            self.timer = 0 # Reset timer 
            self.occupied = False # The station is not occupied 
            if self.near:
                outersignal = StationState.GREEN # If there is a train near the station, signal is GREEN
                self.near = False
            else:
                outersignal = StationState.RED # Signal is red
        
        if out == ArriveEvent.ENTER: # If a train enters the station 
            self.occupied = True # The station is occupied 
            self.timer = 0 # set a timer 
            outersignal = StationState.RED # Tell other trains to stop -- signal is GREEN 

        if self.occupied and self.timer < self.delay:
            innersignal = StationState.BOARD # Train waits at the station
        elif self.timer >= self.delay and self.occupied: # If timer hits 10 counts 
            innersignal = StationState.EXIT # Train exits the station 
        
        return outersignal, innersignal

class StationInterface:
    def __init__(self, waittime):
        self.station = Station(waittime)
        self.ports = [None, None]
        self.action_taken = (None, None)
        self.internal = None
        self.occupied = False
        
    def is_waiting(self, port):
        self.ports[port] = ArriveEvent.ARRIVE # If a train arrives at the station, it waits 
    
    def step(self):
        # Port[0] = entry    port[1] = exit
        action = self.internal if self.internal else self.ports[0]
        self.internal = None
        self.action_taken = self.station.step(action) # Action taken
        if self.action_taken[0] == StationState.GREEN: # If the station signal is green 
            self.internal = ArriveEvent.ENTER # the train enters the station
            self.ports[0] = None # Train has entered, noting in port[0] now 
        if self.action_taken[1] == StationState.EXIT: # If a train exits the station
            self.internal = ArriveEvent.LEAVE # The state at the station is that a train left
        if self.occupied and self.station.occupied == False: # If the station is occupied
            self.ports[1] = ArriveEvent.LEAVE # Tell the train to leave 
        else:
            self.ports[1] = None # If the station is not otherwise occupied, then nothing is leaving the station 
        self.occupied = self.station.occupied

    def is_consumed(self, port):
        if port == 0: # The station becomes occupied 
            return self.internal == ArriveEvent.ENTER # Train enters station 
        else:
            return False
    
    def is_produced(self, port):
        if port == 1: # Station is emptied 
            return self.ports[port] == ArriveEvent.LEAVE # Train leaves the station
        else:
            return False

'''
def testwait(station):
    state = station.step(None)
    while state[1] != StationState.EXIT:
        state = station.step(None)
        print(state)
'''

def testwait(stationInterface):
    while not stationInterface.is_produced(1):
        #for i in range(0, 5):
        stationInterface.step()
        print("Port 0: Consumed ({}), Produced ({})".format(stationInterface.is_consumed(0), stationInterface.is_produced(0)))
        print("Port 1: Consumed ({}), Produced ({})".format(stationInterface.is_consumed(1), stationInterface.is_produced(1)))
        print()

def test():
    interface = StationInterface(2)

    interface.is_waiting(0)
    testwait(interface)
    
    print();print()

    interface.is_waiting(0)
    interface.step()
    print("Port 0: Consumed ({}), Produced ({})".format(interface.is_consumed(0), interface.is_produced(0)))
    print("Port 1: Consumed ({}), Produced ({})".format(interface.is_consumed(1), interface.is_produced(1)))
    print()
    interface.is_waiting(0)
    testwait(interface)
    interface.step()
    testwait(interface)
    
    '''
    station = Station(5)
    print(station.step(None))
    print(station.step(ArriveEvent.ARRIVE))
    print(station.step(ArriveEvent.ENTER))
    testwait(station)
    print(station.step(ArriveEvent.LEAVE))
    print(station.step(None))
    print()

    print(station.step(ArriveEvent.ARRIVE))
    print(station.step(ArriveEvent.ENTER))
    print(station.step(ArriveEvent.ARRIVE))
    testwait(station)
    print(station.step(ArriveEvent.LEAVE))
    print(station.step(ArriveEvent.ENTER))
    testwait(station)
    print(station.step(ArriveEvent.ARRIVE))
    print(station.step(ArriveEvent.LEAVE))
    print(station.step(ArriveEvent.ENTER))
    testwait(station)
    print(station.step(ArriveEvent.LEAVE))
    print(station.step(None))
    '''

test()