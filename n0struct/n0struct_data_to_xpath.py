from typing import Any, Union


def data_to_xpath(
    data: Any,
    indent: Union[int, None] = None,
) -> str:
    """
    Public function: collect elements xpath starts from root and print with indents
    """
    def _build_xpath_list(obj, path="", result_list=None):
        """
        Recursively build list of (xpath, value) tuples
        """
        if result_list is None:
            result_list = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}/{key}" if path else f"//{key}"
                if isinstance(value, (dict, list)):
                    _build_xpath_list(value, current_path, result_list)
                else:
                    result_list.append((current_path, str(value)))
        
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                current_path = f"{path}[{index}]"
                if isinstance(item, (dict, list)):
                    _build_xpath_list(item, current_path, result_list)
                else:
                    result_list.append((current_path, str(item)))
        
        return result_list
    
    # Build list of xpath-value pairs
    xpath_list = _build_xpath_list(data)
    
    # Determine alignment width and left indentation
    if indent is None:
        # Auto-align to maximum xpath length, no left indent
        max_xpath_length = max(len(f"['{xpath}']") for xpath, _ in xpath_list) if xpath_list else 0
        left_indent = ""
    else:
        # Use provided indent for left indentation
        max_xpath_length = max(len(f"['{xpath}']") for xpath, _ in xpath_list) if xpath_list else 0
        left_indent = " " * indent
    
    # Format and print each line
    # for xpath, value in xpath_list:
        # xpath_formatted = f"['{xpath}']"
        # padding = " " * (max_xpath_length - len(xpath_formatted))
        # print(f"{left_indent}{xpath_formatted}{padding} = \"{value}\"")
    return (
        '\n'.join(
            f"{left_indent}{xpath_formatted}{" "* (max_xpath_length - len(xpath_formatted))} = \"{value}\""
            for xpath, value in xpath_list
            if (xpath_formatted:=f"['{xpath}']")
        )
    )


if __name__ == "__main__":
    sample_data = {
        "Products": {
            "Product": [
                {
                    "ImageUrl": "/Portals/harwoodgame/CVStoreImages/MuntBox.jpg",
                    "DisplayOrder": "1"
                },
                {
                    "ProductID": "120",
                    "PortalID": "20"
                }
            ]
        }
    }
    
    print("Without indent:")
    print(data_to_xpath(sample_data))
    
    print("With indent=4:")
    print(data_to_xpath(sample_data, indent=4))
    
    print("With indent=8:")
    print(data_to_xpath(sample_data, indent=8))


################################################################################
__all__ = (
    'data_to_xpath',
)
################################################################################
