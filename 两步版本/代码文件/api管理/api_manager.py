import json

class ApiKeyManager:
    def __init__(self, file_path):
        self.api_keys = self.load_api_keys(file_path)

    def load_api_keys(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_api_key(self, api_name):
        if api_name in self.api_keys:
            return self.api_keys[api_name]
        raise ValueError(f"API key for '{api_name}' not found.")