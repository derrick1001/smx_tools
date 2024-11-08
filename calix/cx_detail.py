from requests import get


# NOTE: Returns dict of customer detail
def cx(e9, ont_id):
    """
    *************************
    This function requires the E9 hostname and the ONT id

    e9: str
    ont_id: str

    Ex: cx('hostname', '1111')
    *************************
    """
    cx_detail = get(
        f"https://10.20.7.10:18443/rest/v1/ems/subscriber/device/{e9}/port/{ont_id}%2Fx1",
        auth=("admin", "Thesearethetimes!"),
        verify=False,
    )
    return cx_detail.json()
