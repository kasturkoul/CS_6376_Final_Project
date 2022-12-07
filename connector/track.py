from enum import Enum

class ArriveEvent(Enum):
    # State of train arriving or leaving
    ARRIVE = 1
    LEAVE = 2

class TrackInterface:
    def __init__(self):
        self.occupied = False # Bool, if train is on track 

    def is_waiting(self):
        if self.occupied: # Throws exception if two trains are on the track
            raise Exception("Track: Safety violation")

        self.occupied = True # Put train on track
        
    def is_leaving(self):
        self.occupied = False # Take train off track

    def step(self):
        pass

    def is_occupied(self):
        return self.occupied # Bool for if train is on track

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

test_track()