from typing import Any, Union
import json

def data_to_json(
    data: Any,
    indent: Union[int, None] = None,
    indent_size: int = 4,
    pairs_in_one_line: bool = True,
    skip_empty_arrays: bool = False,
    compress: bool = False,
    sort_keys: bool = False,
    ensure_ascii: bool = False,
    allow_nan: bool = True,
    escape_special: bool = False,
    escape_unicode: bool = False,
) -> str:
    """
    Converts data to JSON string with customizable formatting.

    Args:
        data: Data to convert to JSON
        indent: Base indentation for entire JSON (None=no base indent, int=spaces to add to all lines)
        indent_size: Indentation size for nested levels (default 4)
        pairs_in_one_line: If True, simple key-value pairs on one line
        skip_empty_arrays: If True, skips empty arrays
        compress: If True, maximally compresses JSON (ignores other formatting params)
        sort_keys: If True, sorts keys in dictionaries
        ensure_ascii: If True, escapes all non-ASCII characters
        allow_nan: If True, allows float('nan'), float('inf') and float('-inf')
        escape_special: If True, escapes special characters (\\x00-\\x1F)
        escape_unicode: If True, escapes all Unicode characters (\\uXXXX)

    Returns:
        str: JSON string
    """

    def escape_string(s):
        """Escapes string according to settings"""
        # Basic JSON escaping
        result = (
            s   .replace('\\',  '\\\\')
                .replace('\"',  '\\"')
                .replace('\b',  '\\b')
                .replace('\f',  '\\f')
                .replace('\n',  '\\n')
                .replace('\r',  '\\r')
                .replace('\t',  '\\t')
       )

        # Escape special characters (control characters)
        if escape_special:
            new_result = ""
            for char in result:
                code = ord(char)
                if 0 <= code <= 31 and char not in '\b\f\n\r\t':  # Exclude already processed
                    new_result += f"\\x{code:02x}"
                else:
                    new_result += char
            result = new_result

        # Escape Unicode characters
        if escape_unicode:
            new_result = ""
            for char in result:
                code = ord(char)
                if code > 127:  # Non-ASCII characters
                    if code > 0xFFFF:
                        # For characters outside BMP use surrogate pair
                        high = ((code - 0x10000) >> 10) + 0xD800
                        low = ((code - 0x10000) & 0x3FF) + 0xDC00
                        new_result += f"\\u{high:04x}\\u{low:04x}"
                    else:
                        new_result += f"\\u{code:04x}"
                else:
                    new_result += char
            result = new_result

        return result

    def is_simple_value(value):
        """Checks if value is simple (not dict/list or empty)"""
        if value is None or isinstance(value, (bool, int, float, str)):
            return True
        if isinstance(value, (dict, list)) and len(value) == 0:
            return True
        return False

    def is_simple_dict(obj):
        """Checks if dictionary contains only simple values"""
        if not isinstance(obj, dict):
            return False
        return all(is_simple_value(v) for v in obj.values())

    def clean_data(obj):
        """Removes empty arrays if skip_empty_arrays=True"""
        if not skip_empty_arrays:
            return obj

        if isinstance(obj, dict):
            cleaned = {}
            for k, v in obj.items():
                if isinstance(v, list) and len(v) == 0:
                    continue  # Skip empty arrays
                cleaned[k] = clean_data(v)
            return cleaned
        elif isinstance(obj, list):
            return [clean_data(item) for item in obj]
        else:
            return obj

    def format_json_custom(obj, level=0):
        """Custom JSON formatting"""
        # Level indent (for nested structures) - no base indent here
        current_indent = " " * (indent_size * level)
        next_indent = " " * (indent_size * (level + 1))

        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, (int, float)):
            # Handle special float values
            if isinstance(obj, float):
                if obj != obj:  # NaN
                    if allow_nan:
                        return "NaN"
                    else:
                        raise ValueError("NaN values are not allowed")
                elif obj == float('inf'):
                    if allow_nan:
                        return "Infinity"
                    else:
                        raise ValueError("Infinity values are not allowed")
                elif obj == float('-inf'):
                    if allow_nan:
                        return "-Infinity"
                    else:
                        raise ValueError("-Infinity values are not allowed")
            return str(obj)
        elif isinstance(obj, str):
            escaped = escape_string(obj)
            return f'"{escaped}"'
        elif isinstance(obj, list):
            if len(obj) == 0:
                return "[]"

            # If all list elements are simple and few
            if len(obj) <= 5 and all(is_simple_value(item) for item in obj):
                items = [format_json_custom(item, level) for item in obj]
                return "[" + ", ".join(items) + "]"

            # Multi-line format
            items = []
            for item in obj:
                formatted_item = format_json_custom(item, level + 1)
                items.append(next_indent + formatted_item)

            return current_indent + "[\n" + ",\n".join(items) + "\n" + current_indent + "]"

        elif isinstance(obj, dict):
            if len(obj) == 0:
                return "{}"

            # Sort keys if needed
            items_iter = sorted(obj.items()) if sort_keys else obj.items()

            # If dictionary is simple and pairs_in_one_line mode is enabled
            if pairs_in_one_line and is_simple_dict(obj):
                items = []
                for k, v in items_iter:
                    key_str = f'"{escape_string(str(k))}"'
                    value_str = format_json_custom(v, level)
                    items.append(f"{key_str}: {value_str}")
                return "{" + ", ".join(items) + "}"

            # Multi-line format
            items = []
            for k, v in items_iter:
                key_str = f'"{escape_string(str(k))}"'
                value_str = format_json_custom(v, level + 1)

                # If value is simple, can place on one line with key
                if pairs_in_one_line and is_simple_value(v):
                    items.append(f"{next_indent}{key_str}: {value_str}")
                else:
                    items.append(f"{next_indent}{key_str}: {value_str}")

            return current_indent + "{\n" + ",\n".join(items) + "\n" + current_indent + "}"

        return str(obj)

    # If compression is enabled, use standard JSON without formatting
    if compress:
        cleaned = clean_data(data)
        return json.dumps(cleaned,
                         ensure_ascii=ensure_ascii,
                         sort_keys=sort_keys,
                         allow_nan=allow_nan,
                         separators=(',', ':'))

    # Clean data from empty arrays if needed
    cleaned_data = clean_data(data)

    # Apply custom formatting
    result = format_json_custom(cleaned_data)

    # Add base indent to the result if needed and it's not already there
    if indent is not None and indent > 0:
        # Split by lines and add base indent to each line
        lines = result.split('\n')
        indented_lines = []
        for line in lines:
            if line.strip():  # Only add indent to non-empty lines
                indented_lines.append((" " * indent) + line)
            else:
                indented_lines.append(line)
        return '\n'.join(indented_lines)

    return result


