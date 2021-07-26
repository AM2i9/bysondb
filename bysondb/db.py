from typing import Any

from bysondb.base import BysonDBBase


class BysonDB(BysonDBBase):
    """
    A simple Key -> Value database.

    Example
    ----------
    ```
    my_db = BysonDB("my_db.bson")
    my_db["first_name"] = "John"
    my_db["age"] = 42

    print(f"My name is {my_db["first_name"]}, and I am {my_db["age"]} years old")
    ```

    Parameters
    -----------
    file: str
        The name or path to the file where the database will store it's data.
        The file will be created if it does not exist, or existing data
        will be loaded.
    """

    def __init__(self, file: str):
        super().__init__(file, {})

    def __setitem__(self, key: str, value: dict) -> None:

        self._db[key] = value
        self._dump()

    def __getitem__(self, key: str) -> Any:
        try:
            self._load()
            return self._db[key]
        except KeyError:
            return None

    def get_all(self) -> dict:
        """
        Returns a dict with all of the keys and their values.
        """
        self._load()
        return self._db

    def remove(self, key: str) -> None:
        """
        Remove a key from the database. Does nothing if the key does not exist.

        Parameters
        -----------
        key: str
            The key to remove from the database.
        """
        try:
            del self._db[key]
        except KeyError:
            pass
        else:
            self._dump()
