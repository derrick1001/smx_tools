from calix.connection import calix_e9
from requests import put

ont = ["2001", "2002", "2003", "2004", "2005"]
cnct = calix_e9()
show_discovered = cnct.send_command_timing(
    "show interface pon 2/1/xp1 discovered-onts | notab | inc CXNK"
).split()[2::3]
cnct.disconnect()

cxnk = []
for i in show_discovered:
    if len(i) == 7:
        i = f"0{i}"
    elif len(i) == 6:
        i = f"00{i}"
    cxnk.append(i)
print(cxnk)


for id, sn in zip(ont, cxnk):
    payload = {
        "serial-number": sn,
        "ont-id": id,
        "ont-profile-id": "GP1100X",
    }
    service = put(
        f"https://10.20.7.10:18443/rest/v1/config/device/CVEC-E9-1/ont?action=update&ont-id={id}&serial-number=CXNK{sn}",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
        json=payload,
    )
    if service.status_code == 200:
        print("\nONT updated successfully!")
    else:
        print(service.json())
