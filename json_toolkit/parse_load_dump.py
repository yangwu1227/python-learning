# ---------------------------------------------------------------------------- #
#                                    Import                                    #
# ---------------------------------------------------------------------------- #

import os
import json
import inspect

# ---------------------------------------------------------------------------- #
#                                JSON to Python                                #
# ---------------------------------------------------------------------------- #

json_string = '{"name":"John", "age":30, "city":["New York", "Beijing"]}'

# Convert to python dictionary using the loads() function
py_dict = json.loads(s=json_string)
# Check function
inspect.isfunction(json.loads)

py_dict.keys()
py_dict.values()

# Type of values
[type(val) for val in py_dict.values()]

# ---------------------------------------------------------------------------- #
#                                Parse from file                               #
# ---------------------------------------------------------------------------- #

# Open file with 'rt' read only and text (by default)
with open('sample.json', 'rt') as f:
    nested_dict = json.load(f)

# Level 1 keys
keys_1 = (id for id in nested_dict.keys())
list(keys_1)

# level 1 values
# Check type for each value-- both are dictionaries
[type(val) for val in nested_dict.values()]

# Level 2 keys
# Each val is nested_dict.values() is a dictionary
# This returns a nested list
nested_level2_keys = [list(val.keys()) for val in nested_dict.values()]

# Instantiate empty container
flat_list_loop = []
# Flatten the list to retrieve all level 2 keys (loop)
for sublist in nested_level2_keys:
    for key in sublist:
        flat_list_loop.append(key)

# Flatten the list to retrieve all level 2 keys (list comp)
# Call each element in nested_level2_keys 'sublist'
# Call each element in each 'sublist' 'key'
# The outer loop is the expression (for sublist in nested_level2_keys)
# The inner loop is broken up by the above expressions (key (outer loop) for key in sublist)
flat_list_comp = [key for sublist in nested_level2_keys for key in sublist]

# Level 2 values
nested_level2_vals = [list(val.values()) for val in nested_dict.values()]
# Check type of each element--- both are lists
[type(val) for val in nested_level2_vals]
# Therefore, we need to go one more level down to check the elements of each of those two lists
# All elements are dictionaries
[val for sublist in nested_level2_vals for val in sublist]

# ---------------------------------------------------------------------------- #
#                                Python to JSON                                #
# ---------------------------------------------------------------------------- #

# Convert a Python object containing all the legal data types to JSON
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
# Convert
print(json.dumps(py_obj))
# Write to disk with pretty format
# Use 4 places to indent and sort the keys
with open('myinfo_default.json', 'wt', encoding='utf-8') as json_file:
    json.dump(py_obj, json_file, ensure_ascii=True, indent=4, sort_keys=True)

# Change separators when writing
# Default value is (", ", ": ")
# A comma and a space (no space on left side) to separate each object
# A colon and a space (spaces on both sides) to separate keys from values
with open('myinfo_custom_separators.json', 'wt', encoding='utf-8') as json_file:
    json.dump(py_obj, json_file, indent=4,
              separators=("/ ", " = "), sort_keys=True)
