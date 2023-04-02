import typing
from pathlib import Path
from .n0struct_n0list_n0dict import n0dict
from .n0struct_n0list_n0dict import n0list
# ******************************************************************************
# ******************************************************************************
def parse_complex_csv_line(
    line:str,
    delimiter:str = ',',
    process_field:callable = lambda field_value: field_value,  # possible to field_value.strip()
    EOL:str = '\n',
) -> list:
    fields_in_the_row = []
    flag_quotes_in_the_begining = flag_expect_delimiter_or_quotes = False
    field_value = ""
    for offset,ch in enumerate(line.strip(EOL)):
        if ch == delimiter and (flag_quotes_in_the_begining == False or flag_expect_delimiter_or_quotes == True):
            # The next field is started
            fields_in_the_row.append(process_field(field_value))
            flag_quotes_in_the_begining = flag_expect_delimiter_or_quotes = False
            field_value = ""
            continue  # skip delimiter
        elif ch == '"':
            if len(field_value) == 0:
                flag_quotes_in_the_begining = True
                continue  # skip " in the begining of the field
            elif flag_quotes_in_the_begining:
                flag_expect_delimiter_or_quotes = not flag_expect_delimiter_or_quotes # Switch flag_expect_delimiter_or_quotes
                if flag_expect_delimiter_or_quotes == True:
                    # previously flag_expect_delimiter_or_quotes == False, so skip first " in the middle of line
                    continue
                # Got the second ", so save it
                # previously flag_expect_delimiter_or_quotes == True, so save the second "
        elif flag_expect_delimiter_or_quotes:
            raise ValueError(f"Expected delimiter '{delimiter}' or second '\"', but received '{ch}' in offset {offset} of '{line}'")
        field_value += ch
    fields_in_the_row.append(process_field(field_value)) # Save the last field
    return fields_in_the_row
# ******************************************************************************
def load_csv(
    file_name: str,
    column_names: list = None,
    delimiter: str = ',',
    process_field: typing.Union[callable, None] = None,
    EOL: str = '\n',
    contains_header: typing.Union[bool,str] = False,
    process_line: typing.Union[callable, None] = None,
    skip_empty_lines: bool = True,
    strip_line: typing.Union[bool,callable] = False,
    strip_field: typing.Union[bool,callable] = False,
    return_always_list: bool = False,
    return_original_line: bool = False,
    parse_csv_line: callable = parse_complex_csv_line,
    encoding: str = "utf-8",
) -> typing.Generator:  # list, typing.Tuple[list, str], dict, typing.Tuple[dict, str]

    if column_names and len(column_names) != len(set(column_names)):
        raise KeyError(f"Column names {column_names} contains not unique names of columns")

    if not callable(process_field):
        if isinstance(strip_field, bool) and strip_field == True:
            process_field = lambda field_value: field_value.strip()
        elif callable(strip_field):
            process_field = strip_field
        else:
            process_field = lambda field_value: field_value

    if not callable(process_line):
        if isinstance(strip_line, bool) and strip_line == True:
            process_line = lambda field_value: field_value.strip()
        elif callable(strip_line):
            process_line = strip_line
        else:
            process_line = lambda line: line

    if not isinstance(contains_header, (str, bool)):
        raise ValueError(f"Not expectable value in {contains_header=}. Should be bool or str")

    if not process_line:
        process_line = lambda line_value: line_value
    elif isinstance(process_line, bool) and process_line == True:
        process_line = lambda line_value: line_value.strip()

    with open(file_name, 'rt', encoding=encoding) as in_file:
        if contains_header:
            while True:  # skip empty lines at the begining of the file
                file_offset = in_file.tell()
                line = in_file.readline()  # removed walrus operator for compatibility with 3.7
                if not line:
                    return [] # Empty file or file only with spaces
                header_line = process_line(line.rstrip(EOL))
                if header_line:
                    break
            possible_column_names = parse_csv_line(header_line, delimiter, process_field)
            if isinstance(contains_header, str):
                # if contains_header is not boolean, then first line could be header or not
                # to check if the first line is header, check value of first column
                # if it's like expected, then the first line is header
                if possible_column_names[0] != contains_header:
                    in_file.seek(file_offset) # first line is NOT header, re-read first line as data line
                    possible_column_names = None
            else:
                if column_names:
                    if isinstance(contains_header, bool):
                        if set(possible_column_names) != set(column_names):
                            raise KeyError(f"Expected column names {column_names}, but read {possible_column_names}")
                else:
                    if possible_column_names:
                        # Only in case of
                        #   contains_header = "first column name",
                        #   first line contains the header
                        #   column_names = None
                        column_names = possible_column_names

        while True:
            line = in_file.readline()  # removed walrus operator for compatibility with 3.7
            if not line:
                return None  # EOF
            stripped_line = process_line(line.rstrip(EOL))
            if skip_empty_lines and not stripped_line:
                continue
            field_values = parse_csv_line(stripped_line, delimiter, process_field, EOL)
            if not column_names or return_always_list:
                if return_original_line:
                    yield field_values, stripped_line
                else:
                    yield field_values
            else:
                if return_original_line:
                    yield n0dict(zip(column_names, field_values)), stripped_line
                else:
                    yield n0dict(zip(column_names, field_values))
