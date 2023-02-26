import typing
from pathlib import Path
import n0struct
from .n0struct_n0list_n0dict import n0dict
# ******************************************************************************
# ******************************************************************************
def parse_complex_csv_line(
    line:str,
    separator:str = ',',
    strip_column:callable = lambda column_value: column_value,
) -> list:
    fields_in_the_row = []
    flag_delimiter_in_field = flag_expect_delimiter_or_quotes = False
    field_value = ""
    for i,ch in enumerate(line):
        if ch == separator and (not flag_delimiter_in_field or flag_expect_delimiter_or_quotes):
            fields_in_the_row.append(strip_column(field_value))
            flag_delimiter_in_field = flag_expect_delimiter_or_quotes = False
            field_value = ""
            continue  # skip separator
        elif ch == '"':
            if len(field_value) == 0:
                flag_delimiter_in_field = True
                continue  # skip " in the begining of the field
            elif flag_delimiter_in_field:
                if not flag_expect_delimiter_or_quotes:
                    flag_expect_delimiter_or_quotes = True
                    continue  # skip first " in the middle of line
                flag_expect_delimiter_or_quotes = False # Paired " is got, so save the second "
        elif flag_expect_delimiter_or_quotes:
            raise ValueError(f"Expected separator or second \", but received '{ch}' in offset {i} of '{line}'")
        field_value += ch
    fields_in_the_row.append(strip_column(field_value))
    return fields_in_the_row
# ******************************************************************************
def load_csv(
    file_name: str,
    format:list = None,
    separator:str = ',',
    contains_header:bool = False,
    strip_line:callable = lambda line: line,
    strip_column:callable = lambda column_value: column_value,
    parse_csv_line:callable = parse_complex_csv_line,
    skip_empty_lines:bool = True,
) -> typing.Generator:

    if not strip_line:
        strip_line = lambda line_value: line_value
    elif isinstance(strip_line, bool) and strip_line == True:
        strip_line = lambda line_value: line_value.strip()

    if not strip_column:
        strip_column = lambda column_value: column_value
    elif isinstance(strip_column, bool) and strip_column == True:
        strip_column = lambda column_value: column_value.strip()

    with open(file_name, 'rt') as in_file:
        if contains_header:
            while True:
                file_offset = in_file.tell()
                if not (line:=in_file.readline()):
                    return [] # Empty file or file only with spaces
                header_line = strip_line(line.rstrip('\n'))
                if header_line:
                    break
            column_names = parse_csv_line(header_line, separator, strip_column)
            if not isinstance(contains_header, bool):
                # if contains_header is not boolean, then first line could be header or not
                # to check if the first line is header, check value of first column
                # if it's like expected, then the first line is header
                if column_names[0] != contains_header:
                    in_file.seek(file_offset) # first line is NOT header, re-read first line as data line
                    column_names = None
            if not format:
                format = column_names

        if format and len(format) != len(set(format)):
            raise ValueError(f"Format {format} contains not unique names of columns")


        while True:
            if not (line:=in_file.readline()):
                return None  # EOF
            stripped_line = strip_line(line.rstrip('\n'))
            if skip_empty_lines and not stripped_line:
                continue
            column_values = parse_csv_line(stripped_line, separator, strip_column)
            if format:
                column_values = n0dict(zip(format, column_values))
            yield column_values
# ******************************************************************************
def load_simple_csv(
    file_name: str,
    format:list = None,
    separator:str = ',',
    contains_header = False,
    strip_line:callable = lambda line: line,
    strip_column:callable = lambda column_value: column_value,
) -> typing.Generator:
    return load_csv(
        file_name       = file_name,
        format          = format,
        separator       = separator,
        contains_header = contains_header,
        strip_line      = strip_line,
        strip_column    = strip_column,
        parse_csv_line  = lambda line, separator, strip_column: [strip_column(column_value) for column_value in line.split(separator)],
    )
# ******************************************************************************
def load_complex_csv(
    file_name: str,
    format:list = None,
    separator:str = ',',
    contains_header = False,
    strip_line:callable = lambda line: line,
    strip_column:callable = lambda column_value: column_value,
) -> typing.Generator:
    return load_csv(
        file_name       = file_name,
        format          = format,
        separator       = separator,
        contains_header = contains_header,
        strip_line      = strip_line,
        strip_column    = strip_column,
        parse_csv_line  = parse_complex_csv_line
    )
# ******************************************************************************
def generate_comlex_csv_row(row:list, separator:str = ',') -> str:
    buff = ""
    for column_i,column_value in enumerate(row):
        if column_value is None:
            column_value = ""
        elif not isinstance(column_value, str):
            column_value = str(column_value)
        if column_i:
            buff += separator
        if separator in column_value:
            if '"' in column_value:
                column_value = column_value.replace('"', '""')
            column_value = '"' + column_value + '"'
        buff += column_value
    buff += '\n'
    return buff
