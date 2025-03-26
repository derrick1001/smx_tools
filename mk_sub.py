from requests import post

name = input("Name: ")
acct = input("Acct: ")
address = input("Address: ")
city = input("City: ")
state = input("State: ")
zip = input("Zip: ")
fname = input("First: ")
lname = input("Last: ")
phone = input("Phone: ")
email = input("Email: ")

payload = {
    "name": name,
    "customId": acct,
    "type": "Residential",
    "orgId": "Calix",
    "locations": [
        {
            "primary": True,
            "address": [
                {
                    "streetLine1": address,
                    "city": city,
                    "state": state,
                    "zip": zip,
                }
            ],
            "contacts": [
                {
                    "firstName": fname,
                    "lastName": lname,
                    "phone": phone,
                    "email": email,
                    "primary": True,
                }
            ],
        }
    ],
}

sub = post(
    "https://10.20.7.10:18443/rest/v1/ems/subscriber",
    auth=("admin", "Thesearethetimes!"),
    verify=False,
    json=payload,
)
print(sub.json())
if sub.status_code == 201:
    print("\nSubscriber created successfully!")
else:
    print(sub.json())
