from faker import Faker
from app.models import Device, DeviceStatus
import random
from collections import Counter

fake = Faker("pl_PL")
devices_db: dict[int, Device] = {}

def generate_devices(count: int = 2000) -> None:
    for device_id in range(1, count+1):
        temp = fake.city()
        sn = temp[:3]
        device = Device(
            id = device_id,
            name =f"SN {sn} {device_id:04d}",
            location = temp,
            status = random.choice(list(DeviceStatus)),
            ip_address = fake.ipv4(),
            player_version = f"SNPlayer {fake.numerify('#.#.#')}",
            last_seen = str(fake.date_between(start_date="-90d", end_date="today")),
        )
        devices_db[device_id] = device



if __name__ == "__main__":
    generate_devices()
    statuses = [d.status for d in devices_db.values()]
    print(Counter(statuses))
    print(f"wygnenerowano {len(devices_db)} urządzeń")
    print(list(devices_db.values())[:10])