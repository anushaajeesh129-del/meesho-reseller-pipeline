def alias_for(reseller_id):
    return "ALIAS-" + reseller_id[2:]


def assert_no_raw_names_leak(text, names):
    for name in names:
        if name in text:
            return False
    return True