# ******************************************************************************
load_complex_csv = load_csv  # Synonym
# ******************************************************************************
def load_simple_csv(
    file_name: str,
    column_names: list = None,
    delimiter: str = ',',
    process_field: typing.Union[callable, None] = None,
    EOL: str = '\n',
    contains_header: typing.Union[bool,str] = False,
    process_line: typing.Union[callable, None] = None,
    skip_empty_lines: bool = True,
    strip_line: typing.Union[bool,callable] = False,
    strip_field: typing.Union[bool,callable] = False,
    return_always_list: bool = False,
    return_original_line: bool = False,
) -> typing.Generator:  # list, typing.Tuple[list, str], dict, typing.Tuple[dict, str]
    return load_csv(
        file_name               = file_name,
        column_names            = column_names,
        delimiter               = delimiter,
        process_field           = process_field,
        EOL                     = EOL,
        contains_header         = contains_header,
        process_line            = process_line,
        skip_empty_lines        = skip_empty_lines,
        strip_line              = strip_line,
        strip_field             = strip_field,
        return_always_list      = return_always_list,
        return_original_line    = return_original_line,
        parse_csv_line          = lambda line, delimiter, process_field: [process_field(field_value) for field_value in line.split(delimiter)],
    )
# ******************************************************************************
def generate_comlex_csv_row(
    row:list,
    delimiter:str = ',',
    EOL:str = '\n',
) -> str:
    generated_csv_row = ""
    for field_value in row:
        if field_value is None:
            field_value = ""
        elif not isinstance(field_value, str):
            field_value = str(field_value)
        if delimiter in field_value or field_value.startswith('"'):
            if '"' in field_value:
                field_value = field_value.replace('"', '""')
            field_value = '"' + field_value + '"'
        generated_csv_row += field_value + delimiter
    return generated_csv_row[:-len(delimiter)] + EOL
# ******************************************************************************
def generate_csv(
    root_node:dict,
    list_xpath:str,
    mapping_dict:dict = None,
    save_to:str = None,
    delimiter:str = ',',
    show_header:bool = True
) -> list:
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
            out_filehandler.write(generate_comlex_csv_row(header, delimiter))

        for found_item in list_of_items:  # found_item == row in case of CSV list or item node in case of XML structure
            if isinstance(found_item, dict):
                found_item = n0dict(found_item) # to have ability to use .first(xpath)
            elif isinstance(found_item, list):
                found_item = n0list(found_item) # to have ability to use .first(xpath)

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
                out_filehandler.write(generate_comlex_csv_row(csv_row, delimiter))

    if save_to:
        out_filehandler.close

    return csv_table
