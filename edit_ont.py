from time import sleep

from calix.connection import calix_e9
from calix.del_ont import del_ont
from calix.post_eth_serv import mk_eth_serv
from calix.post_ont import mk_ont
from crayon import c_CYAN, c_GREEN, c_MAGENTA, c_RED
from requests import get, put

ont = range(2001, 2100)


def get_discovered():
    cnct = calix_e9()
    sh_ont = cnct.send_command_timing(
        "show interface pon 2/1/xp1 discovered-onts | notab | inc CXNK"
    ).split()[2::3]
    models = cnct.send_command_timing(
        "show interface pon 2/1/xp1 discovered-onts | notab | inc model"
    ).split()[1::2]
    cnct.disconnect()
    cxnk = []
    for i in sh_ont:
        if "DA3659" in i:
            continue
        if len(i) == 7:
            i = f"0{i}"
        elif len(i) == 6:
            i = f"00{i}"
        cxnk.append(i)
    return {sn: mod for sn, mod in zip(cxnk, models)}


def rcode_500(id: str, sn: str, mod: str):
    print(
        f"\n{c_RED}Serial number {c_MAGENTA}CXNK{sn} {c_RED}already in use, force deleting and reassigning"
    )
    sleep(2)
    get_id = get(
        f"https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont?serial-number=CXNK{sn}",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    nid = get_id.json()[0].get("ont-id")
    print(f"{c_CYAN}Deleting old ONT...")
    sleep(2)
    del_ont(nid)
    del_ont(id)
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
    mk_ont("CVEC-E9-1", **payload)
    print(f"{c_CYAN}Applying services...")
    sleep(2)
    payload = {
        "changeGlobalVlan": True,
        "serviceType": "DATA_SERVICE",
        "device-name": "CVEC-E9-1",
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
    mod = get_discovered()
    for id, sn in zip(ont, mod):
        if "DA3659" in sn:
            continue
        payload = {
            "serial-number": sn,
            "ont-id": id,
            "ont-profile-id": mod[sn],
            "subscriber-id": id,
        }
        service = put(
            f"https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont?action=update&ont-id={id}&serial-number=CXNK{sn}",
            auth=("admin", "Thesearethetimes!"),
            verify=False,
            json=payload,
        )
        if service.status_code == 200:
            print(f"\n{c_GREEN}ONT updated successfully!")
        elif service.status_code == 500:
            rcode_500(id, sn, mod[sn])
