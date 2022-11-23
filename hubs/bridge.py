from enum import Enum

class BridgeState(Enum):
    # State at the gates to the bridge
    GREEN = 1
    RED = 2

class ArriveEvent(Enum):
    # State of train arriving or leaving
    ARRIVE = 1
    LEAVE = 2

class Bridge:
    def __init__(self):
        self.near_W = 0
        self.near_E = 0
        
        self.west = BridgeState.RED
        self.east = BridgeState.RED
    
    def step(self, out_W, out_E):
        signal_W = self.west
        signal_E = self.east

        if out_E == ArriveEvent.ARRIVE: # If train arrives at E gate
            self.near_E = 1
        if out_E == ArriveEvent.LEAVE: # If train is leaving from E Gate
            self.near_E = 0
        if out_W == ArriveEvent.ARRIVE: # if train is arriving at W gate
            self.near_W = 1
        if out_W == ArriveEvent.LEAVE: # If train is leaving W gate
            self.near_W = 0
        
        if not self.near_E: # If train is not near E gate 
            self.east = BridgeState.RED # E signal is RED 
        elif self.west == BridgeState.RED: # If W gate signal is RED 
            self.east = BridgeState.GREEN # E gate signal is GREEN 
        
        if not self.near_W: # If train is not near W gate 
            self.west = BridgeState.RED # W gate signal is RED 
        elif self.east == BridgeState.RED: # If E gate signal is RED 
            self.west = BridgeState.GREEN # W gate signal is GREEN 

        # Exception handling - both signals should not be green
        if signal_W == BridgeState.GREEN and signal_E == BridgeState.GREEN:
            raise Exception("Bridge: Safety violation")

        return signal_W, signal_E

# Test
def test():
    bridge = Bridge()
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