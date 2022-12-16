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

        if out_E == ArriveEvent.ARRIVE:  # If train arrives at E gate
            self.near_E = 1
        if out_E == ArriveEvent.LEAVE:  # If train is leaving from E Gate
            self.near_E = 0
        if out_W == ArriveEvent.ARRIVE:  # if train is arriving at W gate
            self.near_W = 1
        if out_W == ArriveEvent.LEAVE:  # If train is leaving W gate
            self.near_W = 0

        if not self.near_E:  # If train is not near E gate
            self.east = BridgeState.RED  # E signal is RED
        elif self.west == BridgeState.RED:  # If W gate signal is RED
            self.east = BridgeState.GREEN  # E gate signal is GREEN

        if not self.near_W:  # If train is not near W gate
            self.west = BridgeState.RED  # W gate signal is RED
        elif self.east == BridgeState.RED:  # If E gate signal is RED
            self.west = BridgeState.GREEN  # W gate signal is GREEN

        # Exception handling - both signals should not be green
        if signal_W == BridgeState.GREEN and signal_E == BridgeState.GREEN:
            raise Exception("Bridge: Safety violation")

        return signal_W, signal_E


class BridgeInterface:
    def __init__(self):
        self.bridge = Bridge()
        self.ports = [None, None]
        self.action_taken = (None, None)

    def is_waiting(self, port):
        self.ports[port] = ArriveEvent.ARRIVE

    def step(self):
        out_W, out_E = self.ports
        self.action_taken = self.bridge.step(out_W, out_E)
        self.ports = [ArriveEvent.LEAVE if self.action_taken[0] == BridgeState.GREEN and self.ports[0] != ArriveEvent.LEAVE else None,
                      ArriveEvent.LEAVE if self.action_taken[1] == BridgeState.GREEN and self.ports[1] != ArriveEvent.LEAVE else None]

    def is_consumed(self, port):
        return self.ports[port] == ArriveEvent.LEAVE

    def is_produced(self, port):
        if port < 2:
            return self.ports[1 - port] == ArriveEvent.LEAVE
        else:
            return False

    def is_awaiting(self, port):
        if port == 0:
            return self.ports[port] == ArriveEvent.ARRIVE or self.bridge.near_W == 1
        elif port == 1:
            return self.ports[port] == ArriveEvent.ARRIVE or self.bridge.near_E == 1
        else:
            return False


# Test
def test():
    bridgeInterface = BridgeInterface()
    bridgeInterface.is_waiting(0)
    bridgeInterface.is_waiting(1)
    for i in range(0, 5):
        bridgeInterface.step()
        print("Port 0: Consumed ({}), Produced ({})".format(
            bridgeInterface.is_consumed(0), bridgeInterface.is_produced(0)))
        print("Port 1: Consumed ({}), Produced ({})".format(
            bridgeInterface.is_consumed(1), bridgeInterface.is_produced(1)))
        print("Port 0 is waiting: {}, Port 1 is waiting: {}".format(
            bridgeInterface.is_awaiting(0), bridgeInterface.is_awaiting(1)))
        print()

    """
    bridge = Bridge()
    print(bridge.step(ArriveEvent.ARRIVE, ArriveEvent.ARRIVE))
    print(bridge.step(None, None))
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
    """


# test()
