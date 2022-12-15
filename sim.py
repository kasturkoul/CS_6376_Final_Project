from enum import Enum
from hubs.bridge import BridgeInterface
from hubs.station import StationInterface
from hubs.fork import ForkInterface
from hubs.merge import MergeInterface
from connector.track import TrackInterface


class HubType(Enum):
    STATION = 1
    FORK = 2
    MERGE = 3
    BRIDGE = 4


class ConnectorData:
    def __init__(self, hubid, hubport):
        self.hubid = hubid
        self.hubport = hubport


class Sim:
    def __init__(self):
        self.hubs = {}
        self.tracks = {}
        self.track_type = TrackInterface
        self.hub_types = {
            HubType.STATION: StationInterface,
            HubType.FORK: ForkInterface,
            HubType.MERGE: MergeInterface,
            HubType.BRIDGE: BridgeInterface
        }
        self.id = 0

    def add_hub(self, hub_type, param=None):
        if param:
            hub = self.hub_types[hub_type](param)
        else:
            hub = self.hub_types[hub_type]()
        self.hubs[self.id] = hub
        self.id += 1

        return self.id - 1

    def add_track(self, start_hub, start_port, end_hub, end_port):
        track = self.track_type()
        startData = ConnectorData(start_hub, start_port)
        endData = ConnectorData(end_hub, end_port)
        self.tracks[self.id] = (track, startData, endData)
        self.id += 1

        return self.id - 1

    def step(self):
        for hub in self.hubs.values():
            hub.step()

        for track, startData, endData in self.tracks.values():
            if track.train_count() > 0 and not self.hubs[endData.hubid].is_awaiting(endData.hubport):
                self.hubs[endData.hubid].is_waiting(endData.hubport)
                track.is_leaving()
                print("Train arrived at hub", endData.hubid,
                      "port", endData.hubport)
            if self.hubs[startData.hubid].is_produced(startData.hubport):
                track.is_waiting()
                print("Train arrived at track")

        print("Step done")

    def add_train(self, id, port=0):
        if id in self.hubs:
            self.hubs[id].is_waiting(port)
        else:
            self.tracks[id][0].is_waiting()


"""
sim = Sim()
station_id = sim.add_hub(HubType.STATION, 1)
track_id = sim.add_track(station_id, 1, station_id, 0)

sim.add_train(track_id)

for i in range(20):
    sim.step()
"""

sim = Sim()
station_id = sim.add_hub(HubType.STATION, 2)
fork_id = sim.add_hub(HubType.FORK)
track_0 = sim.add_track(station_id, 1, fork_id, 0)

bridge_id = sim.add_hub(HubType.BRIDGE)
sim.add_track(fork_id, 1, bridge_id, 0)
track_1 = sim.add_track(fork_id, 2, bridge_id, 1)

merge_id = sim.add_hub(HubType.MERGE)
track_2 = sim.add_track(bridge_id, 0, merge_id, 0)
track_3 = sim.add_track(bridge_id, 1, merge_id, 1)
track_4 = sim.add_track(merge_id, 2, station_id, 0)

print("Tracks:", track_0, track_1, track_2, track_3, track_4)
print("Hubs:", station_id, fork_id, bridge_id, merge_id)

sim.add_train(track_4)
sim.add_train(track_4)
sim.add_train(track_4)
sim.add_train(track_4)
sim.add_train(track_4)

for i in range(5000):
    sim.step()
