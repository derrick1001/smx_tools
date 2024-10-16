# /usr/bin/python3


from warnings import filterwarnings
from sys import argv, path
from calix.missing import get_miss
from calix.subscriber import subs

path.append("/home/derrick/Derrick-shell-scripts/python/modules")
filterwarnings("ignore", message="Unverified HTTPS request")


def get_missing():
    from crayon import c_BLUE, c_CYAN, c_GREEN, c_YELLOW, c_MAGENTA, c_RED

    miss = get_miss(argv[1])
    for i in miss.json():
        if i.get("shelf-id") is None:
            continue
        ont_id = i.get("ont-id")
        sub = subs(argv[1], ont_id)
        shelf_id = i.get("shelf-id")
        slot_id = i.get("slot-id")
        port_id = i.get("port-id")
        sub_id = sub[2].get("ont-ethernet").get("subscriber-id")
        vl = sub[2].get("ont-ethernet").get("vlan")
        if vl is None:
            vlan_id = ""
            pm = ""
            pkg = ""
        else:
            vlan_id = vl[0].get("vlan-id")
            pm = vl[0].get("policy-map")
            pkg = pm[0].get("name")
        loc = i.get("location")
        print(
            f"{c_BLUE}ONT: {c_GREEN}{ont_id}\n{c_BLUE}Port: {c_GREEN}{shelf_id}/{c_GREEN}{slot_id}/{c_GREEN}{port_id}\n{c_BLUE}VLAN: {c_YELLOW}{vlan_id}\n{c_BLUE}PKG: {c_YELLOW}{pkg}\n{c_BLUE}Acct: {c_CYAN}{sub_id}{c_BLUE}\nLocation: {c_MAGENTA}{loc}\n"
        )
    q = input(f"{c_CYAN}Press enter to exit...")
    if q is None:
        exit()


if __name__ == "__main__":
    get_missing()
