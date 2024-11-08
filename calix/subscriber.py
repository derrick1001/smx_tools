from requests import get


def subs(e9, ont_id):
    subscriber = get(
        f"https://10.20.7.10:18443/rest/v1/config/device/{e9}/ontport/{ont_id}",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return subscriber.json()
