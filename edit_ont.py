from time import sleep

from requests import delete, get, post, put

from calix.connection import calix_e9
from calix.del_ont import del_ont

# Convert ont to this data structure for more ONTs in the future
# ont = list(range(2001, end))
ont = ["2001", "2002", "2003", "2004", "2005"]
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
mod = {sn: mod for sn, mod in zip(cxnk, models)}

for id, sn in zip(ont, mod):
    if "DA3659" in sn:
        continue
    payload = {
        "serial-number": sn,
        "ont-id": id,
        "ont-profile-id": mod[sn],
    }
    service = put(
        f"https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont?action=update&ont-id={id}&serial-number=CXNK{sn}",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
        json=payload,
    )
    if service.status_code == 200:
        print("\nONT updated successfully!")
    elif service.status_code == 500:
        print("ONT id already exists, force deleting and reassigning")
        sleep(2)
        get_id = get(
            f"https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont?serial-number=CXNK{sn}",
            auth=("admin", "Thesearethetimes!"),
            verify=False,
        )
        nid = get_id.json()[0].get("ont-id")
        print("Deleting old ONT...")
        sleep(2)
        del_ont(nid)
        del_ont(id)
        payload = {
            "ont-id": id,
            "ont-type": "Residential",
            "isGlobalOnt": False,
            "serial-number": sn,
            "ont-profile-id": mod[sn],
        }
        print("Making new ONT...")
        sleep(2)
        mk_ont = post(
            "https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont",
            auth=("admin", "Thesearethetimes!"),
            verify=False,
            json=payload,
        )
        print("Applying services...")
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
            "policy-map": "Essential",
            "service-name": "Data",
            "vlan": id,
        }
        ont = post(
            f"https://10.20.7.10:18443/rest/v1/ems/service",
            auth=("admin", "Thesearethetimes!"),
            verify=False,
            json=payload,
        )
        print("\nONT updated successfully!")