# Usage examples and tests
if __name__ == "__main__":
    # Set UTF-8 encoding for output (helps with Unicode characters)
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    # Test data
    test_data = {
        "name": "Test object",
        "id": 12345,
        "active": True,
        "score": 98.5,
        "special_chars": "String with\nnewline\tand tab\x02and special char",
        "unicode_text": "Hello world! This is text with emoji",  # Removed emoji for compatibility
        "nan_value": float('nan'),
        "inf_value": float('inf'),
        "tags": ["python", "json", "formatting"],
        "empty_list": [],
        "simple_object": {
            "z_key": "last alphabetically",
            "a_key": "first alphabetically",
            "x": 10,
            "y": 20
        },
        "complex_object": {
            "nested": {
                "deep": {
                    "value": "deeply nested value"
                }
            },
            "items": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"},
                {"id": 3, "name": "Item 3"}
            ]
        },
        "metadata": {
            "created": "2024-01-01",
            "updated": "2024-01-15",
            "version": "1.0"
        }
    }

    print("=== Standard formatting (no base indent) ===")
    print(data_to_json(test_data))

    print("\n=== With base indent=8 (all lines shifted right by 8 spaces) ===")
    print(data_to_json(test_data, indent=8))

    print("\n=== With base indent=0 (explicit no base indent) ===")
    print(data_to_json(test_data, indent=0))

    print("\n=== With indent_size=2 (smaller nested indents) ===")
    print(data_to_json(test_data, indent_size=2))

    print("\n=== Without simple pairs grouping ===")
    print(data_to_json(test_data, pairs_in_one_line=False))

    print("\n=== Skip empty arrays ===")
    print(data_to_json(test_data, skip_empty_arrays=True))

    print("\n=== Compressed format ===")
    print(data_to_json(test_data, compress=True))

    print("\n=== Compressed + skip empty arrays ===")
    print(data_to_json(test_data, compress=True, skip_empty_arrays=True))

    print("\n=== Sort keys ===")
    print(data_to_json(test_data, sort_keys=True))

    print("\n=== Escape special characters ===")
    print(data_to_json(test_data, escape_special=True))

    print("\n=== Escape Unicode ===")
    print(data_to_json(test_data, escape_unicode=True))

    print("\n=== Ensure ASCII (safe for file output) ===")
    print(data_to_json(test_data, ensure_ascii=True))

    print("\n=== Ensure ASCII + Compressed ===")
    print(data_to_json(test_data, ensure_ascii=True, compress=True))

    print("\n=== Without allowing NaN/Infinity ===")
    try:
        print(data_to_json(test_data, allow_nan=False))
    except ValueError as e:
        print(f"Error: {e}")

    # Test with data without NaN/Infinity
    safe_data = {k: v for k, v in test_data.items()
                 if not (isinstance(v, float) and (v != v or v == float('inf') or v == float('-inf')))}

    print("\n=== Safe data without NaN ===")
    print(data_to_json(safe_data, allow_nan=False, sort_keys=True))

    # Test with simple data
    simple_data = {
        "a": 1,
        "b": "text",
        "c": True,
        "d": None
    }

    print("\n=== Simple data ===")
    print(data_to_json(simple_data))

    # Test with list
    list_data = [1, 2, 3, "test", True, None]

    print("\n=== Simple list ===")
    print(data_to_json(list_data))

    complex_list = [
        {"name": "Item 1", "value": 100},
        {"name": "Item 2", "value": 200},
        {"name": "Item 3", "value": 300}
    ]

    print("\n=== Complex list ===")
    print(data_to_json(complex_list))

    print("\n=== Complex list with base indent=4 ===")
    print(data_to_json(complex_list, indent=4))

    print("\n=== Combination: base indent=6, nested indent_size=2 ===")
    print(data_to_json(test_data, indent=6, indent_size=2))

################################################################################
__all__ = (
    'data_to_json',
)
################################################################################
