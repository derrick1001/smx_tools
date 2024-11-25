from calix.affected_decorator import affected_decorator
from crayon import c_BLUE, c_WHITE

E9 = input(f"{c_BLUE}E9{c_WHITE}: ")
ONTS = list(input(f"{c_BLUE}ONT_IDS{c_WHITE}: ").split())


@affected_decorator
def main(e9=None):
    return ONTS


if __name__ == "__main__":
    subs = main(E9)
    for sub in subs:
        print(sub)
