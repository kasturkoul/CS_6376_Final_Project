from enum import Enum

class ArriveEvent(Enum):
    # State of train arriving or leaving
    ARRIVE = 1
    LEAVE = 2

class TrackInterface:
    def __init__(self):
        self.trains = 0 # Bool, if train is on track 

    def is_waiting(self):
        self.trains += 1 # Put train on track
        
    def is_leaving(self):
        if self.trains > 0:
            self.trains -= 1
        else:
            raise Exception("Track: Safety violation")

    def step(self):
        pass

    def train_count(self):
        return self.trains

def test_track():
    track = TrackInterface()
    track.is_waiting()
    track.step()
    print(track.is_occupied())
    track.step()
    print(track.is_occupied())
    track.is_leaving()
    track.step()
    print(track.is_occupied())
    track.is_waiting()
    track.step()
    print(track.is_occupied())
    track.is_waiting()
    track.step()
    print(track.is_occupied())

#test_track()