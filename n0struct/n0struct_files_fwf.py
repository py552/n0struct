import typing
from pathlib import Path
from .n0struct_n0list_n0dict import (
    n0dict,
    n0list,
)
# from .n0struct_logging import (
    # n0print,
    # n0debug,
    # n0debug_calc,
    # n0error,
# )
from .n0struct_utils import (
    to_int,
)
# ******************************************************************************
# ******************************************************************************
def load_fwf_format(file_path: str) -> dict:
    # fwf_format file is csv file, contains columns 'name','offset' and 'width' or 'till'
    return {
        row['name']: {
            'offset':   to_int(column.get('offset'), default_value = None),
            'width':    to_int(column.get('width'), default_value = None),
            'till':     to_int(column.get('till'), default_value = None),
        }
        for row in load_csv(file_path, mandatory_columns=('name','offset'))
    }
# ******************************************************************************
def parse_fwf_row(incoming_row: str, fwf_format: dict, validate: bool = True) -> typing.Union[dict, tuple]:
    if not fwf_format:
        raise SyntaxError("fwf_format is mandatory parameter")
    parsed_row = {}
    for column_name, column_format in fwf_format.items():
        column_value = None
        column_format_offset = column_format.get('offset')  # removed walrus operator for compatibility with 3.7
        column_format_width = column_format.get('width')    # removed walrus operator for compatibility with 3.7
        column_format_till = column_format.get('till')      # removed walrus operator for compatibility with 3.7
        if column_format_offset is not None:
            if column_format_till is None and column_format_width is not None:
                column_format_till = column_format_offset + column_format_width
            if column_format_till is not None:
                column_value = incoming_row[column_format_offset:column_format_till]
        column_format_validations = column_format.get('validations')  # removed walrus operator for compatibility with 3.7
        if validate and column_format_validations:
            error_messages =  []
            for column_format_validation in column_format_validations:
                lambda_function_for_validation = eval("lambda column_value, row, parsed_row: " + column_format_validation)
                if not lambda_function_for_validation(column_value, incoming_row, parsed_row):
                    error_messages.append(column_format.get('error_message'))
            if error_messages:
                return incoming_row, ";".join(error_messages)
        parsed_row.update({column_name: column_value})

    return parsed_row
# ******************************************************************************
def load_fwf(file_path: str, header_format: dict, body_format: dict = None, footer_format: dict = None, validate: bool = True, EOL: str = '\n', return_original_row = None):
    successfully_parsed_rows = []
    failed_rows = []
    if not header_format:
        raise SyntaxError("header_format is mandatory parameter")
    if not body_format:
        body_format = header_format
    if not footer_format:
        footer_format = body_format

    with open(file_path, 'rt') as filehandler:
        previous_row = None
        for i, row in enumerate(filehandler.read().split(EOL)):
            if previous_row:
                parsed_row = parse_fwf_row(previous_row, header_format if i == 1 else body_format, validate)
                if isinstance(parsed_row, dict):
                    if return_original_row:
                        parsed_row[return_original_row] = previous_row
                    successfully_parsed_rows.append(parsed_row)
                else:
                    failed_rows.append(i, *parsed_row)
            previous_row = row
        if previous_row:
            parsed_row = parse_fwf_row(previous_row, footer_format, validate)
            if isinstance(parsed_row, dict):
                if return_original_row:
                    parsed_row[return_original_row] = previous_row
                successfully_parsed_rows.append(parsed_row)
            else:
                failed_rows.append(parsed_row)
    if validate:
        return successfully_parsed_rows, failed_rows
    else:
        return successfully_parsed_rows
# ******************************************************************************
def generate_fwf_row(struct_to_save: dict, fwf_format: dict, filler: str = ' '):
    if not fwf_format:
        raise SyntaxError("fwf_format is mandatory parameter")

    row_len = max([column['till'] for column in fwf_format])
    rendered_row = filler*row_len

    for column_format in fwf_format:
        column_format_mapping = column_format.get('mapping')    # removed walrus operator for compatibility with 3.7
        if column_format['name'] in struct_to_save:
            column_value = struct_to_save[column_format['name']]
        elif column_format_mapping:
            lambda_function_for_mapping = eval("lambda incoming_row: " + column_format_mapping)
            column_value = lambda_function_for_mapping(struct_to_save)
        else:
            continue
        column_format_size = column_format['size']
        if column_format.get('type') == 'int':
            column_value = str(column_value).zfill(column_format_size)[:column_format_size]
        else:
            column_value = str(column_value).ljust(column_format_size)[:column_format_size]
        rendered_row = rendered_row[:column_format['offset']] +  column_value + rendered_row[column_format['till']:]

    return rendered_row
# ******************************************************************************
def generate_fwf(root_node: dict, list_xpath: str, mapping_dict: dict, fwf_format: dict, save_to: str = None, filler: str = ' ') -> list:
    if isinstance(root_node, (list, tuple)):
        list_of_items = root_node
    else:
        list_of_items = root_node.get(list_xpath, tuple())

    if save_to:
        out_filehandler = open(save_to, 'wt')

    fwf_table = []
    if list_of_items:
        if mapping_dict is None:
            if isinstance(list_of_items[0], list):
                header = [str(i) for i in range(0, len(list_of_items[0]))]
            elif isinstance(list_of_items[0], dict):
                header = list(list_of_items[0].keys())
            mapping_dict = {column_name: column_name for column_name in header}

        for found_item in list_of_items:  # found_item == row in case of CSV list or item node in case of XML structure
            if isinstance(found_item, dict):
                found_item = n0dict(found_item) # to have ability to use .first(xpath)
            elif isinstance(found_item, list):
                found_item = n0list(found_item) # to have ability to use .first(xpath)

            fwf_row = {}
            for column_name in mapping_dict:
                xpaths = mapping_dict[column_name]
                if not isinstance(xpaths, (list, tuple)):
                    xpaths = [xpaths]
                for xpath in xpaths:
                    found_value = found_item.first(xpath, "")
                    if found_value:
                        break
                fwf_row.update({column_name: found_value})
            fwf_table.append(fwf_row)

            if save_to:
                out_filehandler.write(generate_fwf_row(fwf_row, fwf_format, filler))

    if save_to:
        out_filehandler.close

    return fwf_table
# ******************************************************************************
# ******************************************************************************
