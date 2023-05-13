import typing
from pathlib import Path
from .n0struct_n0list_n0dict import n0dict
from .n0struct_n0list_n0dict import n0list
from n0struct import * # required to use external functions in validate_csv_row()
# ******************************************************************************
# ******************************************************************************
def parse_complex_csv_line(
    line: str,
    delimiter: str = ',',
    process_field: callable = lambda field_value: field_value,  # possible to field_value.strip()
    EOL: str = '\n',
) -> list:
    fields_in_the_row = []
    flag_quotes_in_the_begining = flag_expect_delimiter_or_quotes = False
    field_value = ""
    for offset, ch in enumerate(line.strip(EOL)):
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
    column_names: typing.Union[list, tuple, None] = None,
    delimiter: str = ',',
    process_field: typing.Union[callable, None] = None,
    # process_field == None
    #   strip_field == False                    lambda field_value: field_value
    #   strip_field == True                     lambda field_value: field_value.strip()
    EOL: str = '\n',
    contains_header: typing.Union[bool, str, list, tuple, None] = None,
    # contains_header == True || False          ***LEGACY***
    #   header_is_mandatory == None             Copy value from contains_header into header_is_mandatory
    #   header_is_mandatory != contains_header  Exception
    #
    # contains_header == "???"
    #   contains_header == row[0]
    #       column_names == []                  First row is header: column_names as is
    #       column_names == None                First row is header: column_names = row
    #   contains_header != row[0]
    #       header_is_mandatory == False        First row is data
    #       header_is_mandatory == True         Exception
    #
    # contains_header == []
    #   all(contains_header[i] in row)
    #       column_names == []                  First row is header: column_names as is
    #       column_names == None                First row is header: column_names = row
    #   any(contains_header[i] not in row)
    #       header_is_mandatory == False        First row is data
    #       header_is_mandatory == True         Exception
    #
    # contains_header == None
    #   column_names == []
    #       all(column_names[i] in row)         First row is header: column_names as is
    #       any(column_names[i] not in row)
    #           header_is_mandatory == True     Exception
    #           header_is_mandatory == False    First row is data
    #   column_names == None
    #       header_is_mandatory == True         First row is header: column_names = row
    #       header_is_mandatory == False        First row is data
    process_line: typing.Union[callable, bool, None] = None,
    # process_line == None
    #   strip_line == False                 line_value: line_value.strip()
    #   strip_line == True                  line_value: line_value
    skip_empty_lines: bool = True,
    strip_line: typing.Union[bool, callable] = False,
    strip_field: typing.Union[bool, callable] = False,
    return_original_line: bool = False,
    # return_original_line == False         Return list/dict of fields
    # return_original_line == True          Return tuple(list/dict of fields, read line)
    parse_csv_line: callable = parse_complex_csv_line,
    encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
    read_mode: str = "t",
    header_is_mandatory: typing.Union[bool, None] = None,
    # header_is_mandatory == None
    #   contains_header == True || False    Copy value from contains_header in header_is_mandatory
    #   contains_header == None             header_is_mandatory = False
    # header_is_mandatory == False          The first row is header or data row, depends of contains_header/column_names
    # header_is_mandatory == True
    #   contains_header == None
    #       column_names == None            Exception
    #       column_names == []              All column names from column_names are mandatory
    #   contains_header == []               All column names from contains_header are mandatory
    #       column_names == None            The first row is header, column_names = first row
    #       column_names == []              The first row is header
) -> typing.Generator:
    # dict                                  dict of fields got from current read line
    # typing.Tuple[dict, str]               dict of fields got from current read line, current read line

    ## header_is_mandatory
    if header_is_mandatory is None:
        header_is_mandatory = False
    elif not isinstance(header_is_mandatory, bool):
        raise SyntaxError(f"Not expectable value in {header_is_mandatory=}. Should be bool or None")

    ## column_names
    if isinstance(column_names, (list, tuple)):
        if not column_names:
            column_names = None
        else:
            if len(column_names) != len(set(column_names)):
                raise SyntaxError(f"Column names {column_names} contains not unique names of columns")
            elif contains_header:
                if isinstance(contains_header, str) and column_names[0] != contains_header:
                    raise SyntaxError(f"Column names {column_names} contains not unique names of columns")
                elif isinstance(contains_header, (list, tuple)) \
                     and any(mandatory_column_name not in column_names for mandatory_column_name in contains_header):
                    raise SyntaxError(f"Mandatory column names {contains_header} are not in expected column names {column_names}")
    elif column_names is not None:
        raise SyntaxError(f"Not expectable value in {column_names=}. Should be list/tuple/None")

    ## contains_header
    if isinstance(contains_header, (str, list, tuple)) and not contains_header:
        contains_header = None
    if isinstance(contains_header, bool):
        ## LEGACY
        if header_is_mandatory is None:
            header_is_mandatory = contains_header
        elif isinstance(header_is_mandatory, bool):
            if header_is_mandatory != contains_header:
                raise SyntaxError(f"{contains_header=} must be equal {header_is_mandatory=} if it's bool")
        contains_header = column_names
    elif isinstance(contains_header, (list, tuple)):
        if len(contains_header) != len(set(contains_header)):
            raise SyntaxError(f"Column names {contains_header} contains not unique names of columns")
    elif contains_header is None:
        contains_header = column_names
    elif not isinstance(contains_header, str):
        raise SyntaxError(f"Not expectable type of {type(contains_header)} {contains_header=}."
                         " Should be str (first column name) or list/tuple (mandatory column names) or bool (LEGACY) or None"
        )


    ## process_field
    if not callable(process_field):
        if isinstance(strip_field, bool) and strip_field == True:
            process_field = lambda field_value: field_value.strip()
        elif callable(strip_field):
            process_field = strip_field
        else:
            process_field = lambda field_value: field_value

    ## process_line
    if not callable(process_line):
        if isinstance(strip_line, bool) and strip_line == True:
            process_line = lambda line_value: line_value.strip()
        elif callable(strip_line):
            process_line = strip_line
        else:
            process_line = lambda line_value: line_value


    with open(file_name, mode='r'+read_mode, encoding=encoding) as in_file:
        # skip empty lines at the begining of the file
        while True:
            file_offset = in_file.tell()
            line = in_file.readline()  # removed walrus operator for compatibility with 3.7
            if not line:
                raise EOFError("Empty file or file only with spaces")
            header_line = process_line(line.rstrip(EOL))
            if header_line:
                break

        possible_column_names = parse_csv_line(header_line, delimiter, process_field)

        first_line_is_header = False
        if contains_header:
            if isinstance(contains_header, str):
                if possible_column_names[0] != contains_header:
                    if header_is_mandatory:
                        raise ReferenceError(f"First line is not header {possible_column_names}. Expected first column '{contains_header}'")
                else:
                    first_line_is_header = True
            elif isinstance(contains_header, (list, tuple)):
                if any(mandatory_column_name not in possible_column_names for mandatory_column_name in contains_header):
                    if header_is_mandatory:
                        raise ReferenceError(f"First line is not header {possible_column_names}. Expected {contains_header}")
                else:
                    first_line_is_header = True
        else:
            if header_is_mandatory and not column_names:
                first_line_is_header = True

        if not first_line_is_header:
            in_file.seek(file_offset) # first line is NOT header, re-read first line as data line
            if column_names:
                possible_column_names = column_names
            else:
                column_names = possible_column_names = [i for i in range(len(possible_column_names))]
        else:
            if header_is_mandatory and len(possible_column_names) != len(set(possible_column_names)):
                raise KeyError(f"Read header {possible_column_names} contains not unique names of columns")
            if not column_names:
                column_names = possible_column_names
        len_possible_column_names = len(possible_column_names)

        while True:
            line = in_file.readline()  # removed walrus operator for compatibility with 3.7
            if not line:
                return None  # EOF
            stripped_line = process_line(line.rstrip(EOL))
            if skip_empty_lines and not stripped_line:
                continue

            # removed walrus operator for compatibility with 3.7
            list_field_values = parse_csv_line(stripped_line, delimiter, process_field, EOL)
            dict_field_values = n0dict( zip(
                                    possible_column_names,
                                    list_field_values
                                    + ([None] * (len_possible_column_names - len(list_field_values)))
            ))
            if column_names != possible_column_names:
                dict_field_values = n0dict({
                    key: dict_field_values[key]
                    for key in column_names
                })
            if return_original_line:
                yield dict_field_values, stripped_line
            else:
                yield dict_field_values
