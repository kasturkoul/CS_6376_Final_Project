from track import TrackInterface
from merge import MergeInterface
from fork import ForkInterface
from station import StationInterface
from bridge import BridgeInterface
import sys
from enum import Enum
sys.path.insert(0, './hubs')
sys.path.insert(0, './connector')


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

    def add_hub(self, hub_type):
        hub = self.hub_types[hub_type]()
        self.hubs[self.id](hub)
        self.id += 1

        return hub, self.id - 1

    def add_track(self, start_hub, start_port, end_hub, end_port):
        track = self.track_type()
        startData = ConnectorData(start_hub, start_port)
        endData = ConnectorData(end_hub, end_port)
        self.tracks[self.id] = (track, startData, endData)
        self.id += 1

        return track, self.id - 1
