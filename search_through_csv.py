import csv

a = ["1700000579", "1700000676"]

result = {}
with open("inventory.csv", "r") as f:
    chreader = csv.DictReader(f)
    for row in chreader:
        for s in a:
            if s in row.get("AccountName"):
                result[row["OntId"]] = row["DeviceName"]

print(result)
