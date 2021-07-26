from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import bson


class BysonDB:
    """
    A BysonDB instance.

    Parameters
    -----------
    file: str
        The name or path to the file where the database will store it's data.
        The file will be created if it does not exist, or existing data
        will be loaded.
    """

    def __init__(self, file: str):
        
        self.file = file
        self.path = Path(file).with_suffix(".bson")

        self._db = {}

        self._load_if_exists()
    
    def __str__(self) -> str:
        return f"<BysonDB file={self.path.resolve()} data={self._db}>"

    def _load_if_exists(self) -> None:
        """
        Loads the database file if it exists. If it does not exist, a new one
        is created.
        """
        try:
            self._db = self._load()
        except FileNotFoundError:
            self._dump()

    def _load(self) -> Optional[dict]:
        """
        Open the database file, and load the data stored in it.
        """

        byte_data = self.path.read_bytes()
        data = bson.loads(byte_data)
        
        return data
    
    def _dump(self) -> None:
        """
        Open the database file, and dump the current data to it. If the file
        does not exist, a new one is created.
        """

        if not self.path.exists():
            self.path.resolve().parent.mkdir(parents=True, exist_ok=True)

        data = bson.dumps(self._db)
        self.path.write_bytes(data)

    def __setitem__(self, key: str, value: dict) -> None:

        self._db[key] = value
        self._dump()
    
    def __getitem__(self, key: str) -> Any:
        try:
            self._load()
            return self._db[key]
        except KeyError:
            return None
        