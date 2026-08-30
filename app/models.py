from enum import Enum

from pydantic import BaseModel


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class Device(BaseModel):
    id: int
    name: str
    location: str
    status: DeviceStatus
    ip_address: str
    player_version: str
    last_seen: str

class DeviceCreate(BaseModel):
    name: str
    location: str
    status: DeviceStatus
    ip_address: str
    player_version: str
    last_seen: str