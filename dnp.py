import csv

from remove_subs_smx import rem_sub, rem_ont


def contruct(get_names: callable) -> set:
    def inner(csv0, csv1):
        names = get_names(csv0, csv1)
        with open(csv1, "r") as f:
            reader = csv.DictReader(f)
            ont_e9_acct = {
                (data.get("OntId"), data.get("DeviceName"), data.get("AccountName"))
                for data in reader
                for name in names
                if name == data.get("SubscriberName")
            }
            return ont_e9_acct

    return inner


@contruct
def get_names(csv_file: str, csv_file1: str) -> set:
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        names = {row.get("Contact Name") for row in reader}
        return names


if __name__ == "__main__":
    data = get_names("fiber_dnp.csv", "inventory.csv")
    accounts = [acct for id, e9, acct in data]
    devices = {id: e9 for id, e9, acct in data}
    rem_ont(devices)
    rem_sub(accounts)
