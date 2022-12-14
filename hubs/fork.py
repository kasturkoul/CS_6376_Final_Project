from enum import Enum
import random as r


class Direction(Enum):
    OUT_1 = 1
    OUT_2 = 2


class Fork:
    def __init__(self):
        self.current_direction = Direction.OUT_1

    def toggle_direction(self):
        # Change the train's direction
        if self.current_direction == Direction.OUT_1:
            self.current_direction = Direction.OUT_2
        else:
            self.current_direction = Direction.OUT_1

    def step(self, direction):
        old_direction = self.current_direction  # Keep track of the old direction
        if direction != None and direction != self.current_direction:
            # If the direction is not none (error check) and the new direction is not the current direction of the train
            self.toggle_direction()  # Change direction
        # return old direction (part of the one step penalty) -- this is the current direction
        return old_direction


class ForkInterface:
    def __init__(self):
        self.fork = Fork()
        self.ports = [None, None, None]
        self.action_taken = None
        self.entering = False
        self.waiting = False
        self.exiting = False

    def is_waiting(self, port):
        self.ports[port] = r.choice([Direction.OUT_1, Direction.OUT_2])
        print("Random direction: {}".format(self.ports[port]))
        self.entering = True

    def step(self):
        self.action_taken = self.fork.step(self.ports[0])
        self.ports[0] = None
        self.exiting = self.waiting
        self.waiting = self.entering
        self.entering = False

    def is_consumed(self, port):
        return port == 0 and self.exiting

    def is_produced(self, port):
        if port == 1:
            return self.exiting and self.action_taken == Direction.OUT_1
        elif port == 2:
            return self.exiting and self.action_taken == Direction.OUT_2
        else:
            return False

    def is_awaiting(self, port):
        return False


def test():
    forkInterface = ForkInterface()
    for i in range(0, 6):
        if not (i % 2):
            forkInterface.is_waiting(0)
        forkInterface.step()
        print("Port 0: Consumed ({}), Produced ({})".format(
            forkInterface.is_consumed(0), forkInterface.is_produced(0)))
        print("Port 1: Consumed ({}), Produced ({})".format(
            forkInterface.is_consumed(1), forkInterface.is_produced(1)))
        print("Port 2: Consumed ({}), Produced ({})".format(
            forkInterface.is_consumed(2), forkInterface.is_produced(2)))
        print()

    """
    fork = Fork()
    print(fork.step(Direction.OUT_1))
    print(fork.step(Direction.OUT_2))
    print(fork.step(Direction.OUT_2))
    print(fork.step(None))
    print(fork.step(Direction.OUT_1))
    print(fork.step(Direction.OUT_1))
    print(fork.step(Direction.OUT_1))
    print(fork.step(None))
    print(fork.step(Direction.OUT_2))
    print(fork.step(Direction.OUT_1))
    print(fork.step(None))
    print(fork.step(None))
    """

# test()
