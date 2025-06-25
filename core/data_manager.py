import json
import os
from typing import List, Type, TypeVar, Any

T = TypeVar("T")


class JSONDataManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        # Ensure the file exists with an empty list if it's new
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def load_items(self, item_type: Type[T]) -> List[T]:
        """Loads a list of dataclass instances from the JSON file."""
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                return [item_type.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_items(self, items: List[T]):
        """Saves a list of dataclass instances to the JSON file."""
        with open(self.filepath, "w") as f:
            json.dump([item.to_dict() for item in items], f, indent=4)

    def load_raw_data(self) -> Any:
        """Loads raw JSON data from the file (e.g., for simple lists/dicts)."""
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Return empty list by default for people.json

    def save_raw_data(self, data: Any):
        """Saves raw Python data (list, dict, etc.) to the JSON file."""
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
