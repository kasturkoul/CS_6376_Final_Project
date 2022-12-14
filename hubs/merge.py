from enum import Enum
import random as r


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

        if out_2 == ArriveEvent.ARRIVE:  # If second train arrives at merge point
            self.near_2 = 1
        if out_2 == ArriveEvent.LEAVE:  # If second train is going on to the merge point
            self.near_2 = 0
        if out_1 == ArriveEvent.ARRIVE:  # if first train is arriving at merge point
            self.near_1 = 1
        if out_1 == ArriveEvent.LEAVE:  # If first train is going on to the merge point
            self.near_1 = 0

        def handle_second():
            if not self.near_2:  # If train is not at the merge point
                self.second = MergeState.RED  # Second train track signal is RED
            elif self.first == MergeState.RED:  # If first train track signal is RED
                self.second = MergeState.GREEN  # Second train track signal is GREEN

        def handle_first():
            if not self.near_1:  # If train is not at the merge point
                self.first = MergeState.RED  # First train track signal is RED
            elif self.second == MergeState.RED:  # If second train track signal is RED
                self.first = MergeState.GREEN  # First train track signal is GREEN

        if (r.random() < 0.5):
            handle_second()
            handle_first()
        else:
            handle_first()
            handle_second()

        # Exception handling - both signals should not be green
        if signal_1 == MergeState.GREEN and signal_2 == MergeState.GREEN:
            raise Exception("Merge: Safety violation")

        return signal_1, signal_2


class MergeInterface:
    def __init__(self):
        self.bridge = Merge()
        self.ports = [None, None, None]
        self.action_taken = (None, None)

    def is_waiting(self, port):
        self.ports[port] = ArriveEvent.ARRIVE

    def step(self):
        out_W, out_E, _ = self.ports
        self.action_taken = self.bridge.step(out_W, out_E)
        self.ports = [ArriveEvent.LEAVE if self.action_taken[0] == MergeState.GREEN and self.ports[0] != ArriveEvent.LEAVE else None,
                      ArriveEvent.LEAVE if self.action_taken[
                          1] == MergeState.GREEN and self.ports[1] != ArriveEvent.LEAVE else None,
                      None]

    def is_consumed(self, port):
        return self.ports[port] == ArriveEvent.LEAVE

    def is_produced(self, port):
        if port == 2:
            return self.ports[0] == ArriveEvent.LEAVE or self.ports[1] == ArriveEvent.LEAVE
        else:
            return False

    def is_awaiting(self, port):
        if port == 0:
            return self.ports[port] == ArriveEvent.ARRIVE or self.bridge.near_1 == 1
        elif port == 1:
            return self.ports[port] == ArriveEvent.ARRIVE or self.bridge.near_2 == 1
        else:
            return False

# Test


def test():
    mergeInterface = MergeInterface()
    mergeInterface.is_waiting(0)
    mergeInterface.is_waiting(1)
    for i in range(0, 5):
        mergeInterface.step()
        print("Port 0: Consumed ({}), Produced ({})".format(
            mergeInterface.is_consumed(0), mergeInterface.is_produced(0)))
        print("Port 1: Consumed ({}), Produced ({})".format(
            mergeInterface.is_consumed(1), mergeInterface.is_produced(1)))
        print("Port 2: Consumed ({}), Produced ({})".format(
            mergeInterface.is_consumed(2), mergeInterface.is_produced(2)))
        print("Port 1 is awaiting: {}, Port 2 is awaiting: {}".format(
            mergeInterface.is_awaiting(0), mergeInterface.is_awaiting(1)))
        print()

    """
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
    """


# test()
