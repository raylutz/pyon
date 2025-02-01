"""
pyontools.py

PYONTools: A lightweight module for encoding and decoding Python Object Notation (PYON).

PYON (Python Object Notation) mirrors Python's `repr()` output, making it a simple, 
human-readable format for serializing Python-native objects such as `dict`, `list`, 
`tuple`, `set`, and more. PYONTools provides safe methods for encoding, decoding, 
and compacting PYON data, particularly useful for CSV workflows.

Core Features:
- pyon_encode: Generate PYON representations using Python's `repr()` output.
- pyon_decode: Safely reconstruct PYON-encoded strings into Python objects.
- pyon_decode_row: Decode entire CSV rows containing PYON-encoded objects.
- remove_spaces: Produce a compact PYON representation by removing unnecessary spaces.
- pyon_to_json: Convert PYON-compatible objects into JSON format for external compatibility.

Example Use Cases:
- Serializing arbitrary objects for storage without restrictions of JSON
- Storing Python-native objects in CSV files with `csv.writer`.
- Reading and decoding structured data using `csv.reader`.
- Compacting PYON strings for optimized storage.
- Ensuring safe deserialization of string representations.

Key Differences Between PYON and JSON:
- PYON supports non-string dictionary keys, sets, and tuples, which JSON does not.
- PYON is human-readable and mirrors native Python syntax (`repr()`).
- JSON ensures cross-language compatibility, while PYON is Python-specific, but
is easily converted to JSON (although losing flexibility).

Examples:

# JSON fails to handle these cases:
data = {
    1: "integer key",          # Non-string key
    "set": {1, 2, 3},          # Set type
    "tuple": (1, 2, 3),        # Tuple type
    "nested": {"a": True, "b": [1, 2, 3]}
}

# PYON representation:
pyon_str = repr(data)
print(pyon_str)
# Output: {1: 'integer key', 'set': {1, 2, 3}, 'tuple': (1, 2, 3), 'nested': {'a': True, 'b': [1, 2, 3]}}

# Safely decode PYON back to a Python object:
import ast
decoded = ast.literal_eval(pyon_str)
print(decoded)
# Output: {1: 'integer key', 'set': {1, 2, 3}, 'tuple': (1, 2, 3), 'nested': {'a': True, 'b': [1, 2, 3]}}

# JSON limitations:
import json
try:
    json_str = json.dumps(data)  # This will raise a TypeError due to unsupported types
except TypeError as e:
    print(f"JSON Error: {e}")
# Output: JSON Error: keys must be str, int, float, bool or None, not int

License: MIT License
Author: Ray Lutz
Version: 0.1.0
"""

import ast
import re
import pprint
from typing import Any, List #, Union


__all__ = [
    "sort_dict_keys", 
    "normalize_pyon", 
    "pyon_encode", 
    "pyon_decode", 
    "remove_spaces", 
    "pyon_to_json", 
    "pyon_decode_row",
    "dumps",
    "loads",
]


# Core PYON Methods
def pyon_encode(obj: Any, indent: int=0, width=160) -> str:
    """
    Encode a Python object into its __repr__ representation (PYON format).
    Mirrors the behavior of csv.writer() for embedded structures.

    Args:
        obj: The Python object to encode.
        indent: if nonzero, create indented "pretty printed" form using multiple lines.
        width: if indent is nonzero, then limit width to this number of characters.

    Returns:
        str: __repr__ representation of the object.
    """
    if indent:
        return pprint.pformat(obj, indent=indent, width=width, compact=False)
    
    return repr(obj)


def pyon_decode(pyon_str: str) -> Any:
    """
    Safely decode a PYON-encoded string into its original Python object.

    Args:
        pyon_str: The string representation to decode.

    Returns:
        Any: The reconstructed Python object.

    Raises:
        ValueError: If decoding fails.
    """
    if not pyon_str:
        return pyon_str
    
    try:
        return ast.literal_eval(pyon_str)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Invalid PYON data: {e}")


# support aliases for compatibility with existing code.

dumps = pyon_encode
loads = pyon_decode


# Utility for Compact Representation
def remove_spaces(pyon_str: str) -> str:
    """
    Remove spaces from a PYON string, ignoring spaces inside quotes.

    Args:
        pyon_str: The input string in PYON format.

    Returns:
        str: The string with spaces removed outside quoted substrings.
    """
    return re.sub(r" (?=(?:[^']*'[^']*')*[^']*$)", "", pyon_str)


