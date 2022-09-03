from typing import Union


class Difficulty:
    r"""
    Represents the Difficulty levels.

    Please note that these Difficulty values are consistent across the API as well.

    Attributes
    ----------
    id: int
        The difficulty ID.
    name: str
        The difficulty name.

    """

    def __init__(self, diff_id: int, name: str):
        self.id = diff_id
        self.name = name.lower()

    def __len__(self):
        return self.id

    def __str__(self):
        return self.name


# PRE DEFINED DIFFICULTIES
EASY = Difficulty(1, "easy")
MEDIUM = Difficulty(2, "medium")
HARD = Difficulty(3, "hard")

_diff = {1: EASY, 2: MEDIUM, 3: HARD}


def get_difficulty(difficulty: Union[int, str]) -> Difficulty:
    """
    Get the difficulty object associated with the difficulty.

    :param difficulty: Union[int, str]
        The difficulty ID or name.
    :return: Optional[:ref:`Difficulty`]
    """
    if isinstance(difficulty, int):
        return _diff[difficulty]

    for obj in _diff.values():
        if obj.name.lower() == difficulty.lower():
            return obj
