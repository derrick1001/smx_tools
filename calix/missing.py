from requests import get


def missing(e9):
    miss_ont = get(
        f"https://10.20.7.10:18443/rest/v1/config/device/{e9}/ont/missingONTs?offset=0&limit=20",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return miss_ont