# ******************************************************************************
def remove_colums_in_csv(
    columns_to_remove: list,
    csv_rows: list = None,
    csv_schema: dict = None,
    are_required: bool = False
):
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

        len__columns_to_remove = len(columns_to_remove)  # removed walrus operator for compatibility with 3.7
        csv_schema['maxItems'] = csv_schema.get('maxItems', 0) - len__columns_to_remove
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

        len__additional_columns = len(additional_columns)  # removed walrus operator for compatibility with 3.7
        csv_schema['maxItems'] = csv_schema.get('maxItems', 0) + len__additional_columns
        if are_required:
            csv_schema['minItems'] = csv_schema.get('minItems', 0) + len__additional_columns
            if 'required' not in csv_schema:
                csv_schema['required'] = []
            csv_schema['required'].extend(additional_columns)

        return csv_rows, csv_schema
    else:
        return csv_rows
# ******************************************************************************
def validate_csv_row(
    row: typing.Union[list, dict],
    csv_schema: dict,
    external_variables = {},
    interrupt_after_first_fail: bool = False,
):
    '''
    row:
        list: [field_value[0], field_value[1], ... field_value[i]]
        dict: {column_name[0]: field_value[0], column_name[1]: field_value[1], ... column_name[i]: field_value[i]}
    csv_schema: dict
        //items[0..i]/id                     = column_name[i]
        //items[0..i]/mandatory              = true|false
        //items[0..i]/validations[0..j@i][0] = mandatory str, which could be processed with eval("lambda field_value, row:" + validations[0..j@i][0]),
                                               for example: "field_value == {ORG}"
                                               in the lambda function body could be used variables:
                                                    field_value
                                                    row[column_name[0..i]]
                                                    external_variables
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
        row = {column_index: field_value for column_index, field_value in enumerate(row)}
    elif not isinstance(row, dict):
        raise TypeError(f"Incoming agrument 'row' must be list or dict, but received {type(row)} '{row}'")

    the_whole_row_related_validations = None
    failed_validations = {the_whole_row_related_validations: []}
    columns_count = len(row)
    min_items = int(csv_schema.get("minItems", -1))     # removed walrus operator for compatibility with 3.7
    if columns_count < min_items:
        failed_validations[the_whole_row_related_validations].append(f"Mimimum {min_items} columns expected, but got {columns_count}")
    max_items = int(csv_schema.get("maxItems", 9999))   # removed walrus operator for compatibility with 3.7
    if columns_count > max_items:
        failed_validations[the_whole_row_related_validations].append(f"Maximum {max_items} columns expected, but got {columns_count}")
        
    required_columns = csv_schema.get("required")       # removed walrus operator for compatibility with 3.7
    if required_columns and isinstance(required_columns, (list, tuple)):
        for required_column in required_columns:
            if required_column not in row:
                failed_validations[the_whole_row_related_validations].append(f"Required column '{required_column}' doesn't exist in row")
    if not failed_validations[the_whole_row_related_validations]:
        del failed_validations[the_whole_row_related_validations]
    elif interrupt_after_first_fail:
        return failed_validations

    mapped_values = {**external_variables, **{f'value_{column_name}': row[column_name] for column_name in row}}

    for column_name in row:
        field_value = row[column_name]
        column_schema = csv_schema.first(f"items/[id={column_name}]")
        mapped_values.update({
            'column_name': column_name,
            'column_value': field_value,  # Legacy
            'field_value': field_value,
            'column_schema': column_schema,
        })

        if column_schema.get('mandatory', False) and not field_value:
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

            is_valid = False
            try:
                lambda_function_for_validation = eval("lambda field_value, row: " + validation_lambda.format(**mapped_values))
            except Exception as ex1:
                validation_msg = f"Not passed validation #1 for '{column_name}': " + str(ex1)
            else:
                try:
                    is_valid = lambda_function_for_validation(field_value, row)
                except Exception as ex2:
                    validation_msg = f"Not passed validation #2 for '{column_name}': " + str(ex2)
                    
            if is_valid == False:
                if column_name not in failed_validations:
                    failed_validations.update({column_name: []})

                try:
                    failed_validation_message = validation_msg.format(**mapped_values)
                except Exception as ex3:
                    failed_validation_message = f"Not passed validation #3 for '{column_name}': " + str(ex3)

                failed_validations[column_name].append(failed_validation_message)
                if interrupt_after_first_fail:
                    break

    return failed_validations
# ******************************************************************************
# ******************************************************************************
