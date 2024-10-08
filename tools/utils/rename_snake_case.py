import os
import re
from pathlib import Path

def to_snake_case(name) -> str:
    # Identify the file extension if present (ignoring hidden files starting with .)
    if '.' in name and not name.startswith('.'):
        # One split on the last occurrence of the period
        base_name, extension = name.rsplit('.', 1)
        # Replace spaces and other non-alphanumeric characters (excluding parentheses) with underscores in the base name
        snake_case_name = re.sub(r'\s+', '_', base_name).lower()
        snake_case_name = re.sub(r'[^\w\d_\(\)]', '_', snake_case_name)
        # Reattach the extension
        return f"{snake_case_name}.{extension}"
    else:
        # Process names without extensions (or hidden files) directly
        snake_case_name = re.sub(r'\s+', '_', name).lower()
        snake_case_name = re.sub(r'[^\w\d_\(\)]', '_', snake_case_name)
        return snake_case_name

def rename_to_snake_case(path) -> None:
    temp_suffix = "_temp_rename"
    # First pass: rename to a temporary name
    for current_path in Path(path).rglob('*'):
        if current_path.name.startswith('.'):
            continue
        temp_name = current_path.parent / (current_path.name + temp_suffix)
        os.rename(current_path, temp_name)
    # Second pass: rename to the final snake case name
    for temp_path in Path(path).rglob(f'*{temp_suffix}'):
        original_name = temp_path.name[:-len(temp_suffix)]
        new_name = to_snake_case(original_name)
        final_name = temp_path.parent / new_name
        os.rename(temp_path, final_name)
        print(f"Renamed {temp_path} to {final_name}")

def main() -> int:
    # Rename files and directories in the current directory
    rename_to_snake_case('.')
    return 0

if __name__ == '__main__':
    
    main()