# ******************************************************************************
load_complex_csv = load_csv  # Synonym
# ******************************************************************************
def load_simple_csv(
    file_name: str,
    column_names: typing.Union[list, tuple, None] = None,
    delimiter: str = ',',
    process_field: typing.Union[callable, None] = None,
    EOL: str = '\n',
    contains_header: typing.Union[bool, str, list, tuple, None] = None,
    process_line: typing.Union[callable, bool, None] = None,
    skip_empty_lines: bool = True,
    strip_line: typing.Union[bool, callable] = False,
    strip_field: typing.Union[bool, callable] = False,
    return_original_line: bool = False,
    parse_csv_line: callable = lambda line, delimiter, process_field: [process_field(field_value) for field_value in line.split(delimiter)],
    encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
    read_mode: str = "t",
    header_is_mandatory: typing.Union[bool, None] = None,
) -> typing.Generator:
    # dict                                  dict of fields got from current read line
    # typing.Tuple[dict, str]               dict of fields got from current read line, current read line
    return load_csv(
        file_name            = file_name,
        column_names         = column_names,
        delimiter            = delimiter,
        process_field        = process_field,
        EOL                  = EOL,
        contains_header      = contains_header,
        process_line         = process_line,
        skip_empty_lines     = skip_empty_lines,
        strip_line           = strip_line,
        strip_field          = strip_field,
        return_original_line = return_original_line,
        parse_csv_line       = parse_csv_line,
        encoding             = encoding,
        read_mode            = read_mode,
        header_is_mandatory  = header_is_mandatory,
    )
