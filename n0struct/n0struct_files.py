import typing
# import n0struct
# ******************************************************************************
# ******************************************************************************
def load_file(file_name: str) -> list:
    with open(file_name, 'rt') as inFile:
        return [line.strip() for line in inFile.read().split("\n") if line.strip()]
# ******************************************************************************
def save_file(file_name: str, lines: typing.Any):
    if isinstance(lines, (list, tuple)):
        buffer = "\n".join(lines)
    elif isinstance(lines, (str)):
        buffer = lines
    else:
        buffer = str(lines)
    with open(file_name, 'wt') as outFile:
        outFile.write(buffer)
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
