from enum import Enum

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
        old_direction = self.current_direction # Keep track of the old direction
        if direction != None and direction != self.current_direction: 
            # If the direction is not none (error check) and the new direction is not the current direction of the train
            self.toggle_direction() # Change direction
        return old_direction # return old direction (part of the one step penalty) -- this is the current direction

def test():
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

test()