#!/usr/bin/python3

import csv


def rows(get_count):
    def inner(*args):
        count = get_count(args[0])
        s = 0
        f = 6
        sl = slice(s, f)
        while count > 0:
            sl = slice(s, f)
            b = args[0][sl]
            s += 6
            f += 6
            count -= 1
            yield b

    return inner


@rows
def get_count(sub_lst):
    count = 1
    while "" in sub_lst:
        sub_lst.remove("")
        count += 1
    return count


if __name__ == "__main__":
    with open("subs.txt", "r") as subs:
        col = ["Acct", "Name", "Phone", "Port/Fiber", "Email", "Address"]
        sub_lst = [i.rstrip("\n") for i in subs]
        z = get_count(sub_lst)
        data = [i for i in z]
        data.insert(0, col)
    with open("cx.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)
