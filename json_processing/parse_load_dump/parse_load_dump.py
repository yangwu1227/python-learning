# ---------------------------------------------------------------------------- #
#                                    Import                                    #
# ---------------------------------------------------------------------------- #

import os
import json
import inspect
from typing import Dict, Any, Tuple

# ---------------------------------------------------------------------------- #
#                                JSON to Python                                #
# ---------------------------------------------------------------------------- #

def parse_json(json_string: str) -> Dict[str, Any]:
    """
    Convert a JSON string to a Python dictionary and explore its content.

    Parameters
    ----------
    json_string : str
        JSON string to be parsed.

    Returns
    -------
    Dict[str, Any]
        A dictionary representation of the JSON string.

    Notes
    -----
    This function uses the json.loads() method to convert the JSON string
    and inspect various properties of the resultant dictionary.
    """
    py_dict = json.loads(s=json_string)
    
    return py_dict

# ---------------------------------------------------------------------------- #
#                                Parse from file                               #
# ---------------------------------------------------------------------------- #

def parse_json_from_file(filename: str) -> Dict[str, Any]:
    """
    Parse JSON data from a file and analyze its structure.

    Parameters
    ----------
    filename : str
        File path for the JSON file to be parsed.

    Returns
    -------
    Dict[str, Any]
        A dictionary with nested dictionaries as parsed from the JSON file.

    Notes
    -----
    This function examines various levels of nesting within the JSON data
    and provides insights into the data structure by exploring keys and values at different levels.
    """
    with open(filename, 'rt') as f:
        nested_dict = json.load(f)

    keys_level1 = list(nested_dict.keys())
    values_level1 = [type(val) for val in nested_dict.values()]
    
    print(f"Level 1 keys: {keys_level1}")
    print(f"Level 1 values: {values_level1}")
    
    nested_level2_keys = [list(val.keys()) for val in nested_dict.values()]
    flat_list_comp = [key for sublist in nested_level2_keys for key in sublist]
    nested_level2_vals = [list(val.values()) for val in nested_dict.values()]
    
    print(f"Level 2 keys: {flat_list_comp}")
    print(f"Level 2 values: {nested_level2_vals}")
    
    # Extracting further nested values and their types
    further_nested_vals = [val for sublist in nested_level2_vals for val in sublist]
    types_of_further_nested_vals = [type(item) for sublist in nested_level2_vals for item in sublist]
    
    print(f"Further nested values: {further_nested_vals}")
    print(f"Types of further nested values: {types_of_further_nested_vals}")
    
    return nested_dict

# ---------------------------------------------------------------------------- #
#                                Python to JSON                                #
# ---------------------------------------------------------------------------- #

def convert_to_json_and_save(py_obj: Dict[str, Any], filename: str, custom_separators: Tuple[str, str] = (", ", ": ")) -> None:
    """
    Convert a Python dictionary to a JSON string and save it to a file.

    Parameters
    ----------
    py_obj : Dict[str, Any]
        The Python dictionary to convert.
    filename : str
        The file path to save the JSON data.
    custom_separators : Tuple[str, str], optional
        Separators for objects and array elements (default is (", ", ": ")).

    Notes
    -----
    This function allows customizing the JSON output format by specifying separators
    and the sort order of keys. The default behavior is to use JSON's default separators.
    The function will print the JSON string and write it to the specified file with
    indentation for better readability and sorted keys.
    """
    json_str = json.dumps(py_obj)
    print(json_str)
    
    with open(filename, 'wt', encoding='utf-8') as json_file:
        json.dump(py_obj, json_file, ensure_ascii=True, indent=4, separators=custom_separators, sort_keys=True)

# ---------------------------------------------------------------------------- #
#                                    Main                                      #
# ---------------------------------------------------------------------------- #

def main() -> int:
    """
    Main function to handle workflow.
    """
    json_string = '{"name":"John", "age":30, "city":["New York", "Beijing"]}'
    py_dict = parse_json(json_string)
    print(py_dict)
    
    nested_dict = parse_json_from_file('sample.json')
    print(nested_dict)
    
    py_obj = {
        "name": "Yang",
        "age": 23,
        "married": False,
        "divorced": False,
        "children": ("Ann", "Billy"),
        "pets": None,
        "sex": "Male",
        "programming Language": ["R", "Python", "C++", "SQL"],
        "favorite numbers": (7, 12, 17, 27),
        "cars": [
            {"model": "Chevy Prizm", "mpg": 27.5},
            {"model": "Ford Edge", "mpg": 24.1}
        ]
    }
    convert_to_json_and_save(py_obj, 'myinfo_custom_separators.json', ("/ ", " = "))
    
    return 0

if __name__ == "__main__":
    
    main()
