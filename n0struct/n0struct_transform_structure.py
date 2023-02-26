# ******************************************************************************
# ******************************************************************************
strip_ns = lambda key: key.split(':',1)[1] if ':' in key else key
# ******************************************************************************
'''
# Sample
currency_converter = {"682": "SAR"}
keys_for_currency_convertion = {
    "currency":         lambda value: currency_converter[value] if value in currency_converter else value,
    "source_currency":  lambda value: currency_converter[value] if value in currency_converter else value,
}
def convert_to_native_format(value, key = None, exception = None, transform_depends_of_key = keys_for_currency_convertion):
'''
# ******************************************************************************
def convert_to_native_format(value, key = None, exception = None, transform_depends_of_key = None):
    if key is not None:
        if exception is not None:
            if key in exception:
                return value
        if key in transform_depends_of_key:
            return transform_depends_of_key[key](value)
    if isinstance(value, str):
        value = value.strip()
        if len(value) == 10 and value[2] == '/' and value[5] == '/':
            return datetime.strptime(value, "%d/%m/%Y")  # EUROPEAN!!!
        if len(value) == 10 and value[4] == '-' and value[7] == '-':
            return datetime.strptime(value, "%Y-%m-%d")
        if len(value) == 19 and value[4] == '-' and value[7] == '-' and value[10] == ' ' and value[13] == ':' and value[16] == ':':
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        if n0isnumeric(value):
            return abs(float(value))
        else:
            return value.upper()
    else:
        return value
# ******************************************************************************
def transform_structure(in_structure, transform_key = strip_ns, transform_value = convert_to_native_format):
    if isinstance(in_structure, dict):
        in_list = [in_structure]  # 0.18 = 2020-10-22 workaround fix for Py38: changing (A,) into [A], because of generates NOT tuple, but initial A
    else:
        in_list = in_structure
    if isinstance(in_list, (list, tuple, n0list)):
        out_list = n0list()
        for in_dict in in_list:
            if not isinstance(in_dict, dict):
                raise TypeError("transform_structure(): expected to get dict/n0dict as second level item")
            out_list.append(n0dict())
            for key_in in in_dict:
                key_out = transform_key(key_in)
                out_list[-1].update({key_out: transform_value(in_dict[key_in], key_out) if transform_value else in_dict[key_in]})
    else:
        raise TypeError("transform_structure(): expected to get dict/n0dict or list/tuple/n0list as argument")
    if isinstance(in_structure, dict):
        return out_list[0]
    else:
        return out_list
# ******************************************************************************
# ******************************************************************************
