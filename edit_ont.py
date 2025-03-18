from calix.connection import calix_e9
from requests import put

ont = ["2001", "2002", "2003", "2004", "2005"]
cnct = calix_e9()
sh_ont = cnct.send_command_timing(
    "show interface pon 2/1/xp1 discovered-onts | notab | inc CXNK"
).split()[2::3]
sh_model = cnct.send_command_timing(
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
model = [i for i in sh_model]
for sn, mod in zip(cxnk, model):
    if mod == "GP1100X":
        continue
    print(f"{sn} is {mod}")


for id, sn, mod in zip(ont, cxnk, model):
    payload = {
        "serial-number": sn,
        "ont-id": id,
        "ont-profile-id": mod,
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
