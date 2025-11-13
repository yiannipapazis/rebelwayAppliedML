import json
import os
from dataclasses import dataclass, field

@dataclass
class Fstream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)
    
    @classmethod
    def load_json_files(cls, path) -> dict:
        """
        Read json files from a directory
        
        Args:
            path: the path for the json file to read.
        Returns:
            dict: A hash map with the json structure.
        """
        print(f"Reading data file from {path}...")
        with open(path, "r") as data_file:
            try:
                cls.data_file = json.load(data_file)
            except json.decoder.JSONDecodeError:
                print(f"Empty JSON file. Initializing empty dictionary...")
                cls.data_file = {}
        return cls.data_file
    
    @staticmethod
    def print_json_structure(data_file: dict):
        for id, item in data_file["Items"].items():
            print(id ,item)
