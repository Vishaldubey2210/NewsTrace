"""
JSON Exporter Module
Serializes news intelligence, entity graphs, and sentiment records into JSON format.
"""

import json
from typing import List, Dict, Any

class JSONExporter:
    """Exports structured news articles and analytics to JSON files or strings."""

    @staticmethod
    def export_to_string(data: Any, indent: int = 2) -> str:
        return json.dumps(data, indent=indent, default=str)

    @staticmethod
    def export_to_file(data: Any, filepath: str, indent: int = 2) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, default=str)
            return True
        except Exception:
            return False
