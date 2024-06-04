#!/usr/bin/python3

from requests import get
from warnings import filterwarnings
from sys import argv, path

filterwarnings("ignore", message="Unverified HTTPS request")


def get_onts():
    path.append('/home/derrick/Derrick-shell-scripts/python/modules')
    from crayon import c_BLUE, c_CYAN, c_GREEN, c_YELLOW, c_MAGENTA, c_RED, c_WHITE
    shelf = (input(f'{c_BLUE}Shelf: {c_WHITE}'))
    slot = (input(f'{c_BLUE}Slot: {c_WHITE}'))
    port = (input(f'{c_BLUE}Port: {c_WHITE}'))
    response = get(f'https://10.20.7.10:18443/rest/v1/performance/device/{argv[1]}/ponstatus/shelf/{shelf}/slot/{slot}/port/{port}/status?refresh=false',
                   auth=('admin', 'Thesearethetimes!'),
                   verify=False)
    r = response.json()
    for i in r:
        ont_id = i.get('ont-id')
        sn = i.get('status').get('serial-number')
        subscriber = get(f'https://10.20.7.10:18443/rest/v1/config/device/{argv[1]}/ontport/{ont_id}',
                         auth=('admin', 'Thesearethetimes!'),
                         verify=False)
        sub = subscriber.json()
        sub_id = sub[2].get('ont-ethernet').get('subscriber-id')
        vl = sub[2].get('ont-ethernet').get('vlan')
        if vl is None:
            vlan_id = ""
            pm = ""
            pkg = ""
        else:
            vlan_id = vl[0].get('vlan-id')
            pm = vl[0].get('policy-map')
            pkg = pm[0].get('name')
        up_rx = i.get('detail').get('opt-signal-level')
        dn_rx = i.get('detail').get('ne-opt-signal-level')
        up_ber = i.get('detail').get('us-sdber-rate')
        dn_ber = i.get('detail').get('ds-sdber-rate')
        rlen = i.get('detail').get('range-length')
        rr = i.get('detail').get('latest-restart-reason')
        print(f'\n{c_BLUE}ONT: {c_GREEN}{ont_id}\n{c_BLUE}SN: {c_CYAN}CXNK{sn}\n{c_BLUE}Acct: {c_CYAN}{sub_id}\n{c_BLUE}Light U/D: {c_YELLOW}{up_rx}{c_GREEN}/{c_YELLOW}{dn_rx}\n{c_BLUE}BER: {c_YELLOW}{up_ber}{c_GREEN}/{c_YELLOW}{dn_ber}\n{c_BLUE}Range: {c_YELLOW}{rlen / 1000} km\n{c_BLUE}VLAN: {c_YELLOW}{vlan_id}\n{c_BLUE}PKG: {c_YELLOW}{pkg}\n{c_MAGENTA}{rr}')
    q = input(f'{c_CYAN}Press enter to exit...')
    if q is None:
        exit()


get_onts()