# ******************************************************************************
def generate_csv(root_node:dict, list_xpath:str, mapping_dict:dict = None, save_to:str = None, separator:str = ',', show_header:bool = True) -> list:
    '''
    Samples:
        response_json = n0dict({
            "records" : [
                {
                    "node" : {
                        "field1": "row1_value1",
                        "subnode1": {
                            "field2": "row1_value2",
                        },
                        "subnode2": {
                            "field3": "row1_value3",
                        },
                    }
                },
                {
                    "node" : {
                        "field1": "row2_value1",
                        "subnode1": {
                            "field2": "row2_value2",
                        },
                        "subnode2": {
                            "field3": "row2_value3",
                        },
                    }
                },
            ]
        })
        generated_csv = generate_csv(
                                        response_json,
                                        "//records[*]",
                                        {
                                            "Name of field #1": "node/field1",
                                            "Name of field #2": "node/subnode1/field2",
                                            "Name of field #3": ("node/subnode1/field3", "node/subnode2/field3"),
                                        }
        ) == [
            ["row1_value1", "row1_value2", "row1_value3"],
            ["row2_value1", "row2_value2", "row2_value3"],
        ]
        generate_csv(
                                        response_json,
                                        "//records[*]",
                                        {
                                            "Name of field #1": "node/field1",
                                            "Name of field #2": "node/subnode1/field2",
                                            "Name of field #3": "node/subnode2/field3",
                                        },
                                        "sample.csv"
        )
    '''

    if isinstance(root_node, (list, tuple)):
        list_of_items = root_node
    else:
        list_of_items = root_node.get(list_xpath, tuple())

    if save_to:
        out_filehandler = open(save_to, 'wt')

    csv_table = []
    if list_of_items:
        if mapping_dict is None:
            if isinstance(list_of_items[0], list):
                header = [str(i) for i in range(0,len(list_of_items[0]))]
            elif isinstance(list_of_items[0], dict):
                header = list(list_of_items[0].keys())
            mapping_dict = {column_name: column_name for column_name in header}
        else:
            header = list(mapping_dict.keys())

        if save_to and show_header:
            out_filehandler.write(generate_comlex_csv_row(header, separator))

        for found_item in list_of_items:  # found_item == row in case of CSV list or item node in case of XML structure
            if isinstance(found_item, dict):
                found_item = n0struct.n0dict(found_item) # to have ability to use .first(xpath)
            elif isinstance(found_item, list):
                found_item = n0struct.n0list(found_item) # to have ability to use .first(xpath)

            csv_row = []
            for column_name in mapping_dict:
                xpaths = mapping_dict[column_name]
                if not isinstance(xpaths, (list, tuple)):
                    xpaths = [xpaths]
                for xpath in xpaths:
                    found_value = found_item.first(xpath, "")
                    if found_value:
                        break
                csv_row.append(found_value)
            csv_table.append(csv_row)

            if save_to:
                out_filehandler.write(generate_comlex_csv_row(csv_row, separator))

    if save_to:
        out_filehandler.close

    return csv_table
# ******************************************************************************
def remove_colums_in_csv(columns_to_remove: list, csv_rows: list = None, csv_schema: dict = None, are_required: bool = False):
    if all([isinstance(column_to_remove,int) for column_to_remove in columns_to_remove]) \
       and len(csv_rows) and isinstance(csv_rows[0], list):
        columns_to_remove.sort(reverse=True) # delete firstly last elements in the list


    for row_index, row in enumerate(csv_rows):
        # Remove columns in structure
        if isinstance(csv_rows[row_index], (dict, list)):
            for column_name in columns_to_remove:
                del csv_rows[row_index][column_name]
        else:
            raise TypeError(f"row #{row_index} in csv_rows should dict/list, got {type(csv_rows[row_index])}")

    if isinstance(csv_schema, dict):
        for column_name in columns_to_remove:
            csv_schema.delete(f"items/[id={column_name}]")

        csv_schema['maxItems'] = csv_schema.get('maxItems', 0) - (len__columns_to_remove:=len(columns_to_remove))
        if are_required:
            csv_schema['minItems'] = csv_schema.get('minItems', 0) - len__columns_to_remove
            if 'required' in csv_schema:
                for column_to_remove in reversed(columns_to_remove):
                    for i in range(len(csv_schema['required'])-1, -1, -1):
                        if csv_schema['required'][i] == column_to_remove:
                            del csv_schema['required'][i]
                            break
        return csv_rows, csv_schema
    else:
        return csv_rows
