from requests import get

from calix.cx_detail import cx

# NOTE:
# This is the 'Subscribers' hyperlink under alarms
# This will show a good amount of information on the affected subscriber


def affected(e9, instid):
    response = get(
        f"https://10.20.7.10:18443/rest/v1/fault/export/csv/subscriber/device-name/{e9}/instance-id/{id}",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return response
