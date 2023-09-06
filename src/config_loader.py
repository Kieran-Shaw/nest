import json


class ServiceConfig:
    def __init__(self, config_path: str):
        self.config = self.load_config(file_path="config/config.json")

    @staticmethod
    def load_config(file_path: str) -> dict:
        with open(file_path, "r") as f:
            return json.load(f)
