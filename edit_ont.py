from requests import put

id = ["2001", "2002", "2003", "2004", "2005"]

for i in id:
    sn = input("SN: ")
    payload = {
        "serial-number": sn,
        "ont-id": i,
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
