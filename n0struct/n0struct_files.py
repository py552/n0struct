import typing
from pathlib import Path
# import n0struct
# ******************************************************************************
# ******************************************************************************
def load_file(file_name: str) -> list:
    with open(file_name, 'rt') as in_file:
        return [line.strip() for line in in_file.read().split("\n") if line.strip()]
# ******************************************************************************
def load_simple_csv(file_name: str, format:list = None, delimiter:str = ',', contains_header = False) -> list:
    loaded_csv = []
    with open(file_name, 'rt') as in_file:
        if contains_header:
            header_line = in_file.readline()
            column_names = header_line.rstrip('\n').split(delimiter)
            if not isinstance(contains_header, bool):
                # if contains_header is not boolean, then first line could be header or not
                # to check if the first line is header, check value of first column
                # if it's like expected, then the first line is header
                if column_names[0] != contains_header:
                    in_file.seek(0) # first line is NOT header, re-read first line as data line
                    column_names = None
            if not format:
                format = column_names

        if format and len(format) != len(set(format)):
            raise Exception(f"Format {format} contains not unique names of columns")

        for line in in_file.readlines():
            column_values = line.rstrip('\n').split(delimiter)
            if format:
                column_values = dict(zip(format, column_values))
            loaded_csv.append(column_values)
    return loaded_csv
# ******************************************************************************
def save_file(file_name: str, lines: typing.Any):
    Path(file_name).parent.mkdir(parents=True, exist_ok=True)

    if isinstance(lines, (list, tuple)):
        buffer = "\n".join(lines)
    elif isinstance(lines, str):
        buffer = lines
    else:
        buffer = str(lines)
    with open(file_name, 'wt') as out_filehandler:
        out_filehandler.write(buffer)
# ******************************************************************************
def load_ini(file_name: str, default_value = None, equal_sign = '=') -> dict:
    ini_dict = {}
    with open(file_name, 'rt') as in_filehanlder:
        for line in in_filehanlder.readlines():
            items = line.strip().split(equal_sign, 1)
            if items:
                ini_dict.update({
                                items[0].upper():   (
                                                    int(items[1])
                                                    if len(items) > 1 and items[1].isdecimal()
                                                    else default_value
                                                    )
                })
    return ini_dict
# ******************************************************************************
# def generate_csv(root_node:n0dict, list_xpath:str, mapping_dict:dict, file_path:str = None, separator:str = '|') -> list:
def generate_csv(root_node:dict, list_xpath:str, mapping_dict:dict, file_path:str = None, separator:str = '|') -> list:
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
    if file_path:
        out_filehandler = open(file_path, 'wt')
        out_filehandler.write(separator.join(list(mapping_dict.keys())) +  "\n")

    csv_table = []
    for found_node in root_node.get(list_xpath, set()):
        csv_row = []
        for key in mapping_dict:
            xpaths = mapping_dict[key]
            if not isinstance(xpaths, (list, tuple)):
                xpaths = [xpaths]
            for xpath in xpaths:
                found_value = found_node.first(xpath, "")
                if found_value:
                    break
            csv_row.append(found_value)
        csv_table.append(csv_row)

        if file_path:
            out_filehandler.write(separator.join(csv_row) +  "\n")

    if file_path:
        out_filehandler.close

    return csv_table
# ******************************************************************************
def n0eval(_str: str) -> typing.Union[int, float, typing.Any]:
    def my_split(_str: str, _separator: str) -> typing.List:
        return [
                (_separator if _separator != '+' and i else "") + itm.strip()
                for i, itm in enumerate(_str.split(_separator))
                if itm.strip()
        ]

    if not isinstance(_str, str):
        return _str

    _str = _str.replace(" ","").lower()
    if not _str:
        return _str
        # raise ValueError("Could not convert empty/null string into index")

    first_split = my_split(_str, '+')
    second_split = []
    for item in first_split:
        items = my_split(item, '-')
        second_split.extend(items)

    result = 0
    for item in second_split:
        if item == "new()":
            return _str
        if item == "last()":
            item = -1
        else:
            try:
                if '.' in item:
                    item = float(item)
                else:
                    item = int(item)
            except Exception:
                return _str
        result += item

    return result
# ******************************************************************************
def load_serialized(file_name: str,
                    # /,  # When everybody migrates to py3.8, then we will make it much beautiful
                    equal_tag: str = "=",
                    separator_tag: str = ";",
                    comment_tags: typing.Union[tuple, list] = ("#", "//"),
                    remove_startswith: str = "",
                    remove_endswith: str = ""
                    # ) -> n0struct.n0list:
                    ) -> list:

    # result = n0struct.n0list()
    result = list()

    for line in load_file(file_name):
        line = line.strip()
        if any(line.startswith(comment_tag) for comment_tag in comment_tags):
            continue
        if line.startswith(remove_startswith):
            line = line[len(remove_startswith):]
        if line.startswith(remove_startswith):
            line = line[len(remove_startswith):]

        pairs = line.split(separator_tag)
        if len(pairs):
            # result["root"].append(n0dict())
            # result.append(n0struct.n0dict())
            result.append(dict())
            for pair in pairs:
                if equal_tag in pair:
                    tag, value = pair.split(equal_tag, 1)
                    value = value.strip()
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    else:
                        value = n0eval(value)
                else:
                    tag = pair
                    value = None
                result[-1].update({tag.strip(): value})
                # result["root"][-1].update({tag.strip(): value})
    return result
# ******************************************************************************
# ******************************************************************************
