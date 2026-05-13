#!/usr/bin/env python3
import json
import re

class TOON:
    """
    Token-efficient Object Notation (TOON).
    Designed to compress JSON-like structures for LLM context optimization.
    
    Format: [key|value] or [key|val1;val2;val3]
    Nested: [key|[subkey|val]]
    """
    
    @staticmethod
    def encode(data) -> str:
        """Converts Python dict/list to TOON string."""
        if isinstance(data, dict):
            parts = []
            for k, v in data.items():
                encoded_v = TOON.encode(v)
                parts.append(f"{k}|{encoded_v}")
            return "[" + ";".join(parts) + "]"
        elif isinstance(data, list):
            return "(" + ";".join(TOON.encode(i) for i in data) + ")"
        elif isinstance(data, bool):
            return "1" if data else "0"
        elif data is None:
            return "~"
        else:
            return str(data)

    @staticmethod
    def decode(toon_str: str):
        """Decodes TOON string back to Python objects using a stack-based parser."""
        if not toon_str:
            return None
            
        def parse(text, pos=0):
            char = text[pos]
            if char == '[': # Dict
                pos += 1
                obj = {}
                while text[pos] != ']':
                    key, pos = parse_key(text, pos)
                    if text[pos] != '|': raise ValueError(f"Expected | at {pos}")
                    pos += 1
                    val, pos = parse(text, pos)
                    obj[key] = val
                    if text[pos] == ';': pos += 1
                return obj, pos + 1
            elif char == '(': # List
                pos += 1
                lst = []
                while text[pos] != ')':
                    val, pos = parse(text, pos)
                    lst.append(val)
                    if text[pos] == ';': pos += 1
                return lst, pos + 1
            elif char == '1': return True, pos + 1
            elif char == '0': return False, pos + 1
            elif char == '~': return None, pos + 1
            else: # String/Value
                match = re.match(r"[^|;\]\)]+", text[pos:])
                if not match: return "", pos
                val = match.group(0)
                return val, pos + len(val)

        def parse_key(text, pos):
            match = re.match(r"[^|]+", text[pos:])
            key = match.group(0)
            return key, pos + len(key)

        result, _ = parse(toon_str)
        return result

if __name__ == "__main__":
    test_data = {
        "id": "1d181db9",
        "status": "pending",
        "priority": "normal",
        "tags": ["core", "ui"],
        "metadata": {"version": 1, "active": True}
    }
    
    json_str = json.dumps(test_data)
    toon_str = TOON.encode(test_data)
    
    print(f"JSON ({len(json_str)} chars): {json_str}")
    print(f"TOON ({len(toon_str)} chars): {toon_str}")
    print(f"Compression: {((len(json_str) - len(toon_str)) / len(json_str)) * 100:.1f}%")
