#!/usr/bin/python3

import re
from calix import ssp, netcon, cx_detail
from crayon import c_BLUE, c_GREEN, c_YELLOW, c_RED, c_CYAN, c_MAGENTA
from typing import Generator, List, Callable


def end(wr_main: Callable) -> str:
    def wrap_wr_main(*args):
        ranged_onts, e9 = wr_main(*args)
        ont_ids = (id.get("ont-id") for id in ranged_onts)
        names = (cx_detail(e9, id).json().get("name") for id in ont_ids)
        for name in names:
            print(name)
        print(ont_ids)
        return

    return wrap_wr_main


#            for k, v in i.items():
#                if k == "ranged-onts":
#                    continue
#                if k == "ont-id":
#                    print(f"{c_BLUE}{k}\t\t{c_GREEN}{v}")
#                    continue
#                if "errors" in k:
#                    numv = int(v)
#                    if numv == 0:
#                        print(f"{c_BLUE}{k}\t{c_MAGENTA}{v}")
#                    else:
#                        print(f"{c_BLUE}{k}\t{c_RED}{v}")
# ;                    continue
#                if k == "ds-sdber-rate":
#                    print(f"{c_BLUE}{k}\t{c_YELLOW}{v}\n")
#                    continue
#                print(f"{c_BLUE}{k}\t{c_YELLOW}{v}")
#    q = input(f"{c_CYAN}Press enter to exit...")
#    if q is None:
#        exit()


def ranged_onts(main: Callable) -> Callable:
    @end
    def wr_main(*args) -> Generator:
        # This is what main return objects are
        t: tuple[str, str] = main(*args)
        ronts, e9 = t
        match: List[str] = re.split(r"ont CXNK [A-Z0-9]{6,7}", ronts)
        match_lst: Generator = (i.split() for i in match[1:])
        ranged_onts: Generator = (
            dict(zip(i[::2], i[1::2])) for i in match_lst)
        return ranged_onts, e9

    return wr_main


@ranged_onts
def main(cnct: Callable) -> tuple[str, str]:
    ranged_onts: str = cnct.send_command_timing(
        f"show interface pon {shelf}/{slot}/xp{port} ranged-onts statistics"
    )
    cnct.send_command_timing("configure")
    e9: str = (
        cnct.send_command_timing("show full-configuration hostname")
        .split("\n")[0]
        .lstrip("hostname ")
    )
    cnct.send_command_timing("exit")
    return ranged_onts, e9


t: tuple[str, str, str] = ssp()
shelf, slot, port = t
if __name__ == "__main__":
    main(netcon(*t))
