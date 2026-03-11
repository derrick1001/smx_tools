from warnings import filterwarnings
from sys import path
from time import sleep
import logging

import auth
from calix.e9 import CalixE9
from calix.ont_detail import ont
from calix.axos_e9 import e9
from calix.rmont import rmont
from calix.post_eth_serv import mk_eth_serv
from calix.post_ont import mk_ont
from calix.crayon import c_CYAN, c_GREEN, c_MAGENTA, c_RED, c_WHITE
from requests import get, put

# NOTE: Configure logging paramerters
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s %(name)s %(asctime)s: %(message)s (Line: %(lineno)d in %(filename)s)")
file_handler = logging.FileHandler("ont_test.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

path.append("/home/test/smx_tools/")
filterwarnings("ignore", message="Unverified HTTPS request")

LOW_UP_THRESHOLD = range(-30, -22)
LOW_DOWN_THRESHOLD = range(-25, -20)
cvec = CalixE9("10.20.0.51", "CVEC-E9-1")
ONT_RANGE = range(201, 217)


def get_count():
    wt = f"{c_CYAN}Waiting for ONTs"
    while True:
        print(wt + ".", end="\r")
        sleep(1)
        print(wt + "..", end="\r")
        sleep(1)
        print(wt + "...", end="\r")
        sleep(1)
        print(wt.strip("."), end="   \n")
        count = cvec.connection.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered-ont[^s] | exclude 9A3F1A | count")
        serial_numbers = cvec.connection.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered-ont[^s] | exclude 9A3F1A").split()[2::3]
        for serial_number in serial_numbers:
            print(f"Found {c_MAGENTA}{serial_number}")
        if '5' in count:
            return 5


def get_discovered():
    # NOTE:
    # If discovering both ports is necessary, do it here and join the lists together with sh_ont.extend()
    #
    sh_ont = cvec.connection.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered-ont | exclude 9A3F1A").split()[3::3]
    cxnk = [f"0{i}" if len(i) == 7 else f"00{i}" for i in sh_ont]
    return cxnk


def get_light(id: str) -> str:
    response = ont(cvec.name, id)
    try:
        dl = int(float(response.get('opt-signal-level')))
        ul = int(float(response.get('ne-opt-signal-level')))
        dber = response.get('ds-sdber-rate')
        uber = response.get('us-sdber-rate')
    except (TypeError, AttributeError):
        dl = None
        ul = None
        dber = None
        uber = None
    if dl in LOW_DOWN_THRESHOLD:
        dl = f"{c_RED}{dl}"
    if ul in LOW_UP_THRESHOLD:
        ul = f"{c_RED}{ul}"
    if dber != '1.00E-14':
        dber = f"{c_RED}{dber}"
    if uber != '1.00E-14':
        uber = f"{c_RED}{dber}"
    return f"{c_CYAN}DL_{id}:\t{c_GREEN}{dl}\n\t{c_GREEN}{dber}\n{c_CYAN}UL_{id}:\t{c_GREEN}{ul}\n\t{c_GREEN}{uber}\n"


def make_payload(id: str, sn: str) -> tuple[dict, dict]:
    new_ont_payload = {
        "ont-id": id,
        "ont-type": "Residential",
        "isGlobalOnt": False,
        "serial-number": f"CXNK{sn}",
        "ont-profile-id": "GP1100X",
        "subscriber-id": id,
    }
    services_payload = {
        "changeGlobalVlan": True,
        "serviceType": "DATA_SERVICE",
        "device-name": cvec.name,
        "ont-port-id": "x1",
        "admin-state": "enabled",
        "admin-status": "active",
        "ont-id": id,
        "subscriber-id": id,
        "policy-map": "Elite",
        "service-name": "Data",
        "vlan": id,
    }
    return new_ont_payload, services_payload


def rcode_500(id: str, sn: str):
    new_ont_payload, services_payload = make_payload(id, sn)
    print(f"\n{c_RED}Serial number {c_MAGENTA}CXNK{sn} {c_RED}already in use, deleting and reassigning...")
    sleep(2)
    for hostname in e9.keys():
        get_id = get(f"https://10.20.7.10:18443/rest/v1/config/device/{hostname}/ont?serial-number=CXNK{sn}",
                     auth=(auth.username, auth.password),
                     verify=False)
        if get_id.status_code == 200:
            print(f"{c_MAGENTA}{sn}{c_WHITE} found on {c_GREEN}{hostname}")
            if hostname == 'CVEC-E9-1':
                print(f"{c_CYAN}Deleting old ONT...")
                rmont(id, cvec.name)
                sleep(2)
                print(f"{c_CYAN}Making new ONT...")
                mk_ont(cvec.name, **new_ont_payload)
                sleep(2)
                print(f"{c_CYAN}Applying services...")
                mk_eth_serv(**services_payload)
                break
            nid = get_id.json()[0].get("ont-id")
            sleep(2)
            print(f"{c_CYAN}Deleting old ONT...")
            rmont(nid, hostname)
            sleep(1)
            rmont(id, cvec.name)
            sleep(1)
            print(f"{c_CYAN}Making new ONT...")
            mk_ont(cvec.name, **new_ont_payload)
            sleep(2)
            print(f"{c_CYAN}Applying services...")
            mk_eth_serv(**services_payload)
            sleep(2)
            validate = get(f"https://10.20.7.10:18443/rest/v1/config/device/{cvec.name}/ont?serial-number=CXNK{sn}",
                           auth=(auth.username, auth.password),
                           verify=False)
            if validate.status_code == 200:
                print(f"\nONT {c_MAGENTA}{sn} {c_WHITE}successfully updated with account {c_CYAN}{id}")
                return 0
        elif get_id.status_code == 404:
            print(f"{c_MAGENTA}{sn} {c_WHITE}not found on {c_CYAN}{hostname}, searching...")
            sleep(1)
            continue


def kansas_city_shuffle(id, sn) -> int:
    service = put(f"https://10.20.7.10:18443/rest/v1/config/device/{cvec.name}/ont?action=replace&ont-id={id}&serial-number=CXNK{sn}",
                  auth=(auth.username, auth.password),
                  verify=False,
                  )
    return service


if __name__ == "__main__":
    while True:
        count = get_count()
        if count == 5:
            print(f"{c_GREEN}ONTs discovered!!\n")
            sleep(2)
            serial_numbers = get_discovered()
            for id, sn in zip(ONT_RANGE, serial_numbers):
                payload = {
                    "serial-number": sn,
                    "ont-id": id,
                    "ont-profile-id": "GP1100X",
                    "subscriber-id": id,
                }
                service = kansas_city_shuffle(id, sn)
                if service.status_code == 200:
                    print(f"\nONT {c_MAGENTA}{sn} {c_WHITE}successfully updated with account {c_CYAN}{id}")
                    sleep(2)
                    levels = get_light(id)
                    print(levels)
                elif service.status_code == 500 or service.status_code == 403:
                    rcode_500(id, sn)
                    sleep(2)
                    levels = get_light(id)
                    print(levels)
                elif service.status_code == 404:
                    print(f"{c_CYAN}{id} {c_WHITE} does not exist, creating...")
                    new_ont_payload, services_payload = make_payload(id, sn,)
                    sleep(2)
                    mk_ont(cvec.name, **new_ont_payload)
                    sleep(2)
                    print(f"{c_CYAN}Applying services...")
                    mk_eth_serv(**services_payload)
                    sleep(2)
                    levels = get_light(id)
                    print(levels)
                elif service.status_code == 412:
                    print(f"{c_MAGENTA}{sn} {c_WHITE} is already assigned to {c_CYAN}{id}{c_WHITE}, skipping...")
                    sleep(2)
                    levels = get_light(id)
                    print(levels)
                    continue
                else:
                    print(service.status_code)
                    print(service.json())
                    break
            sleep(180)
        else:
            continue
