from warnings import filterwarnings
from sys import path
from time import sleep

from calix.e9 import CalixE9
from calix.ont_detail import ont
from calix.axos_e9 import e9
from calix.rmont import rmont
from calix.post_eth_serv import mk_eth_serv
from calix.post_ont import mk_ont
from calix.crayon import c_CYAN, c_GREEN, c_MAGENTA, c_RED, c_WHITE
from requests import get, put

path.append("/home/test/smx_tools/")
filterwarnings("ignore", message="Unverified HTTPS request")

LOW_UP_THRESHOLD = range(-30, -22)
LOW_DOWN_THRESHOLD = range(-25, -20)
cvec = CalixE9("10.20.0.51", "CVEC-E9-1")
ont_range = range(201, 217)


def get_count():
    wt = f"{c_CYAN}Waiting for ONTs"
    while True:
        print(wt + ".", end="\r")
        sleep(1)
        print(wt + "..", end="\r")
        sleep(1)
        print(wt + "...", end="\r")
        sleep(1)
        print(wt.strip("."), end="   \r")
        count = cvec.connection.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered-ont[^s] | count")
        if '5' in count:
            return 5


def get_discovered():
    # If discovering both ports is necessary, do it here and join the lists together with sh_ont.extend()
    sh_ont = cvec.connection.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered").split()[3::3]
    models = cvec.connection.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc model").split()[1::2]
    cxnk = [f"0{i}" if len(i) == 7 else f"00{i}" for i in sh_ont]
    return {sn: mod for sn, mod in zip(cxnk, models)}


def get_light(id: str) -> str:
    response = ont(cvec.name, id)
    try:
        dl = int(float(response.get('opt-signal-level')))
        ul = int(float(response.get('ne-opt-signal-level')))
    except TypeError:
        dl = None
        ul = None
    dber = response.get('ds-sdber-rate')
    uber = response.get('us-sdber-rate')
    if dl in LOW_DOWN_THRESHOLD:
        dl = f"{c_RED}{dl}"
    if ul in LOW_UP_THRESHOLD:
        ul = f"{c_RED}{ul}"
    if dber != '1.00E-14':
        dber = f"{c_RED}{dber}"
    if uber != '1.00E-14':
        uber = f"{c_RED}{dber}"
    return f"{c_CYAN}DL_{id}:\t{c_GREEN}{dl}\n\t{c_GREEN}{dber}\n{c_CYAN}UL_{id}:\t{c_GREEN}{ul}\n\t{c_GREEN}{uber}\n"


def rcode_500(id: str, sn: str, mod: str):
    print(f"\n{c_RED}Serial number {c_MAGENTA}CXNK{sn} {c_RED}already in use, force deleting and reassigning")
    sleep(2)
    for hostname in e9.keys():
        get_id = get(f"https://10.20.7.10:18443/rest/v1/config/device/{hostname}/ont?serial-number=CXNK{sn}",
                     auth=("admin", "Thesearethetimes!"),
                     verify=False)
        if get_id.status_code == 200:
            print(f"{c_MAGENTA}{sn}{c_WHITE} found on {c_GREEN}{hostname}")
            sleep(1)
            nid = get_id.json()[0].get("ont-id")
            print(f"{c_CYAN}Deleting old ONT...")
            sleep(2)
            rmont(nid, hostname)
            payload = {
                "ont-id": id,
                "ont-type": "Residential",
                "isGlobalOnt": False,
                "serial-number": f"CXNK{sn}",
                "ont-profile-id": mod,
                "subscriber-id": id,
            }
            print(f"{c_CYAN}Making new ONT...")
            sleep(2)
            mk_ont(cvec.name, **payload)
            print(f"{c_CYAN}Applying services...")
            sleep(2)
            payload = {
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
            mk_eth_serv(**payload)
            print(f"{c_GREEN}ONT updated successfully!")
        elif get_id.status_code == 404:
            print(f"{c_MAGENTA}{sn} {c_WHITE}not found on {c_CYAN}{hostname}, searching...")
            sleep(1)
            continue
        else:
            print(f"{c_RED}, {c_WHITE}could not find {c_MAGENTA}{sn}")
            sleep(1)
            print(get_id.json())


if __name__ == "__main__":
    while True:
        count = get_count()
        if count == 5:
            print(f"{c_GREEN}ONTs discovered!!\n")
            sleep(2)
            mod = get_discovered()
            for id, sn in zip(ont_range, mod):
                payload = {
                    "serial-number": sn,
                    "ont-id": id,
                    "ont-profile-id": mod[sn],
                    "subscriber-id": id,
                    "twdm-channel": {
                        "rmon-session": [
                          {
                            "bin-duration": 1,
                            "bin-count": 100
                          }
                        ]
                      }
                }
                service = put(
                    f"https://10.20.7.10:18443/rest/v1/config/device/{cvec.name}/ont?action=update&ont-id={id}&serial-number=CXNK{sn}",
                    auth=("admin", "Thesearethetimes!"),
                    verify=False,
                    json=payload,
                )
                if service.status_code == 200:
                    print(f"\nONT {c_MAGENTA}{sn} {c_WHITE}successfully updated with account {c_CYAN}{id}")
                    sleep(2)
                    levels = get_light(id)
                    print(levels)
                elif service.status_code == 500:
                    rcode_500(id, sn, mod[sn])
                    sleep(2)
                    levels = get_light(id)
                    print(levels)
                else:
                    print(service.status_code)
                    print(service.json())
                    continue
            sleep(180)
        else:
            continue
