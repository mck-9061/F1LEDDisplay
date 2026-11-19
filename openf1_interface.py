import time
from datetime import timedelta

import requests
import json
import datetime
import time as sleep

all_received_control = []
yellow_sectors = []
double_yellow_sectors = []
rain_risk = 0
pit_exit = True
overtake = False
safety_car = False
virtual_safety_car = False
red_flag = False
chequered_flag = False
status = ""

def handle_control_message(message):
    global rain_risk
    global overtake
    global status
    global pit_exit
    global safety_car
    global virtual_safety_car
    global red_flag
    global yellow_sectors
    global double_yellow_sectors
    global chequered_flag

    # print(json.dumps(message, indent=2))
    all_received_control.append(message)

    driver = message["driver_number"]
    category = message["category"]
    flag = message["flag"]
    scope = message["scope"]
    sector = message["sector"]
    m = message["message"]


    # Flags
    if category == "Flag":
        if flag == "GREEN":
            print("Green flag")

        if flag == "YELLOW":
            yellow_sectors.append(sector)
            if sector in double_yellow_sectors: double_yellow_sectors.remove(sector)
            print(f"Yellow flags: {", ".join([str(sector) for sector in yellow_sectors])}")

        if flag == "DOUBLE YELLOW":
            if sector in yellow_sectors: yellow_sectors.remove(sector)
            double_yellow_sectors.append(sector)
            print(f"Double yellow flags: {", ".join([str(sector) for sector in double_yellow_sectors])}")

        if flag == "CLEAR":
            if m == "TRACK CLEAR":
                yellow_sectors = []
                double_yellow_sectors = []
                print("All sectors clear")
            else:
                if sector in yellow_sectors: yellow_sectors.remove(sector)
                if sector in double_yellow_sectors: double_yellow_sectors.remove(sector)
                if len(yellow_sectors) == 0 and len(double_yellow_sectors) == 0:
                    print("All sectors clear")
                else:
                    print(f"Yellow flags: {", ".join([str(sector) for sector in yellow_sectors])}")
                    print(f"Double yellow flags: {", ".join([str(sector) for sector in double_yellow_sectors])}")

        if flag == "CHEQUERED":
            chequered_flag = True
            print("Chequered flag")


    if category == "Other" and "RED FLAG" in m:
        print("Red flag")
        red_flag = True
        safety_car = False
        virtual_safety_car = False

    # Session status
    if category == "SessionStatus":
        status = m
        print(f"Status: {status}")

        if status == "SESSION STARTED":
            red_flag = False

    # Pit exit
    if "PIT EXIT" in m:
        if "OPEN" in m:
            pit_exit = True
        else:
            pit_exit = False

        print(f"Pit exit: {str(pit_exit)}")

    # Rain
    if "RISK OF RAIN" in m:
        rain_risk = int(m.split("IS ")[1].split("%")[0])

    # Overtake
    if "OVERTAKE" in m:
        if "DISABLED" in m:
            overtake = False
        else:
            overtake = True

        print(f"Overtake: {str(overtake)}")

    # Incidents
    if "INCIDENT INVOLVING" in m:
        if "NOTED" in m:
            print(m)

        if "NO FURTHER INVESTIGATION":
            print(m)

    # Safety cars
    if category == "SafetyCar":
        if message == "SAFETY CAR DEPLOYED":
            safety_car = True
            print("Safety car deployed")

        if message == "VSC DEPLOYED":
            virtual_safety_car = True
            print("Virtual safety car deployed")

        if message == "VSC ENDING":
            virtual_safety_car = False
            print("Virtual safety car ending")


openf1_base_url = "https://api.openf1.org/v1/"

def get_race_control_previous():
    meetings = json.loads(requests.get(openf1_base_url + "meetings?year=2026&country_name=Italy", verify="/etc/ssl/certs/ca-certificates.crt").content)
    meeting_key = meetings[0]["meeting_key"]
    sessions = json.loads(requests.get(openf1_base_url + f"sessions?meeting_key={meeting_key}", verify="/etc/ssl/certs/ca-certificates.crt").content)

    race_session = None
    for session in sessions:
        if session["session_type"] == "Race":
            race_session = session

    session_key = race_session["session_key"]

    current = datetime.datetime(2026, 9, 6, 12, 19, 26)

    while True:
        current = current + timedelta(seconds=30)
        ftime = current.strftime("%Y-%m-%dT%H:%M:%S+00:00")

        print(ftime)

        control = json.loads(requests.get(openf1_base_url + f"race_control?session_key={session_key}&date<{ftime}", verify="/etc/ssl/certs/ca-certificates.crt").content)

        for message in control:
            if message not in all_received_control:
                handle_control_message(message)

        sleep.sleep(5)

def get_result_previous():
    meetings = json.loads(requests.get(openf1_base_url + "meetings?year=2026&country_name=Brazil", verify="/etc/ssl/certs/ca-certificates.crt").content)
    meeting_key = meetings[0]["meeting_key"]
    sessions = json.loads(requests.get(openf1_base_url + f"sessions?meeting_key={meeting_key}", verify="/etc/ssl/certs/ca-certificates.crt").content)

    race_session = None
    for session in sessions:
        if session["session_type"] == "Race":
            race_session = session

    session_key = race_session["session_key"]

    driver_order = [driver["driver_number"] for driver in json.loads(requests.get(openf1_base_url + f"session_result?session_key={session_key}", verify="/etc/ssl/certs/ca-certificates.crt").content)]
    print(driver_order)
    print("Getting driver data...")

    allDrivers = []

    for driver_num in driver_order:
        time.sleep(0.5)
        driver = json.loads(requests.get(openf1_base_url + f"drivers?driver_number={driver_num}&session_key={session_key}", verify="/etc/ssl/certs/ca-certificates.crt").content)[0]
        print(driver)
        allDrivers.append(driver)

    return allDrivers

def get_current_driver_data():
    all_drivers = []
    found_numbers = []

    drivers = json.loads(requests.get(openf1_base_url + f"drivers?session_key=latest", verify="/etc/ssl/certs/ca-certificates.crt").content)

    for driver in drivers:
        if driver["driver_number"] not in found_numbers:
            found_numbers.append(driver["driver_number"])
            all_drivers.append(driver)

    return all_drivers

def get_latest_positions():
    aa = json.loads(requests.get(openf1_base_url + f"position?session_key=latest").content)
    print(json.dumps(aa, indent=2))

    currentPositions = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    for event in aa:
        currentPositions[event["position"] - 1] = event["driver_number"]

    return currentPositions

if __name__ == '__main__':
    print(get_latest_positions())