from enum import Enum

class MergeState(Enum):
    # Control which train merges onto the track
    GREEN = 1
    RED = 2

class ArriveEvent(Enum):
    # Which trains have arrived at the merge point 
    ARRIVE = 1
    LEAVE = 2

class Merge:
    def __init__(self):
        self.near_1 = 0
        self.near_2 = 0
        
        self.first = MergeState.RED
        self.second = MergeState.RED
    
    def step(self, out_1, out_2):
        signal_1 = self.first
        signal_2 = self.second

        if out_2 == ArriveEvent.ARRIVE: # If second train arrives at merge point
            self.near_2 = 1
        if out_2 == ArriveEvent.LEAVE: # If second train is going on to the merge point
            self.near_2 = 0
        if out_1 == ArriveEvent.ARRIVE: # if first train is arriving at merge point
            self.near_1 = 1
        if out_1 == ArriveEvent.LEAVE: # If first train is going on to the merge point
            self.near_1 = 0
        
        if not self.near_2: # If train is not at the merge point
            self.second = MergeState.RED # Second train track signal is RED 
        elif self.first == MergeState.RED: # If first train track signal is RED
            self.second = MergeState.GREEN # Second train track signal is GREEN
        
        if not self.near_1: # If train is not at the merge point
            self.first = MergeState.RED # First train track signal is RED 
        elif self.second == MergeState.RED: # If second train track signal is RED 
            self.first = MergeState.GREEN # First train track signal is GREEN

        # Exception handling - both signals should not be green 
        if signal_1 == MergeState.GREEN and signal_2 == MergeState.GREEN:
            raise Exception("Merge: Safety violation")

        return signal_1, signal_2

# Test
def test():
    bridge = Merge()
    print(bridge.step(ArriveEvent.ARRIVE, ArriveEvent.ARRIVE))
    print(bridge.step(None, ArriveEvent.LEAVE))
    print(bridge.step(ArriveEvent.LEAVE, None))
    print(bridge.step(None, None))
    print()
    print(bridge.step(ArriveEvent.ARRIVE, ArriveEvent.ARRIVE))
    print(bridge.step(None, ArriveEvent.LEAVE))
    print(bridge.step(None, ArriveEvent.ARRIVE))
    print(bridge.step(ArriveEvent.LEAVE, None))
    print(bridge.step(None, None))
    print(bridge.step(None, ArriveEvent.LEAVE))
    print(bridge.step(None, None))

test()