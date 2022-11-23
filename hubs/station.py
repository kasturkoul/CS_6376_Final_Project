from enum import Enum

'''
- one way in and out 
- train stops for certain period of time 
- alert other trains to stop outside station in a queue
'''
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
    def __init__(self):
        self.timer = 0
        self.occupied = False
        self.near = False

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

        if self.occupied and self.timer < 10:
            innersignal = StationState.BOARD # Train waits at the station
        elif self.timer >= 10: # If timer hits 10 counts 
            innersignal = StationState.EXIT # Train exits the station 
        
        return outersignal, innersignal

def testwait(station):
    state = station.step(None)
    while state[1] != StationState.EXIT:
        state = station.step(None)
        print(state)

def test():
    station = Station()
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

test()