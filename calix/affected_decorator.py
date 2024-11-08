from calix.cx_detail import cx
from calix.ont_detail import ont
from calix.path import cvec_alrms

# NOTE:
#   Debating on what to do once code is churned through this
#   decorator. Write to file and reuse later?


def affected_decorator(func):
    def inner(*args, **kwargs):
        ont_ids = func()
        pon_ports = (ont(kwargs.get("e9"), id).get("linked-pon") for id in ont_ids)
        account = (cx(kwargs.get("e9"), id) for id in ont_ids)
        for sub in account:
            try:
                name = sub.get("name")
                acct = sub.get("customId")
                phone = sub.get("locations")[0].get("contacts")[0].get("phone")
                em = sub.get("locations")[0].get("contacts")[0].get("email")
                loc = (
                    sub.get("locations")[0].get("address")[0].get("streetLine1")
                    + ", "
                    + sub.get("locations")[0].get("address")[0].get("city")
                )
            except Exception:
                if name or acct is None:
                    continue
            else:
                if phone is None or phone == "":
                    phone = "No phone"
                if em is None or em == "":
                    em = "No email"
                if loc is None or loc == "":
                    loc = "No location"
                port = next(pon_ports)
            yield f"{acct}\n{name}\n{phone}\n{port}\n{em}\n{loc}\n"

    return inner
