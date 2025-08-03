from .n0struct_utils import isnumber

# ******************************************************************************
strip_ns = lambda key: key.split(':', 1)[1] if ':' in key else key
# ******************************************************************************
'''
sample:
    currency_converter = {"682": "SAR"}
    keys_for_currency_convertion = {
        "currency":         lambda value: currency_converter[value] if value in currency_converter else value,
        "source_currency":  lambda value: currency_converter[value] if value in currency_converter else value,
    }
    def convert_to_native_format(value, key = None, exception = None, transform_depends_of_key = keys_for_currency_convertion):
'''
# ******************************************************************************
def convert_to_native_format(value, key = None, exception: set = None, transform_depends_of_key: dict = None):
    if key is not None:
        if exception and key in exception:
            return value
        if transform_depends_of_key and key in transform_depends_of_key:
            return transform_depends_of_key[key](value)
    if isinstance(value, str):
        value = value.strip()
        if len(value) == 10 and value[2] == '/' and value[5] == '/':
            return datetime.strptime(value, "%d/%m/%Y")             # EUROPEAN not US
        if len(value) == 10 and value[4] == '-' and value[7] == '-':
            return datetime.strptime(value, "%Y-%m-%d")             # ISO date
        if len(value) == 19 and value[4] == '-' and value[7] == '-' and value[10] == ' ' and value[13] == ':' and value[16] == ':':
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")    # ISO datetime
        if isnumber(value):
            return abs(float(value))
        else:
            return value.upper()
    else:
        return value
# ******************************************************************************
def transform_dict(in_dict, transform_key = strip_ns, transform_value = convert_to_native_format):
    return {
        transform_key(k) if isinstance(transform_key, Callable) else k: transform_value(v) if isinstance(transform_value, Callable) else v
        for k,v in in_dict.items()
    }
# ******************************************************************************
def transform_dicts(in_dicts, transform_key = strip_ns, transform_value = convert_to_native_format):
    """
        {}    -> [{}]
        [{}]  -> [{ transform_key(k1): transform_value(v1), transform_key(k2): transform_value(v2), ... }, ...]

        usefull when required to convert list of dicts (2 level XML) with text data into native python structure with datetime/float
    """
    if isinstance(in_dicts, dict):
        return transform_dict(in_dict, transform_key, transform_value)
    return {
        transform_dict(in_dict, transform_key, transform_value)
        for in_dict in in_dicts
    }

################################################################################
__all__ = (
    'strip_ns',
    'convert_to_native_format',
    'transform_dict',
    'transform_dicts',
)
################################################################################
