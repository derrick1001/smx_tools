from requests import post

payload = {
    "changeGlobalVlan": True,
    "serviceType": "DATA_SERVICE",
    "device-name": "CVEC-E9-1",
    "ont-port-id": "x1",
    "admin-state": "enabled",
    "admin-status": "active",
    "ont-id": "548",
    "subscriber-id": "2010",
    "policy-map": "Essential",
    "service-name": "Data",
    "global-vlan-desc": "1000",
}

ont = post(
    f"https://10.20.7.10:18443/rest/v1/ems/service",
    auth=("admin", "Thesearethetimes!"),
    verify=False,
    json=payload,
)
if ont.status_code == 200:
    print(f"\nService provisioned successfully!")
else:
    print(ont.json())
