from warnings import filterwarnings
from sys import path
from time import sleep

from calix.connection import calix_e9
from calix.rmont import rmont
from calix.post_eth_serv import mk_eth_serv
from calix.post_ont import mk_ont
from calix.crayon import c_CYAN, c_GREEN, c_MAGENTA, c_RED
from requests import get, put

path.append("/home/test/smx_tools/")
filterwarnings("ignore", message="Unverified HTTPS request")

ont = range(201, 217)
e9 = 'CVEC-E9-1'


def get_discovered():
    cnct = calix_e9()
    # If discovering both ports is necessary, do it here and join the lists together with sh_ont.extend()
    sh_ont = cnct.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered").split()[3::3]
    models = cnct.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc model").split()[1::2]
    cxnk = [f"0{i}" if len(i) == 7 else f"00{i}" for i in sh_ont]
    return {sn: mod for sn, mod in zip(cxnk, models)}


def rcode_500(id: str, sn: str, mod: str):
    print(f"\n{c_RED}Serial number {c_MAGENTA}CXNK{sn} {c_RED}already in use, force deleting and reassigning")
    sleep(2)
    get_id = get(f"https://10.20.7.10:18443/rest/v1/config/device/{e9}/ont?serial-number=CXNK{sn}",
                 auth=("admin", "Thesearethetimes!"),
                 verify=False)
    nid = get_id.json().get("ont-id")
    print(f"{c_CYAN}Deleting old ONT...")
    sleep(2)
    rmont(nid, e9)
    rmont(id, e9)
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
    mk_ont(e9, **payload)
    print(f"{c_CYAN}Applying services...")
    sleep(2)
    payload = {
        "changeGlobalVlan": True,
        "serviceType": "DATA_SERVICE",
        "device-name": e9,
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


if __name__ == "__main__":
    cnct = calix_e9()
    wt = f"{c_CYAN}Waiting for ONTs"
    while True:
        print(wt + ".", end="\r")
        sleep(1)
        print(wt + "..", end="\r")
        sleep(1)
        print(wt + "...", end="\r")
        sleep(1)
        print(wt.strip("."), end="   \r")
        count = cnct.send_command_timing("show interface pon 2/1/xp2 discovered-onts | notab | inc discovered-ont[^s] | count")
        if "4" in count:
            print(f"{c_GREEN}ONTs discovered!!\n")
            sleep(2)
            mod = get_discovered()
            print(mod)
            for id, sn in zip(ont, mod):
                payload = {
                    "serial-number": sn,
                    "ont-id": id,
                    "ont-profile-id": mod[sn],
                    "subscriber-id": id,
                }
                service = put(
                    f"https://10.20.7.10:18443/rest/v1/config/device/{e9}/ont?action=update&ont-id={id}&serial-number=CXNK{sn}",
                    auth=("admin", "Thesearethetimes!"),
                    verify=False,
                    json=payload,
                )
                if service.status_code == 200:
                    print(f"\n{c_GREEN}ONT {c_MAGENTA}{sn} successfully updated with account {c_CYAN}{ont}")
                elif service.status_code == 500:
                    rcode_500(id, sn, mod[sn])
                else:
                    print(service.json())
            sleep(180)
