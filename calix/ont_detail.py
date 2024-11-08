from requests import get


# NOTE: Returns dict of ont detail
def ont(e9, ont_id):
    """
    *************************
    This function requires the E9 hostname and the ONT id

    e9: str
    ont_id: str

    Ex: ont('hostname', '1111')
    *************************
    """
    ont_detail = get(
        f"https://10.20.7.10:18443/rest/v1/performance/device/{e9}/ont/{ont_id}/status",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return ont_detail.json()
