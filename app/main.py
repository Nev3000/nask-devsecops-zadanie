from fastapi import FastAPI, HTTPException, Query
from app.data import generate_devices, devices_db
from app.models import Device, DeviceCreate
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
app = FastAPI()

generate_devices()
logger.info(f"Wygenerowana baza danych: {len(devices_db)}")
@app.get("/")
def root():
    return {"message": "Menedżer floty działa", "ilość urządzeń": len(devices_db)}

@app.get("/devices/{device_id}")
def get_device(device_id: int) -> Device:
    if device_id not in devices_db:
        logger.warning(f"{device_id} nie istnieje")
        raise HTTPException(status_code=404, detail="Nie ma takiej  maszyny")
    logger.info(f"Zapytanie o urządzenie: {device_id}")
    return devices_db[device_id]

@app.get("/devices")
def list_devices(skip: int = 0, limit: int = Query(default=50, le=200)) -> list[Device]:
    lista=list(devices_db.values())
    logger.info(f"Zapytanie o listę urządzeń: skip={skip}, limit={limit}, zwrócono={len(lista[skip:skip+limit])}")
    return lista[skip:skip+limit]


@app.post("/devices", status_code=201)
def create_device(device_create: DeviceCreate) -> Device:
    new_id = max(devices_db.keys()) + 1
    device_data = device_create.model_dump()
    new_device = Device(id=new_id, **device_data)
    devices_db[new_id] = new_device
    logger.info(f"Utworzono nowe urządzenie: id={new_id}, name={new_device.name}")
    return new_device

@app.put("/devices/{device_id}")
def update_device(device_id: int, device_create: DeviceCreate) -> Device:
    if device_id not in devices_db:
        logger.warning(f"{device_id} nie istnieje")
        raise HTTPException(status_code=404, detail="Device not found")
    new_id = device_id
    device_data = device_create.model_dump()
    new_device = Device(id=new_id, **device_data)
    devices_db[new_id] = new_device
    logger.info(f"Zmodyfikowano urządzenie: id={new_id}, name={new_device.name}")
    return new_device

@app.delete("/devices/{device_id}")
def delete_device(device_id: int) -> Device:
    if device_id not in devices_db:
        logger.warning(f"{device_id} nie istnieje")
        raise HTTPException(status_code=404, detail="Device not found")
    del_device = devices_db.pop(device_id)
    logger.info(f"Usunieto urządzenie: {device_id}")
    return del_device