# ******************************************************************************
def add_colums_into_csv(additional_columns: list, csv_rows: list = None, csv_schema: dict = None, are_required: bool = False):
    for row_index, row in enumerate(csv_rows):
        for column_name in additional_columns:
            # Add additional columns into structure
            if isinstance(csv_rows[row_index], dict):
                csv_rows[row_index].update({column_name: None})
            elif isinstance(csv_rows[row_index], list):
                csv_rows[row_index].append([None]*len(additional_columns))
            else:
                raise TypeError(f"row #{row_index} in csv_rows should dict/list, got {type(csv_rows[row_index])}")

    if isinstance(csv_schema, dict):
        for column_name in additional_columns:
            # Update schema: Add additional columns
            csv_schema['items'].append({'id': column_name})

        csv_schema['maxItems'] = csv_schema.get('maxItems', 0) + (len__additional_columns:=len(additional_columns))
        if are_required:
            csv_schema['minItems'] = csv_schema.get('minItems', 0) + len__additional_columns
            if 'required' not in csv_schema:
                csv_schema['required'] = []
            csv_schema['required'].extend(additional_columns)

        return csv_rows, csv_schema
    else:
        return csv_rows
# ******************************************************************************
def validate_csv_row(row: typing.Union[list, dict], csv_schema: dict,
    external_variables = {},
    interrupt_after_first_fail: bool = False,
):
    '''
    row:
        list: [column_value[0], column_value[1], ... column_value[i]]
        dict: {column_name[0]: column_value[0], column_name[1]: column_value[1], ... column_name[i]: column_value[i]}
    csv_schema: dict
        //items[0..i]/id                     = column_name[i]
        //items[0..i]/mandatory              = true|false
        //items[0..i]/validations[0..j@i][0] = mandatory str, which could be processed with eval("lambda column_value, row:" + validations[0..j@i][0]),
                                               for example: "column_value == __params__['ORG']"
                                               in the lambda function body could be used variables:
                                                    column_value
                                                    row[column_name[0..i]]
                                                    global variables
        //items[0..i]/validations[0..j@i][1] = optional f-str, message in case of validations[0..j@i][0] returned False,
                                               for example: "expected '{ORG}', but got '{value_ORG}'"
                                               in the failed message body could be used variables:
                                                    external_variables.keys()
                                                    value_{column_name[0..i]}
        //minItems                           = optional int, min of columns
        //maxItems                           = optional int, max of columns
        //required[0..k]                     = optional str, mandatory column_name[k]
    external_variables: dict
        List of variables with names external_variables.keys() used in failed validation messages (f-str)
        For example __params__ as {
            'ORG': "123",
            'BIN': "456789"
        } could be used to exchange f-str placeholders {ORG} and {BIN}
    '''
    if isinstance(row, list):
        row = {column_index: column_value for column_index, column_value in enumerate(row)}
    elif not isinstance(row, dict):
        raise TypeError(f"Incoming agrument 'row' must be list or dict, but received {type(row)} '{row}'")

    the_whole_row_related_validations = None
    failed_validations = {the_whole_row_related_validations: []}
    columns_count = len(row)
    if (min_items:=csv_schema.get("minItems")) and columns_count < min_items:
        failed_validations[the_whole_row_related_validations].append(f"Mimimum {min_items} columns expected, but got {columns_count}")
    if (max_items:=csv_schema.get("maxItems")) and columns_count > max_items:
        failed_validations[the_whole_row_related_validations].append(f"Maximum {max_items} columns expected, but got {columns_count}")
    if (required_columns:=csv_schema.get("required")):
        for required_column in required_columns:
            if required_column not in row:
                failed_validations[the_whole_row_related_validations].append(f"Required column '{required_column}' doesn't exist in row")
    if not failed_validations[the_whole_row_related_validations]:
        del failed_validations[the_whole_row_related_validations]
    elif interrupt_after_first_fail:
        return failed_validations

    mapped_values = {**external_variables, **{f'value_{column_name}': row[column_name] for column_name in row}}

    for column_name in row:
        column_value = row[column_name]
        column_schema = csv_schema.first(f"items/[id={column_name}]")

        if column_schema.get('mandatory', False) and not column_value:
            failed_validations.update({column_name: f"mandatory column '{column_name}' is empty"})
            continue

        for validation in column_schema.get('validations', ()):
            validation_msg = None
            if isinstance(validation, (list,tuple)):
                validation_lambda = validation[0]
                if len(validation) >= 2:
                    validation_msg = validation[1]
            else:
                validation_lambda = validation

            try:
                lambda_function_for_validation = eval("lambda column_value, row: " + validation_lambda)
            except Exception as ex1:
                n0error(f"{validation_lambda=}")
                n0error(f"{ex1=}")

            try:
                validation_result = lambda_function_for_validation(column_value, row)
            except Exception as ex2:
                set_debug_show_object_type(True)
                n0debug("external_variables")
                n0error(f"{validation_lambda=}")
                n0error(f"{ex2=}")

            if not validation_result:
                if column_name not in failed_validations:
                    failed_validations.update({column_name: []})

                try:
                    failed_validation_message = validation_msg.format(**mapped_values)
                except:
                    failed_validation_message = "not passed validation"
                failed_validations[column_name].append(failed_validation_message)
                if interrupt_after_first_fail:
                    return failed_validations

    return failed_validations
# ******************************************************************************
# ******************************************************************************
