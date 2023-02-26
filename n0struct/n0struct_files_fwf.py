import typing
from pathlib import Path
import n0struct
from .n0struct_n0list_n0dict import n0dict
# ******************************************************************************
# ******************************************************************************
def load_fwf_format(file_path: str):
    # fwf_format file is csv file, contains columns:
    #   #,name,offset,size,till
    loaded_format = load_csv(file_path)
    for i,column in enumerate(loaded_format):
        if (column_offset := column['offset']) is not None and column_offset != "":
            loaded_format[i]['offset'] = int(column_offset)
        else:
            loaded_format[i]['offset'] = None
        if (column_till := column['till']) is not None and column_till != "":
            loaded_format[i]['till']   = int(column_till)
        else:
            loaded_format[i]['till']   = None
        if (column_size := column['size']) is not None and column_size != "":
            loaded_format[i]['size']   = int(column_size)
        else:
            loaded_format[i]['size']   = None
    return loaded_format
# ******************************************************************************
def parse_fwf_line(incoming_row: str, fwf_format: dict, validate: bool = True, validate_empty: bool = True):
    if not fwf_format:
        raise SyntaxError("fwf_format is mandatory parameter")
    parsed_line = {}
    for format_column in fwf_format:
        if format_column['name']:
            column_value = None
            if (format_column_offset := format_column['offset']) is not None and \
               (format_column_till := format_column['till']) is not None:
                column_value = incoming_row[format_column_offset:format_column_till].strip()
            parsed_line.update({format_column['name']: column_value})
    if validate:
        error_messages =  []
        for format_column in fwf_format:
            if (format_column_validation := format_column['validation']):
                lambda_function_for_validation = eval("lambda column_value, row: " + format_column_validation)
                if not lambda_function_for_validation(column_value, parsed_line):
                    error_messages.append(format_column['error_message'])
        if error_messages:
            return incoming_row, ";".join(error_messages)
            
    return parsed_line
# ******************************************************************************
def load_fwf(file_path:str, header_format: dict, body_format: dict = None, tail_format: dict = None, validate: bool = True, validate_empty: bool = True):
    success_parsed_lines = []
    failed_lines = []
    if not header_format:
        raise SyntaxError("header_format is mandatory parameter")
    if not body_format:
        body_format = header_format
    if not tail_format:
        tail_format = body_format

    with open(file_path, 'rt') as filehandler:
        previous_line = None
        for i, line in enumerate(filehandler.read().split('\n')):
            if previous_line:
                parsed_line = parse_fwf_line(previous_line, header_format if i == 1 else body_format, validate, validate_empty)
                if isinstance(parsed_line, dict):
                    success_parsed_lines.append(parsed_line)
                else:
                    failed_lines.append(parsed_line)
            previous_line = line
        if previous_line:
            parsed_line = parse_fwf_line(previous_line, tail_format, validate, validate_empty)
            if isinstance(parsed_line, dict):
                success_parsed_lines.append(parsed_line)
            else:
                failed_lines.append(parsed_line)
    return success_parsed_lines, failed_lines
# ******************************************************************************
def generate_fwf_row(struct_to_save: dict, fwf_format: dict, filler:str = ' '):
    if not fwf_format:
        raise Exception("fwf_format is mandatory parameter")

    line_len = max([column['till'] for column in fwf_format])
    rendered_line = filler*line_len

    for format_column in fwf_format:
        format_column_mapping = None
        if format_column['name'] in struct_to_save:
            column_value = struct_to_save[format_column['name']]
        elif (format_column_mapping := format_column['mapping']):
            # n0struct.n0debug("struct_to_save")
            lambda_function_for_mapping = eval("lambda incoming_row: " + format_column_mapping)
            # n0struct.n0debug("format_column_mapping")
            column_value = lambda_function_for_mapping(struct_to_save)
        else:
            continue
        format_column_size = format_column['size']
        if format_column.get('type') == 'int':
            column_value = str(column_value).zfill(format_column_size)[:format_column_size]
        else:
            column_value = str(column_value).ljust(format_column_size)[:format_column_size]
        rendered_line = rendered_line[:format_column['offset']] +  column_value + rendered_line[format_column['till']:]

    return rendered_line
# ******************************************************************************
def generate_fwf(root_node:dict, list_xpath:str, mapping_dict:dict, fwf_format: dict, save_to:str = None, filler:str = ' ') -> list:
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
                header = [str(i) for i in range(0,len(list_of_items[0]))]
            elif isinstance(list_of_items[0], dict):
                header = list(list_of_items[0].keys())
            mapping_dict = {column_name: column_name for column_name in header}
        else:
            header = list(mapping_dict.keys())

        for found_item in list_of_items:  # found_item == row in case of CSV list or item node in case of XML structure
            if isinstance(found_item, dict):
                found_item = n0struct.n0dict(found_item) # to have ability to use .first(xpath)
            elif isinstance(found_item, list):
                found_item = n0struct.n0list(found_item) # to have ability to use .first(xpath)

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