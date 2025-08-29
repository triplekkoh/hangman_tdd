"""Module for selecting words or phrases based on difficulty level."""

import random as rnd
from dataclasses import dataclass
from enum import Enum, auto
from typing import List
import requests

# A list of valid basic words extarcted from a larger online dictionary.
WORD_LINK = "https://www.mit.edu/~ecprice/wordlist.10000"
RESPONSE = requests.get(WORD_LINK, timeout=10)
BASIC_WORDS = RESPONSE.content.splitlines()

# A list of intermediate phrases for intermediate players.
INTERMEDIATE_PHRASES: List[str] = [
    "agile methodology",
    "artificial intelligence",
    "continuous integration",
    "espresso machine",
    "data science",
    "northern territory",
    "object oriented programming",
    "personal computer",
    "test driven development",
    "user experience",
    "machine learning",
    "cloud computing",
    "source control",
    "information system",
    "network security",
    "virtual reality",
    "resource management",
    "debug mode",
    "memory leak",
    "syntax error"
]


class Level(Enum):
    """Game difficulty levels."""
    BASIC = auto()
    INTERMEDIATE = auto()


@dataclass
class WordSelector:
    """Select words or phrases based on difficulty level."""
    level: Level = Level.BASIC

    def pick_a_word(self, level: Level) -> str:
        """Pick a random word or phrase based on the selected level."""
        selected_word = ""
        if level == Level.BASIC:
            selected_word = rnd.choice(BASIC_WORDS).decode('UTF-8')
        elif level == Level.INTERMEDIATE:
            selected_word = rnd.choice(INTERMEDIATE_PHRASES)
        else:
            raise ValueError("Unknown level")
        return selected_word
