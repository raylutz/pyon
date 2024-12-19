# **pyon** -- **PYONTools**
pyon: Python Object Notation -- Better Superset of JSON expresses python sets, tuples, dicts, lists, func

**PYONTools** is a lightweight Python module for working with **PYON** (Python Object Notation), a format that is a **superset of JSON**, designed to work seamlessly with Python's **`repr()`** format. PYON provides safe and convenient methods for encoding, decoding, and compacting Python-native objects, making it particularly useful when working with **CSV files**, **Python-native structures**, or ensuring **external compatibility** with tools like JSON.

---

## **What Makes PYON Unique**

1. **Superset of JSON**:  
   - Any valid JSON is also valid PYON, ensuring compatibility with JSON-based systems.
   - Additionally, PYON extends JSON to support Python-specific features.

2. **Additional Features**:
   - **Trailing Commas**: PYON allows trailing commas in lists, tuples, and dictionaries, following Python syntax.
   - **Both Single and Double Quotes**: String literals can use either single (`'`) or double (`"`) quotes for flexibility.
   - **PEP 8 Compliance**: Canonical PYON enforces Python’s style guide for consistent and human-readable formatting.

3. **Beyond JSON**:  
   PYON supports Python-native types and constructs that JSON cannot represent, including:
   - Non-string dictionary keys
   - Sets and tuples
   - Arbitrary objects if `__repr__` is defined
   - Function and class references (module-qualified names)

---

## **Features**

- 🔄 **Encode**: Generate PYON representations using Python's `repr()` for native compatibility.
- ✅ **Safe Decode**: Convert PYON strings back into Python objects safely using `ast.literal_eval`.
- 🚀 **Compact Representation**: Optionally remove unnecessary spaces for minimal output.
- 🔒 **JSON Compatibility**: Convert PYON-compatible objects to valid JSON format.
- 📄 **CSV-Friendly**: Seamlessly integrates with Python’s built-in `csv` module for reading and writing.

---

## **PYON vs JSON**

PYON is an **enhanced version of JSON** that embraces Python-native features, making it more versatile for Python developers:

| **Feature**                    | **PYON**                                | **JSON**                  | **Pickle**                          |
|--------------------------------|-----------------------------------------|---------------------------|-------------------------------------|
| Non-string dictionary keys     | ✅ Supported                            | ❌ Not allowed            | ✅ Supported                        |
| Set data type                  | ✅ Supported                            | ❌ Not supported          | ✅ Supported                        |
| Tuple data type                | ✅ Supported                            | ❌ Not supported          | ✅ Supported                        |
| Function/Class references      | ✅ Represented by module and name       | ❌ Not serializable       | ✅ Serialized as references         |
| Arbitrary data object          | ✅ Supported if `__repr__` provided     | ❌ Not supported          | ✅ Fully supported                  |
| Trailing commas                | ✅ Supported                            | ❌ Not allowed            | ❌ Not applicable                   |
| Single and double quotes        | ✅ Both allowed                         | ❌ Only double quotes     | ❌ Not applicable (binary format)   |
| Readability                    | ✅ Human-readable (PEP 8 compliant)     | ✅ Human-readable         | ❌ Not human-readable               |
| Cross-language compatibility   | ❌ Python-specific but easily converted | ✅ Supported across tools | ❌ Python-specific only             |

---

## **Example Demonstrating Flexibility**

```python
import json
from pyontools import pyon_encode, pyon_decode

# PYON handles non-string keys, sets, and tuples
data = {
    1: "integer key",          # Non-string key
    "set": {1, 2, 3},          # Set type
    "tuple": (1, 2, 3),        # Tuple type
    "nested": {"a": True, "b": [1, 2, 3]},
}

# PYON Representation
pyon_str = pyon_encode(data)
print("PYON:", pyon_str)

# Safe decoding
decoded = pyon_decode(pyon_str)
print("Decoded:", decoded)

# JSON attempt (will fail)
try:
    json_str = json.dumps(data)
except TypeError as e:
    print("JSON Error:", e)
```

**Output**:
```plaintext
PYON: {1: 'integer key', 'set': {1, 2, 3}, 'tuple': (1, 2, 3), 'nested': {'a': True, 'b': [1, 2, 3]}}
Decoded: {1: 'integer key', 'set': {1, 2, 3}, 'tuple': (1, 2, 3), 'nested': {'a': True, 'b': [1, 2, 3]}}
JSON Error: keys must be str, int, float, bool or None, not int
```

---

## **Installation**

Copy the `pyontools.py` file into your project directory.

If you plan to expand this into a full package, it can be installed from PyPI in the future.

---

## **Why PYON?**

PYON already exists. It is defined by what you get if you perform f"{any_object}" to any_object. Thus, we only need to 
document it, and provide some tools for working with it. Better than PICKLE, jsonpickle, and other variants of JSON.

1. **Superset of JSON**: Any valid JSON is valid PYON, but PYON supports additional Python-native features.
2. **Human-Readable**: PYON mirrors Python’s `repr()`, ensuring readability for developers.
3. **PEP 8 Compliance**: Canonical PYON adheres to Python's style guidelines, ensuring consistent formatting.
4. **Safe**: Decoding uses `ast.literal_eval`, avoiding arbitrary code execution.
5. **Python-Native**: Supports Python-specific types, including sets, tuples, and non-string keys.
6. **Lightweight**: No external dependencies required.
7. **CSV-Friendly**: Works seamlessly with `csv.writer()` and `csv.reader()`.

---

## **Future Plans**

- Explore compact mode for `csv.writer` for further optimization.

---

## **License**

This project is licensed under the MIT License.

---

## **Feedback and Contributions**

Contributions and feedback are welcome! If you encounter any issues or have feature suggestions, feel free to submit them. 🚀
