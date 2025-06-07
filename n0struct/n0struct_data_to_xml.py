from typing import Any, Union


def data_to_xml(
    data: Any,
    indent: Union[int, None] = None,
    indent_size: int = 4,
    encoding: str = "utf-8",
    quote: str = '"',
) -> str:
    """
    Converts complex structure (dict/list) to XML string.
    
    Args:
        data: Dictionary or list to convert
        indent: Base indentation for entire XML (default None)
        indent_size: Indentation size for each nesting level (default 4)
        encoding: Encoding for XML header (default "utf-8", "" - without encoding, None - without header)
        quote: Quote type for attribute values (default ")
        
    Returns:
        str: XML string
    """
    
    def escape_xml(text):
        """Escapes special XML characters"""
        if not isinstance(text, str):
            text = str(text)
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&apos;'))
    
    def get_indent_str(level):
        """Returns indentation string for specified level"""
        if indent_size == 0:
            return ""
        base_indent = " " * (indent if indent else 0)
        level_indent = " " * (indent_size * level)
        return base_indent + level_indent
    
    def get_newline():
        """Returns newline character or empty string"""
        return "\n" if indent_size > 0 else ""
    
    def process_element(key, value, level=0):
        """Processes one element of data structure"""
        indent_str = get_indent_str(level)
        newline = get_newline()
        
        if isinstance(value, dict):
            # Separate attributes and child elements
            attributes = {}
            children = {}
            
            for k, v in value.items():
                if k.startswith('@'):
                    attributes[k[1:]] = v  # remove @ from attribute name
                else:
                    children[k] = v
            
            # Form attribute string
            attr_str = ""
            if attributes:
                attr_parts = []
                for attr_name, attr_value in attributes.items():
                    escaped_value = escape_xml(attr_value)
                    attr_parts.append(f"{attr_name}={quote}{escaped_value}{quote}")
                attr_str = " " + " ".join(attr_parts)
            
            # If there are child elements
            if children:
                result = f"{indent_str}<{key}{attr_str}>{newline}"
                
                for child_key, child_value in children.items():
                    if isinstance(child_value, list):
                        for item in child_value:
                            result += process_element(child_key, item, level + 1)
                    else:
                        result += process_element(child_key, child_value, level + 1)
                
                result += f"{indent_str}</{key}>{newline}"
                return result
            else:
                # Self-closing tag
                return f"{indent_str}<{key}{attr_str}/>{newline}"
        
        elif isinstance(value, list):
            # For lists create multiple elements with same name
            result = ""
            for item in value:
                result += process_element(key, item, level)
            return result
        
        else:
            # Simple value
            escaped_value = escape_xml(value)
            return f"{indent_str}<{key}>{escaped_value}</{key}>{newline}"
    
    # Generate XML header
    xml_parts = []
    
    if encoding is not None:  # None means without header
        if encoding:  # Non-empty string
            header = f'<?xml version="1.0" encoding="{encoding}"?>'
        else:  # Empty string
            header = '<?xml version="1.0"?>'
        
        if indent:
            header = " " * indent + header
        
        xml_parts.append(header)
        if indent_size > 0:
            xml_parts.append("")  # Empty line for separation
    
    # Process main data
    if isinstance(data, dict):
        for key, value in data.items():
            if not key.startswith('@'):  # Ignore attributes at root level
                xml_parts.append(process_element(key, value, 0))
    elif isinstance(data, list):
        # If list is passed, wrap in root element
        for i, item in enumerate(data):
            xml_parts.append(process_element(f"item_{i}", item, 0))
    else:
        # Wrap simple value in root element
        xml_parts.append(process_element("root", data, 0))
    
    # Join all parts
    if indent_size > 0:
        result = "\n".join(xml_parts)
    else:
        result = "".join(xml_parts)
    
    # Remove extra newlines at the end
    return result.rstrip()


# Usage examples
if __name__ == "__main__":
    # Test data
    test_data = {
        "root": {
            "@id": "123",
            "@type": "document",
            "title": "Document title",
            "content": {
                "@lang": "en",
                "text": "Content text",
                "metadata": {
                    "author": "Author",
                    "date": "2024-01-01"
                }
            },
            "items": [
                {"@id": "1", "name": "Item 1"},
                {"@id": "2", "name": "Item 2"},
                {"@id": "3", "name": "Item 3"}
            ]
        }
    }
    
    print("=== Standard XML ===")
    print(data_to_xml(test_data))
    
    print("\n=== With base indentation of 2 spaces ===")
    print(data_to_xml(test_data, indent=2))
    
    print("\n=== Indentation size = 2 ===")
    print(data_to_xml(test_data, indent_size=2))
    
    print("\n=== Without line breaks ===")
    print(data_to_xml(test_data, indent_size=0))
    
    print("\n=== Without encoding in header ===")
    print(data_to_xml(test_data, encoding=""))
    
    print("\n=== Without header ===")
    print(data_to_xml(test_data, encoding=None))
    
    print("\n=== With single quotes ===")
    print(data_to_xml(test_data, quote="'"))

################################################################################
__all__ = (
    'data_to_xml',
)
################################################################################
