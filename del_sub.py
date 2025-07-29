from requests import delete


# This will become input from a csv file
acct = input("Name: ")


del_sub = delete(
    f"https://10.20.7.10:18443/rest/v1/ems/subscriber/org/Calix/account/{acct}",
    auth=("admin", "Thesearethetimes!"),
    verify=False,
)
if del_sub.status_code == 200:
    print("Subscriber successfully deleted!!")
else:
    print(del_sub.json())
