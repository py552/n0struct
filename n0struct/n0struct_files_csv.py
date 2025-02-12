import types
import os
import typing
from pathlib import Path
import csv
from .n0struct_n0list_n0dict import n0dict
from .n0struct_n0list_n0dict import n0list

# required to use external functions in validate_csv_row()
from . import *
import re

from .n0struct_date import *
from .n0struct_utils import *

# ******************************************************************************
# ******************************************************************************
def parse_complex_csv_line(
    line: typing.Union[str, bytes],
    delimiter: typing.Union[str, bytes] = ',',
    process_field: callable = lambda field_value: field_value,  # possible to field_value.strip()
    EOL: typing.Any = None,  # Left for back compatibility
) -> list:
    if isinstance(line, str):
        CRLF = '\r\n'
        empty_field_value = ''
        if isinstance(delimiter, bytes):
            delimiter = delimiter.decode("utf-8-sig")
    else:
        CRLF = b'\r\n'
        empty_field_value = b''
        if isinstance(delimiter, str):
            delimiter = delimiter.encode("utf-8")

    field_value = empty_field_value
    fields_in_the_row = []
    flag_quotes_in_the_begining = flag_expect_delimiter_or_quotes = False

    for offset, ch in enumerate(line.rstrip(CRLF)):
        if isinstance(ch, int):  # if line is bytes, each fetched item will be int
            ch = ch.to_bytes(1, "big") # for compatibility with 3.7
        if ch == delimiter and (flag_quotes_in_the_begining == False or flag_expect_delimiter_or_quotes == True):
            # The next field is started
            fields_in_the_row.append(process_field(field_value))
            flag_quotes_in_the_begining = flag_expect_delimiter_or_quotes = False
            field_value = empty_field_value
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
    file_path: str,
    column_names: typing.Union[list, tuple, None] = None,
    delimiter: str = ',',
    process_field: typing.Union[callable, None] = None,
    # process_field == None
    #   strip_field == False                    lambda field_value: field_value
    #   strip_field == True                     lambda field_value: field_value.strip()
    EOL: typing.Any = None,                     # Left for back compatibility
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
    return_unknown_fields: bool = False,
    raise_exception: bool = True,
) -> typing.Generator:
    # dict                                  dict of fields got from current read line
    # typing.Tuple[dict, str]               dict of fields got from current read line, current read line

    ## header_is_mandatory
    if header_is_mandatory is None:
        header_is_mandatory = False
    elif not isinstance(header_is_mandatory, bool):
        raise SyntaxError(f"Not expectable value in header_is_mandatory='{header_is_mandatory}'. Should be bool or None")

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
        raise SyntaxError(f"Not expectable value in column_names='{column_names}'. Should be list/tuple/None")

    ## contains_header
    if isinstance(contains_header, (str, list, tuple)) and not contains_header:
        contains_header = None
    if isinstance(contains_header, bool):
        ## LEGACY
        if header_is_mandatory is None:
            header_is_mandatory = contains_header
        elif isinstance(header_is_mandatory, bool):
            if header_is_mandatory != contains_header:
                raise SyntaxError(f"contains_header='{contains_header}' must be equal header_is_mandatory='{header_is_mandatory}' if it's bool")
        contains_header = column_names
    elif isinstance(contains_header, (list, tuple)):
        if len(contains_header) != len(set(contains_header)):
            raise SyntaxError(f"Column names {contains_header} contains not unique names of columns")
    elif contains_header is None:
        contains_header = column_names
    elif not isinstance(contains_header, str):
        raise SyntaxError(f"Not expectable type of {type(contains_header)} contains_header='{contains_header}'."
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

    if read_mode == 't':
        CRLF = '\r\n'
    else:
        CRLF = b'\r\n'

    with open(
        file_path,
        mode='r'+read_mode,
        encoding=encoding if read_mode == 't' else None
    ) as in_file:
        ########################################################################
        # skip empty lines at the begining of the file
        ########################################################################
        # FIXME: .readline() doesn't support \r in binary and \n\r in binary and text read modes
        while True:
            file_offset = in_file.tell()
            line = in_file.readline()  # removed walrus operator for compatibility with 3.7
            if not line:
                raise EOFError("Empty file or file only with spaces")
            header_line = process_line(line.rstrip(CRLF))
            if header_line:
                break

        ########################################################################
        # determine if the first row is header
        ########################################################################
        first_line_column_names = parse_csv_line(header_line, delimiter, process_field)
        first_line_is_header = False
        if contains_header:
            if isinstance(contains_header, str):
                if first_line_column_names[0] != contains_header:
                    if header_is_mandatory:
                        if raise_exception:
                            raise ReferenceError(f"First line is not the header: expected column names {tuple(contains_header)}, received {tuple(first_line_column_names)}. First column name '{first_line_column_names[0]}' is not equal to expected '{contains_header}'")
                        else:
                            return tuple()
                else:
                    first_line_is_header = True
            elif isinstance(contains_header, (list, tuple)):
                mandatory_column_name_does_not_exist = next((mandatory_column_name for mandatory_column_name in contains_header if mandatory_column_name not in first_line_column_names), None)
                if mandatory_column_name_does_not_exist:
                    if header_is_mandatory:
                        if raise_exception:
                            raise ReferenceError(f"First line is not the header: expected column names {tuple(contains_header)}, received {tuple(first_line_column_names)}. '{mandatory_column_name_does_not_exist}' doesn't exist.")
                        else:
                            return tuple()
                else:
                    first_line_is_header = True
        else:
            if header_is_mandatory and not column_names:
                first_line_is_header = True

        if not first_line_is_header:
            in_file.seek(file_offset) # first line is NOT header, re-read first line as data line
            if column_names:
                first_line_column_names = column_names
            else:
                column_names = first_line_column_names = [i for i in range(len(first_line_column_names))]
        else:
            if header_is_mandatory and len(first_line_column_names) != len(set(first_line_column_names)):
                raise KeyError(f"Read header {first_line_column_names} contains not unique names of columns")
            if not column_names:
                column_names = first_line_column_names
        len_first_line_column_names = len(first_line_column_names)

        ########################################################################
        # own realization for binary support, sorting of columns, removing redundant columns and etc.
        ########################################################################
        while True:
            line = in_file.readline()  # removed walrus operator for compatibility with 3.7
            if not line:
                return None  # EOF
            stripped_line = process_line(line.rstrip(CRLF))
            if skip_empty_lines and not stripped_line:
                continue

            # removed walrus operator for compatibility with 3.7
            list_field_values = parse_csv_line(stripped_line, delimiter, process_field)
            dict_field_values = n0dict( zip(
                                    first_line_column_names,
                                    list_field_values
                                    + ([None] * (len_first_line_column_names - len(list_field_values)))
            ))
            if not return_unknown_fields and column_names != first_line_column_names:
                dict_field_values = n0dict({
                    key: dict_field_values.get(key) # If optional column doesn't exist, then it will be None
                    for key in column_names
                })
            if return_original_line:
                yield dict_field_values, stripped_line
            else:
                yield dict_field_values
# ******************************************************************************
def load_native_csv(
    file_path: str,
    column_names: typing.Union[list, tuple, None] = None,
    delimiter: str = ',',
    EOL: str = '\n',  # '\n' should be universal for Linux and Windows in case of 'rt' mode
    contains_header: typing.Union[bool, None] = True,
    encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
    raise_exception: bool = True,
) -> typing.Generator:
    if column_names is not None:
        if not isinstance(column_names, (list, tuple)):
            raise SyntaxError(f"Not expectable value in column_names='{column_names}'. Should be list/tupleNone")
        elif len(column_names) != len(set(column_names)):
            raise SyntaxError(f"Column names {column_names} contains not unique names of columns")

    with open(file_path, 'rt', encoding=encoding, newline='') as in_filehandler:
        csv_reader = csv.DictReader(
            in_filehandler,
            fieldnames=column_names,
            delimiter=delimiter,
            lineterminator=EOL,
            strict=True
        )
        for i, row in enumerate(csv_reader):
            if i == 0 and contains_header:
                not_equal_column_name = next((f"name '{value}' of column #{j} is not equal to expected '{key}'" for j,(key,value) in enumerate(row.items()) if key != value), None)
                if not_equal_column_name:
                    if raise_exception:
                        raise ReferenceError(f"First line is not the header: expected column names {tuple(column_names)}, received {tuple(row.keys())}. For example: {not_equal_column_name}")
                    else:
                        return tuple()
                continue
            yield row
# ******************************************************************************
load_complex_csv = load_csv # Synonym
# ******************************************************************************
def load_simple_csv(
    file_path: str,
    column_names: typing.Union[list, tuple, None] = None,
    delimiter: str = ',',
    process_field: typing.Union[callable, None] = None,
    EOL: str = '\n',  # '\n' should be universal for Linux and Windows in case of 'rt' mode
    contains_header: typing.Union[bool, str, list, tuple, None] = None,
    process_line: typing.Union[callable, bool, None] = None,
    skip_empty_lines: bool = True,
    strip_line: typing.Union[bool, callable] = False,
    strip_field: typing.Union[bool, callable] = False,
    return_original_line: bool = False,
    parse_csv_line: callable =
        lambda
            line,
            delimiter,
            process_field:
        [
            process_field(field_value)
            for field_value in line
                .rstrip('\r\n')
                .split(delimiter)
        ]
    ,
    encoding: typing.Union[str, None] = "utf-8-sig",  # with possible UTF-8 BOM (Byte Order Mark)
    read_mode: str = 't',
    header_is_mandatory: typing.Union[bool, None] = None,
    raise_exception: bool = True,
) -> typing.Generator:
    # dict                                  dict of fields got from current read line
    # typing.Tuple[dict, str]               dict of fields got from current read line, current read line
    return load_csv(
        file_path            = file_path,
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
        raise_exception      = raise_exception,
    )
# ******************************************************************************
def generate_complex_csv_row(
    row: list,
    delimiter: str = ',',
    EOL: str = '\n',  # '\n' should be universal for Linux and Windows in case of 'wt' mode
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
def save_csv(
                file_path: str,
                rows: typing.Union[list, tuple, None],
                header: typing.Union[list, tuple, None] = None,
                # mode: str = 't', # binary is not supported by csv module
                encoding: str = "utf-8",  # without UTF-8 BOM (Byte Order Mark)
                EOL: str = '\n',  # '\n' should be universal for Linux and Windows in case of 'wt' mode
                delimiter: str = ',',
):
    if rows is None:
        return
    if not isinstance(rows, (list, tuple, types.GeneratorType)):
        raise TypeError(f"Expected rows as list or tuple or generator, but got ({type(rows)}) {rows}")
    if isinstance(rows, (list, tuple)) \
    and not isinstance(rows[0], (list, tuple)) and type(rows[0]) is not {}.values().__class__:
        raise TypeError(f"Expected rows as list/tuples of lists/tuples, but got ({type(rows[0])}) {rows[0]}")
    if header \
    and not isinstance(header, (list, tuple, types.GeneratorType)) \
    and type(header) is not {}.keys().__class__: \
        raise TypeError(f"Expected header as list or tuple, but got ({type(rows)}) {rows}")

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wt', encoding=encoding, newline='') as out_filehandler:
        csv_writer = csv.writer(
            out_filehandler,
            delimiter=delimiter,
            lineterminator=EOL,
        )
        if header:
            csv_writer.writerow(header)
        csv_writer.writerows(rows)

# ******************************************************************************
def generate_csv(
    root_node: dict,
    list_xpath: str,
    mapping_dict: dict = None,
    save_to: str = None,
    delimiter: str = ',',
    show_header: bool = True,
    EOL: str = '\n',  # '\n' should be universal for Linux and Windows in case of 'wt' mode
    encoding: str = "utf-8",  # without UTF-8 BOM (Byte Order Mark)
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

    ## if save_to:
    ##     out_filehandler = open(save_to, 'wt')

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

        ## if save_to and show_header:
        ##     out_filehandler.write(generate_complex_csv_row(header, delimiter))

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

            ## if save_to:
            ##     out_filehandler.write(generate_complex_csv_row(csv_row, delimiter))

    if save_to:
        save_csv(save_to, csv_table, header if show_header else None, delimiter=delimiter, EOL=EOL, encoding=encoding)
    ##    out_filehandler.close

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
    precompile: bool = False,
) -> tuple:  # ( validation_result: str = SKIP|NOWAIT|VALID|REJECT, failed_validations: dict = {column_name: [error message#n,...])
    '''
    row:
        list: [field_value[0], field_value[1], ... field_value[i]]
        dict: {column_name[0]: field_value[0], column_name[1]: field_value[1], ... column_name[i]: field_value[i]}
    csv_schema: dict
        //items[0..i]/id                     = column_name[i]
        //items[0..i]/mandatory              = true|false
        //items[0..i]/validations[0..j@i][0] = mandatory str, which could be processed with eval("lambda field_value, row, row_i, row_last:" + validations[0..j@i][0]),
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
        //items[0..i]/validations[0..j@i][2] = action: "SKIP", "NOWAIT", "VALID", "REJECT" (default None == "REJECT")
                                               if result of validations[0..j@i][0] == False, and  validations[0..j@i][1] == "SKIP", "NOWAIT", "REJECT",
                                               then return back validations[0..j@i][1] ("SKIP", "NOWAIT", "REJECT")
                                               if result of validations[0..j@i][0] == True, and  validations[0..j@i][1] == "VALID"
                                               then return back "REJECT"
        //items[0..i]/validations[0..j@i][3] = next: "EXIT", "BREAK", "CONTINUE" (default None == "CONTINUE")
                                               if result of validations[0..j@i][0] != "VALID"
                                               CONTINUE: go to the next validation rule for current column or next columns
                                               BREAK:    skip next validation rules for the current column, go to validation rules of the next columns
                                               EXIT:     skip validation rules for current and next columns
        //items[0..i]/validations[0..j@i][4] = precompiled validations[0..j@i][0]
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

    if not isinstance(csv_schema, n0dict):
        csv_schema = n0dict(csv_schema)

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
    validation_result = "VALID"

    row_last = rows_count - 1
    for column_schema in csv_schema.get('items'):
        column_name = column_schema['id']
        field_value = row.get(column_name, "$N0t_F0uNd$")
        if column_name != 'common_validations':
            if field_value == "$N0t_F0uNd$":
                if column_schema.get('mandatory'):
                    validation_result = "REJECT"
                    failed_validations.update({column_name: f"mandatory field '{column_name}' doesn't exist"})
                continue # ALL validations will be skipped without error message mandatory==False and field doesn't exist
            elif not field_value:
                if column_schema.get('mandatory'):
                    validation_result = "REJECT"
                    failed_validations.update({column_name: f"mandatory field '{column_name}' is empty"})
                continue # ALL validations will be skipped without error message mandatory==False and field is empty/None

        mapped_values.update({  # Used in validation_lambda/validation_msg
            'column_name': column_name,
            'column_value': field_value,  # Legacy
            'field_value': field_value,
            'column_schema': column_schema,
            'row_i': row_i,
            'rows_count': rows_count,
            'row_last': row_last,
            'row': row,
        })

        for validation_i,validation in enumerate(column_schema.get('validations', ())):

            if not isinstance(validation, (list, tuple)) or len(validation) < 2:
                raise TypeError(f"Validation rule #{validation_i} for '{column_name}' is incorrect."
                                " validation is expected as list/tuple/str"
                                f", but received ({type(validation)}) '{validation}'"
                )
            if len(validation) > 2:
                validation_action = validation[2].upper()  # SKIP/NOWAIT/VALID/REJECT (default)
                validation_action = validate_values(
                    validation_action,
                    ("SKIP", "NOWAIT", "VALID", "REJECT"),
                    raise_if_not_found = Exception(f"Validation rule #{validation_i} for '{column_name}' is incorrect."
                                                   " Action is expected as SKIP or NOWAIT or VALID or REJECT"
                                                   f", but received '{validation_action}'"
                                         )
                )
            else:
                validation_action = "REJECT"
                column_schema['validations'][validation_i].append(validation_action)

            if len(validation) > 3:
                validation_next = validation[3].upper()  # EXIT/BREAK/CONTINUE (default)
                validation_next = validate_values(
                    validation_next,
                    ("EXIT", "BREAK", "CONTINUE"),
                    raise_if_not_found = Exception(f"Validation rule #{validation_i} for '{column_name}' is incorrect."
                                                   " Action is expected as EXIT, BREAK or CONTINUE"
                                                   f", but received '{validation_next}'"
                                         )
                )
            else:
                validation_next = "CONTINUE"
                column_schema['validations'][validation_i].append(validation_next)

            validation_msg = None
            if not precompile or len(validation) <= 4 or not callable(validation[4]):
                try:
                    if isinstance(validation[0], (list,tuple)):
                        validation[0] = ' '.join(validation[0])

                    # for compatibility with python 3.7
                    lambda_txt = "lambda column_name, field_value, row, row_i, row_last: " + validation[0].format(**mapped_values)
                    validation_lambda = eval(lambda_txt)
                    if len(validation) <= 4:
                        column_schema['validations'][validation_i].append(validation_lambda)
                except Exception as ex1:
                    validation_result = "REJECT"
                    validation_msg = f"Incorrect validation rule #{validation_i} for '{column_name}': " + str(ex1)
            else:
                validation_lambda = column_schema['validations'][validation_i][4]

            is_valid = False
            _result = None
            if not validation_msg:
                try:
                    _result = is_valid = validation_lambda(column_name, field_value, row, row_i, row_last)
                    if validation_action == "VALID":
                        is_valid = not is_valid
                except Exception as ex2:
                    validation_result = "REJECT"
                    validation_msg = f"Incorrect validation rule #{validation_i} for '{column_name}': " + str(ex2)

                if not validation_msg and not is_valid:
                    if validation_action == "VALID":
                        validation_result = "REJECT"
                    else:
                        validation_result = validation_action

                    try:
                        validation_msg = validation[1].format(**mapped_values, validation_result=_result)
                    except Exception as ex3:
                        validation_result = "REJECT"
                        validation_msg = f"Incorrect validation message #{validation_i} for '{column_name}': " + str(ex3)

            if validation_msg:
                if column_name not in failed_validations:
                    failed_validations.update({column_name: []})
                failed_validations[column_name].append(validation_msg)

            if validation_result != "VALID":
                if validation_next in ("BREAK", "EXIT") or (validation_result == "REJECT" and interrupt_after_first_fail):
                    break

        if validation_result != "VALID":
            if validation_next == "EXIT" or (validation_result == "REJECT" and interrupt_after_first_fail):
                break

    return validation_result, failed_validations


################################################################################
__all__ = (
    'parse_complex_csv_line',
    'load_csv',
    'load_native_csv',
    'load_simple_csv',
    'generate_complex_csv_row',
    'save_csv',
    'generate_csv',
    'remove_colums_in_csv',
    'add_colums_into_csv',
    'validate_csv_row',
    'load_complex_csv',
)
################################################################################
