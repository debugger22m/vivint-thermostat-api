import json
import random
import pprint

from fastapi import APIRouter
from ..data import generate_thermostat_data
from fastapi import FastAPI, Header
from typing import Optional

router = APIRouter()

#Generate fake data
thermostat_data_set = generate_thermostat_data.GenerateData.init(100)

#Mappings
thermostat_state = {0: "actively cooling", 1: "actively heating"}
thermostat_fan_mode = {0 : "off", 1 : "on", 2 : "auto"}

#GET APIs
@router.get("/get/all", tags=["Get all Devices"])
async def get_all_devices():
    return thermostat_data_set

@router.get("/get/config/", tags=["Get config for given device"])
async def get_config(user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    print(user_id)
    return  thermostat_data_set[user_id][vivint_unit_id]

@router.get("/temperature/current/", tags=["GET Current Temperature"], status_code=200)
async def get_current_temperature(user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    target_temp = thermostat_data_set[user_id][vivint_unit_id]['current_temp']
    return target_temp


@router.get("/temperature/target", tags=["GET Target Temperature"], status_code=200)
async def get_target_temperature(user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    target_temp = thermostat_data_set[user_id][vivint_unit_id]['target_temp']
    return target_temp


@router.get("/state/", tags=["GET Current State"], status_code=200)
async def get_current_state(user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    current_state = thermostat_data_set[user_id][vivint_unit_id]['state']
    return current_state


@router.get("/fan/", tags=["GET Fan Mode"], status_code=200)
async def get_fan_mode(user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    fan_mode = thermostat_data_set[user_id][vivint_unit_id]['fan']
    return fan_mode


#PUT APIs
@router.put("/temperature/current/{temperature}", tags=["Update Current Temperature"], status_code=204)
async def set_current_temperature(temperature: int, user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    thermostat_data_set[user_id][vivint_unit_id]['current_temp']  = temperature
    return {"Current temperature was successfully updated to ":  thermostat_data_set[user_id][vivint_unit_id]['current_temp']}


@router.put("/temperature/target/{temperature}", tags=["Update Target Temperature"], status_code=204)
async def set_target_temperature(temperature: int, user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    thermostat_data_set[user_id][vivint_unit_id]['target_temp']  = temperature
    return {"Current temperature was successfully updated to ":  thermostat_data_set[user_id][vivint_unit_id]['target_temp']}


@router.put("/state/{state}", tags=["Update Current State"], status_code=200)
async def set_current_state(state: int, user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    thermostat_data_set[user_id][vivint_unit_id]['state'] = thermostat_state[state] 
    return {"Current state was successfully updated to ": thermostat_data_set[user_id][vivint_unit_id]['state'] }


@router.put("/fan/{mode}", tags=["Update FAN Mode"], status_code=200)
async def set_fan_mode(mode: int, user_id: Optional[str] = Header(None), vivint_unit_id: Optional[str] = Header(None)):
    thermostat_data_set[user_id][vivint_unit_id]['fan'] = thermostat_fan_mode[mode] 
    return {"Current state was successfully updated to ": thermostat_data_set[user_id][vivint_unit_id]['fan'] }


