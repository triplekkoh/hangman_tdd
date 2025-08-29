"""Core logic for the Hangman game."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Set, List
from hangman.selector import WordSelector, Level  # noqa: E501 pylint: disable= [E0401]

MASK_CHAR = "_"


class GuessResult(Enum):
    """Result of a guess attempt."""
    CORRECT = auto()
    INCORRECT = auto()
    REPEATED = auto()
    INVALID = auto()


@dataclass
class HangmanGame:
    """State and logic for a Hangman game session."""
    selector: WordSelector
    level: Level
    max_lives: int = 6
    answer: str = field(init=False)
    lives: int = max_lives
    guessed: Set[str] = field(default_factory=set, init=False)

    def __post_init__(self):
        """Initialize the game with a riddle and maximum lives."""
        self.answer = self.selector.pick_a_word(self.level).lower()
        self.lives = self.max_lives

    def masked(self) -> str:
        """Reveal found letters; keep spaces and non-letters as-is."""
        masked_chars: List[str] = []
        for ch in self.answer:
            if ch.isalpha():
                masked_chars.append(ch if ch in self.guessed else MASK_CHAR)
            else:
                masked_chars.append(ch)
        return "".join(masked_chars)

    def valid_guess(self, guess: str) -> bool:
        """Check if the guess is a single alphabetic character."""
        return len(guess) == 1 and guess.isalpha()
    
    def guess_letter(self, guess: str) -> GuessResult:
        """Process a letter guess and return guess result."""
        if not self.valid_guess(guess.lower()):
            return GuessResult.INVALID
        if guess.lower() in self.guessed:
            return GuessResult.REPEATED
        self.guessed.add(guess.lower())
        if guess.lower() in self.answer:
            return GuessResult.CORRECT
        self.lives -= 1
        return GuessResult.INCORRECT
    
    def is_won(self) -> bool:
        """Check if the game is won."""
        for ch in self.answer:
            if ch.isalpha() and ch not in self.guessed:
                return False
        return True

    def is_lost(self) -> bool:
        """Check if the game is lost."""
        return self.lives <= 0 and not self.is_won()

    def time_out(self):
        """Call this when the player times out on a guess."""
        self.lives -= 1
