from requests import post

e9 = 'CVEC-E9-1'
vlan = '500'
pkg = 'Epic'
acct = '2000'

payload = {
    "vlan": vlan,
    "serviceType": "DATA_SERVICE",
    "deleteService": false,
    "inActive": false,
    "deletePolicyMap": true,
    "changeGlobalVlan": false,
    "changeGlobalCTag": false,
    "deleteL2match": false,
    "aeontcard": false,
    "poncard": false,
    "in-provisioning": false,
    "device-name": e9,
    "ont-port-id": "x1",
    "admin-state": "enabled",
    "ont-id": "7361",
    "subscriber-id": acct,
    "admin-status": "active",
    "policy-map": pkg,
    "service-name": "Data",
    "address": "0.0.0.0/0",
    "ping": true,
    "traceroute": true,
    "is10GECard": false,
    "isAEONTCard": false,
    "isPONCard": false,
  }

service = post(
    "https://10.20.7.10:18443/rest/v1/ems/service"
    auth=("admin", "Thesearethetimes!"),
    verify=False,
    json=payload,
)
if service.status_code == 200:
    print("\nONT created successfully!")
else:
    print(service.json())