# ******************************************************************************
def generate_comlex_csv_row(
    row: list,
    delimiter: str = ',',
    EOL: str = '\n',
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
    root_node: dict,
    list_xpath: str,
    mapping_dict: dict = None,
    save_to: str = None,
    delimiter: str = ',',
    show_header: bool = True
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
                header = [str(i) for i in range(0, len(list_of_items[0]))]
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
    if all([isinstance(column_to_remove, int) for column_to_remove in columns_to_remove]) \
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
    row_i: int = None,
    rows_count: int = 0,
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

    row_last = rows_count - 1
    for column_name in row:
        field_value = row[column_name]
        column_schema = csv_schema.first(f"items/[id={column_name}]")
        mapped_values.update({  # Used in validation_lambda/validation_msg
            'column_name': column_name,
            'column_value': field_value,  # Legacy
            'field_value': field_value,
            'column_schema': column_schema,
            'row_i': row_i,
            'rows_count': rows_count,
            'row_last': row_last,
        })

        if column_schema.get('mandatory', False) and not field_value:
            failed_validations.update({column_name: f"mandatory column '{column_name}' is empty"})
            continue

        for validation in column_schema.get('validations', ()):
            validation_msg = None
            if isinstance(validation, (list, tuple)):
                validation_lambda = validation[0]
                if len(validation) >= 2:
                    validation_msg = validation[1]
            else:
                validation_lambda = validation

            is_valid = False
            try:
                lambda_function_for_validation = eval(
                    "lambda column_name, field_value, row, row_i, row_last: " + validation_lambda.format(**mapped_values)
                )
            except Exception as ex1:
                validation_msg = f"Not passed validation #1 for '{column_name}': " + str(ex1)
            else:
                try:
                    is_valid = lambda_function_for_validation(column_name, field_value, row, row_i, row_last)
                except Exception as ex2:
                    validation_msg = f"Not passed validation #2 for '{column_name}': " + str(ex2)

            if not is_valid:
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