# PYON to JSON Converter
def pyon_to_json(obj: Any) -> str:
    """
    Convert a PYON-compatible object to JSON format.
    Raises an error for unsupported non-JSON types.
    Attempts to get maximum conversion to equivalent types.

    Args:
        obj: The PYON object to convert.

    Returns:
        str: JSON-formatted string.

    Raises:
        TypeError: If unsupported types are encountered.
    """
    import json
    import types

    def convert(value):
        if isinstance(value, (str, int, float, bool, type(None))):
            return value
        elif isinstance(value, dict):
            return {str(k): convert(v) for k, v in value.items()}  # Ensure string keys
        elif isinstance(value, list):
            return [convert(v) for v in value]
        elif isinstance(value, tuple):
            return [convert(v) for v in value]  # Convert tuple to list
        elif isinstance(value, (types.FunctionType, type)):
            return f"{value.__module__}.{value.__qualname__}"
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    return json.dumps(convert(obj), separators=(",", ":"))
    
    
def simple_pyon_to_json(pyon_str: str) -> str: # JSON str
    """
    Convert a PYON-compatible object to JSON format.
    Raises an error for unsupported non-JSON types.
    Simple conversion to use when the pyon has no non-JSONable objects.
    
    Note: This does not handle any extensions, such as trailing commas, integer or tuple keys, etc.
            
    Perfect for conversion of indirect columns for SQL processing that requires JSON.

    Args:
        obj: The PYON object to convert.

    Returns:
        str: JSON-formatted string.

    Raises:
        TypeError: If unsupported types are encountered.
    """
    
    json_str = re.sub(r"'", '"', pyon_str)
    return json_str
    
    
    # import json
    # return json.dumps(pyon_decode(pyon_str), separators=(",", ":"))
    
    


def pyon_decode_row(row: List[str]) -> List[Any]:
    """
    Decode an entire CSV row with PYON-encoded strings. Identifies objects when strings start/end with {}, [], ()

    Args:
        row: A list of strings (as delivered by csv.reader).

    Returns:
        A list where PYON strings are decoded into Python objects, and other strings are left as-is.
    """
    decoded_row = []
    for cell in row:
        if isinstance(cell, str) and (
            (cell.startswith("{") and cell.endswith("}")) or
            (cell.startswith("[") and cell.endswith("]")) or
            (cell.startswith("(") and cell.endswith(")"))
        ):
            try:
                decoded_row.append(pyon_decode(cell))
            except ValueError:
                decoded_row.append(cell)  # Leave invalid PYON as string
        else:
            decoded_row.append(cell)  # Leave non-PYON strings as-is
    return decoded_row
    
    
def sort_dict_keys(obj: Any) -> Any:
    """
    Recursively sort dictionary keys in a Python object.

    Args:
        obj: The input object, which can be a dictionary, list, tuple, or other types.

    Returns:
        The input object with dictionary keys sorted recursively.
    """
    if isinstance(obj, dict):
        # Sort keys and apply sorting to values
        return {k: sort_dict_keys(v) for k, v in sorted(obj.items())}
    elif isinstance(obj, list):
        # Apply sorting recursively to list elements
        return [sort_dict_keys(item) for item in obj]
    elif isinstance(obj, tuple):
        # Apply sorting recursively to tuple elements
        return tuple(sort_dict_keys(item) for item in obj)
    else:
        # Return object as-is if not a container
        return obj


def normalize_pyon(pyon_str: str) -> str:
    """
    Normalize a PYON string by decoding it, sorting dictionary keys recursively, 
    and re-encoding it into a consistent PYON format.

    Args:
        pyon_str: A string containing PYON-encoded data.

    Returns:
        str: A normalized PYON string with sorted dictionary keys.

    Notes:
        - If the input string cannot be decoded as PYON, it is returned unchanged.
    """
    try:
        # Safely decode the PYON string into a Python object
        pyon_obj = pyon_decode(pyon_str)
        # Recursively sort dictionary keys
        normalized_obj = sort_dict_keys(pyon_obj)
        # Re-encode into a consistent PYON string
        return pyon_encode(normalized_obj)
        
    except (ValueError, SyntaxError):
        # Return the original string if decoding fails
        return pyon_str



# Example of Usage
if __name__ == "__main__":
    # Encode and Decode Example
    data = {"key": True, "list": [1, 2, 3], "nested": {"a": 1, "b": 2}}
    encoded = pyon_encode(data)
    print("Encoded PYON:", encoded)

    decoded = pyon_decode(encoded)
    print("Decoded PYON:", decoded)

    # Remove Spaces Example
    compact = remove_spaces(encoded)
    print("Compact PYON:", compact)

    # Convert to JSON Example
    json_data = pyon_to_json(data)
    print("JSON Data:", json_data)
