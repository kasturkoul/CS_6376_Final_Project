import sys
from enum import Enum
sys.path.insert(0, './hubs')
sys.path.insert(0, './connector')

from bridge import BridgeInterface
from station import StationInterface
from fork import ForkInterface
from merge import MergeInterface
from track import TrackInterface

class HubType(Enum):
    STATION = 1
    FORK = 2
    MERGE = 3
    BRIDGE = 4

